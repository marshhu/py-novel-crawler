import re
import requests
from bs4 import BeautifulSoup


def get_page(url, encoding="utf-8"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    resp = requests.get(url=url, headers=headers)
    resp.encoding = "gbk"
    content = resp.text
    resp.close()
    return content


domain = "http://www.b520.cc"
start_url = "http://www.b520.cc/77_77704"

start_page = get_page(start_url, "gbk")

# 获取小说标题
title_pattern = re.compile("<h1>(?P<title>.*?)</h1>", re.S)
title_ret = title_pattern.finditer(start_page)
novel_title = title_ret.__next__().group("title")
# print(novel_title)

# 获取小说章节标题&链接
chapter_pattern = re.compile(r'<dd><a href="(?P<chapter_link>.*?)">(?P<chapter_title>.*?)</a></dd>', re.S)
chapter_ret = chapter_pattern.finditer(start_page)
chapter_links = []
chapter_titles = []
for item in chapter_ret:
    chapter_links.append(domain + item.group("chapter_link"))
    chapter_titles.append(item.group("chapter_title"))

# print(len(chapter_titles))
# print(len(chapter_links))

# 获取章节内容
f = open(novel_title + ".txt", mode="w", encoding="utf-8")
for i in range(0, len(chapter_links)):
    chapter_page = get_page(chapter_links[i], "gbk")

    soup = BeautifulSoup(chapter_page, "html.parser")
    content_ret = soup.find("div", attrs={"id": "content"})
    if content_ret is not None:
        f.write(chapter_titles[i] + "\n")
        f.write(content_ret.text + "\n")
        print(chapter_titles[i]+"------->成功")
    else:
        f.write(chapter_titles[i] + "\n")
        f.write("下载失败" + "\n")
        print(chapter_titles[i] + "------->下载失败")
f.close()

# f = open(novel_title + ".txt", mode="w", encoding="utf-8")
# for i in range(0, len(chapter_contents)):
#     f.write(chapter_titles[i] + "\n")
#     f.write(chapter_contents[i] + "\n")
# f.close()
