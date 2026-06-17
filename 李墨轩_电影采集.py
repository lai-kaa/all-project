# 导入需要的库
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --------------------------
# 全局配置
# --------------------------
# 基础分页网址模板
BASE_URL = "https://movie.douban.com/top250?start={}&filter="

# 请求头，伪装浏览器，防止反爬拦截
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://movie.douban.com/",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

# 存储全部电影数据
movie_list = []


# --------------------------
# 函数1：获取单页网页源码（封装 + 异常处理）
# --------------------------
def get_html(url):
    """
    传入url，返回网页html文本
    加入try-except异常捕获，请求失败返回None
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = "utf-8"  # 解决中文乱码
        return response.text
    except Exception as e:
        print(f"网页请求异常：{e}")
        return None


# --------------------------
# 函数2：解析单页电影数据
# --------------------------
def parse_html(html, rank_start):
    """
    解析html，提取：排名、电影名、评分、电影链接、图片地址
    rank_start：当前页起始排名
    """
    # 构建解析器
    soup = BeautifulSoup(html, "html.parser")
    # 定位所有电影条目
    item_list = soup.find_all("div", class_="item")

    # 遍历每一部电影
    for idx, item in enumerate(item_list):
        # 1. 电影排名
        rank = rank_start + idx

        # 2. 电影标题
        title_tag = item.find("span", class_="title")
        title = title_tag.text.strip() if title_tag else "无标题"

        # 3. 电影评分
        rating_tag = item.find("span", class_="rating_num")
        rating = rating_tag.text.strip() if rating_tag else "无评分"

        # 4. 电影详情链接
        a_tag = item.find("div", class_="pic").find("a")
        movie_link = a_tag.get("href") if a_tag else "无链接"

        # 5. 电影图片地址
        img_tag = item.find("img")
        img_url = img_tag.get("src") if img_tag else "无图片地址"

        # 存入列表
        movie_list.append({
            "电影排名": rank,
            "电影标题": title,
            "评分": rating,
            "电影链接": movie_link,
            "电影图片地址": img_url
        })


# --------------------------
# 主程序：循环爬取10页全部250部
# --------------------------
def main():
    # 豆瓣Top250一共10页，每页25条
    total_page = 10
    for page in range(total_page):
        # 计算分页start参数
        start_num = page * 25
        url = BASE_URL.format(start_num)
        print(f"正在抓取第 {page+1} 页...")

        # 获取网页源码
        html = get_html(url)
        if not html:
            print(f"第 {page+1} 页获取失败，跳过")
            continue

        # 解析当前页，传入起始排名
        parse_html(html, rank_start=start_num + 1)

        # 延时1秒，防IP封禁
        time.sleep(1)

    # --------------------------
    # 保存数据到Excel
    # --------------------------
    df = pd.DataFrame(movie_list)
    print("\n抓取完成，共抓取：", len(df), "部电影")
    print("\n前5条数据预览：")
    print(df.head())

    # 保存Excel
    df.to_csv("李墨轩_movie_top250.csv", index=False,encoding="ANSI")
    print("\n数据已保存为：李墨轩_movie_top250.csv")


# 程序入口
if __name__ == "__main__":
    main()