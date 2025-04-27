import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
    'https://ip.164746.xyz'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 创建（或打开）一个文件来存储IP地址
with open('ip.txt', 'a') as file:  # 使用 'a' 模式追加内容
    for url in urls:
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            response.raise_for_status()  # 如果请求失败，会引发异常
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 根据网站的不同结构找到包含IP地址的元素
            if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
                elements = soup.find_all('tr')
            elif url == 'https://ip.164746.xyz':
                elements = soup.find_all('tr')
            else:
                elements = soup.find_all('li')
            
            # 遍历所有元素,查找IP地址
            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)
                
                # 如果找到IP地址,则写入文件
                for ip in ip_matches:
                    file.write(ip + '\n')
                    
            print(f'从 {url} 获取的 IP 地址已保存。')

        except requests.exceptions.RequestException as e:
            print(f"请求错误：{url}，错误信息：{e}")

print('IP地址已保存到ip.txt文件中。')
