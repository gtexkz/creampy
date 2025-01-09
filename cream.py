import requests
import os
import re
import browser_cookie3
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def download_media(tag=None, limit=5, urls=None, exclusions=None):
    os.makedirs('downloads', exist_ok=True)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        cookies = browser_cookie3.firefox()
    except Exception as e:
        print("Не удалось загрузить куки Firefox: ", e)
        cookies = None

    # Список исключений
    exclusions = [exclusion.strip() for exclusion in exclusions.split(',')] if exclusions else []

    if urls:
        for url in urls:
            if any(exclusion in url for exclusion in exclusions):
                print(f"Исключаем URL: {url}")
                continue
            
            try:
                response = requests.get(url, headers=headers, cookies=cookies)
                soup = BeautifulSoup(response.content, 'html.parser')
                media_url = None

                img_tag = soup.find('img', {'id': 'image'})
                video_tag = soup.find('source')

                if img_tag:
                    media_url = img_tag['src']
                elif video_tag:
                    media_url = video_tag['src']

                if media_url:
                    file_name = media_url.split('?')[0].split('/')[-1]
                    file_path = os.path.join('downloads', file_name)
                    file_data = requests.get(media_url, headers=headers, cookies=cookies).content
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
                    print(f"Скачано: {file_name}")
                else:
                    print("Медиафайлы не найдены на странице.")
            except Exception as e:
                print(f"Ошибка при скачивании с {url}: {e}")
    
    if tag:
        tags = tag.split(',')
        for t in tags:
            t = t.strip()
            if t in exclusions:
                print(f"Исключаем тег: {t}")
                continue
            url = f'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&tags={t}&limit={limit}'
            response = requests.get(url, headers=headers, cookies=cookies)
            
            if response.status_code != 200:
                print("Ошибка запроса к API")
                return

            posts = response.json()
            if not posts:
                print(f"Медиа не найдены для тега: {t}")
                continue

            for post in posts:
                file_url = post.get('file_url')
                if not file_url:
                    continue

                file_name = file_url.split('?')[0].split('/')[-1]
                file_path = os.path.join('downloads', file_name)

                try:
                    file_data = requests.get(file_url, headers=headers, cookies=cookies).content
                    with open(file_path, 'wb') as file:
                        file.write(file_data)
                    print(f"Скачано: {file_name}")
                except Exception as e:
                    print(f"Ошибка при скачивании {file_name}: {e}")

def on_submit():
    choice = choice_var.get()
    limit = int(limit_entry.get())
    exclusions = exclusion_entry.get()
    if choice == "1":
        tags = tag_entry.get()
        if not tags:
            messagebox.showerror("Ошибка", "Введите хотя бы один тег.")
            return
        download_media(tag=tags, limit=limit, exclusions=exclusions)
    elif choice == "2":
        urls = url_entry.get().split(",")
        if not urls:
            messagebox.showerror("Ошибка", "Введите хотя бы одну ссылку.")
            return
        download_media(urls=urls, exclusions=exclusions)

root = tk.Tk()
root.title("Скачивание медиа с Rule34")

choice_var = tk.StringVar(value="1")

tk.Radiobutton(root, text="По тегу", variable=choice_var, value="1").pack(anchor="w")
tk.Radiobutton(root, text="По ссылке", variable=choice_var, value="2").pack(anchor="w")

tk.Label(root, text="Введите теги (через запятую) или ссылки (через запятую):").pack()
tag_entry = tk.Entry(root, width=50)
tag_entry.pack()

tk.Label(root, text="Введите теги или ссылки для исключения (через запятую):").pack()
exclusion_entry = tk.Entry(root, width=50)
exclusion_entry.pack()


tk.Label(root, text="Сколько файлов скачать?").pack()
limit_entry = tk.Entry(root)
limit_entry.pack()


submit_button = tk.Button(root, text="Скачать", command=on_submit)
submit_button.pack()

root.mainloop()
