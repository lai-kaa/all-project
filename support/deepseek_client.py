"""
DeepSeek V4 API 客户端。
接口文档：https://api-docs.deepseek.com/
"""
import json
import urllib.error
import urllib.request

from django.conf import settings


class DeepSeekError(Exception):
    """DeepSeek API 调用异常"""


def ask_deepseek(question: str) -> str:
    """
    向 DeepSeek V4 发送用户问题，返回客服回答文本。
    默认使用 deepseek-v4-flash 模型。
    """
    api_key = settings.DEEPSEEK_API_KEY
    if not api_key:
        raise DeepSeekError(
            '未配置 DEEPSEEK_API_KEY。请在项目根目录 .env 文件中设置，'
            '例如：DEEPSEEK_API_KEY=sk-你的密钥，然后重启 runserver'
        )

    question = question.strip()
    if not question:
        raise DeepSeekError('问题不能为空')

    payload = {
        'model': settings.DEEPSEEK_MODEL,
        'messages': [
            {
                'role': 'system',
                'content': (
                    '你是中国铁路12306购票系统的智能客服助手。'
                    '请用简洁、专业的中文回答用户关于购票、退票、改签、'
                    '候补、注册登录、密码找回、座位类型等问题。'
                    '若问题与铁路购票无关，请礼貌引导用户咨询铁路相关事宜。'
                    '回答控制在 300 字以内，必要时使用条目列表。'
                ),
            },
            {'role': 'user', 'content': question},
        ],
        'temperature': 0.7,
        'max_tokens': 800,
    }

    request = urllib.request.Request(
        url=f'{settings.DEEPSEEK_BASE_URL.rstrip("/")}/chat/completions',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=settings.DEEPSEEK_TIMEOUT) as response:
            data = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='ignore')
        raise DeepSeekError(f'API 请求失败 ({exc.code}): {body}') from exc
    except urllib.error.URLError as exc:
        raise DeepSeekError(f'网络连接失败：{exc.reason}') from exc

    try:
        return data['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise DeepSeekError('API 返回格式异常') from exc
