import requests
import time
import random
from datetime import datetime
from colorama import Fore, Style

def send_click_request(use_proxy):
    # Đọc thông tin từ file user.txt
    user_data = {}
    with open("user.txt", "r") as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                user_data[key.strip()] = value.strip()

    api_url = "https://api-clicker.pixelverse.xyz/api/users"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Content-Type": "application/json",
        "Initdata": user_data.get("Initdata"),
        "Origin": "https://sexyzbot.pxlvrs.io",
        "Priority": "u=1, i",
        "Referer": "https://sexyzbot.pxlvrs.io/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Secret": user_data.get("Secret"),
        "Tg-Id": user_data.get("Tg-Id"),
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Username": user_data.get("Username")
    }
    data = {"clicksAmount": random.randint(1, 10)}

    proxies = None
    if use_proxy:
        with open("proxy.txt", "r") as f:
            proxy_url = f.readline().strip()
            proxy_username = f.readline().strip()
            proxy_password = f.readline().strip()

            proxies = {
                'http': f'http://{proxy_username}:{proxy_password}@{proxy_url}',
                'https': f'http://{proxy_username}:{proxy_password}@{proxy_url}'
            }

    try:
        print(f"Sending request at {datetime.now()} (Proxy: {use_proxy})")
        response = requests.post(api_url, headers=headers, json=data, proxies=proxies)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
        return None

# Hiển thị thông báo khi bắt đầu chạy (màu đỏ)
print(Fore.RED + "Pixelverse BOT " + Style.RESET_ALL)

# Lựa chọn sử dụng proxy
use_proxy = input("Do you want to use a proxy? (y/n): ").lower() == 'y'

while True:
    response_data = send_click_request(use_proxy)

    if response_data:
        energy = response_data.get('pet', {}).get('energy', 0)
        if energy >= 5:
            print(f"Clicks count: {response_data.get('clicksCount', 0)}")
            print(f"Pet level: {response_data.get('pet', {}).get('level', 0)}")
            print(f"Energy: {energy}")
        else:
            print(f"Energy low ({energy}). Waiting 5 minutes...")
            time.sleep(300)
    else:
        print("Request failed. Waiting 5 minutes...")
        time.sleep(300)
