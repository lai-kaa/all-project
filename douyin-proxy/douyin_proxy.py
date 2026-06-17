#!/usr/bin/env python3
"""
抖音 VRChat 视频代理 v3.1（多线程 + 速度优化）
启动：python vrchat_proxy.py
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import ssl
import socket
import sys
import threading

PORT = 8765
BUFFER_SIZE = 4 * 1024 * 1024  # 4MB 缓冲块，减少系统调用
TIMEOUT = 60  # 统一超时（秒）

# ============ 伪造移动端请求头（CDN 对移动端限速更宽松）============
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36',
    'Accept': 'video/mp4,video/webm,video/*,*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.douyin.com/',
    'Origin': 'https://www.douyin.com',
    'Connection': 'keep-alive',
}


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """多线程服务器，支持同时多个请求"""
    daemon_threads = True


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 健康检查
        if path == '/' or path == '/health':
            self._health_page()
            return

        # 方式1: /proxy-raw/ + URL编码的直链（VRChat用）
        if path.startswith('/proxy-raw/'):
            raw = path[len('/proxy-raw/'):]
            target_url = urllib.parse.unquote(raw)
            self._stream_video(target_url)
            return

        # 方式2: /proxy?url= （浏览器测试用）
        if path == '/proxy':
            params = urllib.parse.parse_qs(parsed.query)
            target_url = params.get('url', [None])[0]
            if not target_url:
                self.send_error(400, '缺少 url 参数')
                return
            self._stream_video(target_url)
            return

        self.send_error(404)

    def _health_page(self):
        ip = get_local_ip()
        html = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>VRChat Proxy</title>
<style>body{{font-family:system-ui;margin:40px;background:#1a1a2e;color:#eee}}
h2{{color:#00d4aa}}code{{background:#16213e;padding:4px 8px;border-radius:4px;word-break:break-all}}</style></head>
<body>
<h2>✅ 代理运行中 v3.1（多线程优化版）</h2>
<p>端口: {PORT} | 本机IP: {ip}</p>
<h3>VRChat 粘贴：</h3>
<p><code>http://{ip}:{PORT}/proxy-raw/URL编码的直链</code></p>
<h3>浏览器测试：</h3>
<p><code>http://localhost:{PORT}/proxy?url=直链</code></p>
</body></html>'''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode())

    def _stream_video(self, target_url):
        if not target_url:
            self.send_error(400)
            return

        short = target_url.split('?')[0]
        short_name = short.split('/')[-1][:30] if '/' in short else short[:30]
        print(f'📡 [{threading.current_thread().name}] {short_name}...', end=' ', flush=True)

        headers = dict(HEADERS)
        if not ('douyin' in target_url or 'douyinvod' in target_url or 'bytecdn' in target_url):
            headers.pop('Referer', None)

        try:
            req = urllib.request.Request(target_url, headers=headers)

            # 透传 Range 头（断点续传 / 拖动进度条）
            range_header = self.headers.get('Range', '')
            if range_header:
                req.add_header('Range', range_header)

            # 忽略 SSL 证书
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # ⚠️ 旧版 Python 只支持单个数字 timeout，不能用元组
            resp = urllib.request.urlopen(req, context=ctx, timeout=TIMEOUT)

            # 转发响应头
            self.send_response(resp.status)
            content_type = resp.headers.get('Content-Type', 'video/mp4')
            content_length = resp.headers.get('Content-Length', '')
            content_range = resp.headers.get('Content-Range', '')

            self.send_header('Content-Type', content_type)
            if content_length:
                self.send_header('Content-Length', content_length)
            if content_range:
                self.send_header('Content-Range', content_range)
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Range, Origin')
            self.send_header('Access-Control-Expose-Headers', 'Content-Range, Content-Length')
            self.end_headers()

            # 流式传输
            total = 0
            while True:
                chunk = resp.read(BUFFER_SIZE)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                    total += len(chunk)
                except (ConnectionAbortedError, BrokenPipeError, ConnectionResetError):
                    print(f'⏹️ 客户端断开 ({total/1024/1024:.1f}MB已传)', flush=True)
                    return

            size_mb = total / 1024 / 1024
            print(f'✅ {size_mb:.1f}MB', flush=True)

        except urllib.error.HTTPError as e:
            print(f'❌ HTTP {e.code}', flush=True)
            try:
                self.send_error(e.code, str(e))
            except:
                pass
        except (socket.timeout, TimeoutError):
            print(f'⏰ 超时', flush=True)
            try:
                self.send_error(504, 'Gateway Timeout')
            except:
                pass
        except Exception as e:
            print(f'❌ {e}', flush=True)
            try:
                self.send_error(502, str(e))
            except:
                pass

    def log_message(self, format, *args):
        pass  # 静默


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'


if __name__ == '__main__':
    local_ip = get_local_ip()
    print('═' * 55)
    print('  🎬  抖音 → VRChat 代理 v3.1 (多线程优化)')
    print('═' * 55)
    print(f'  本机:     http://localhost:{PORT}')
    print(f'  局域网:   http://{local_ip}:{PORT}')
    print()
    print('  VRChat 粘贴:')
    print(f'  http://{local_ip}:{PORT}/proxy-raw/编码后的链接')
    print()
    print('  浏览器测试:')
    print(f'  http://localhost:{PORT}/proxy?url=直链')
    print('═' * 55)

    server = ThreadingHTTPServer(('0.0.0.0', PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n代理已停止')
        server.shutdown()