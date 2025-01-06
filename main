import requests
import os
import re
import browser_cookie3
from bs4 import BeautifulSoup

def download_media(tag=None, limit=5, urls=None):
    os.makedirs('downloads', exist_ok=True)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        cookies = browser_cookie3.firefox()
    except Exception as e:
        print("Не удалось загрузить куки Firefox: ", e)
        cookies = None

    if urls:
        for url in urls:
            try:
                response = requests.get(url, headers=headers, cookies=cookies)
                soup = BeautifulSoup(response.content, 'html.parser')
                media_url = None

                # Попытка найти изображения и видео
                img_tag = soup.find('img', {'id': 'image'})
                video_tag = soup.find('source')

                if img_tag:
                    media_url = img_tag['src']
                elif video_tag:
                    media_url = video_tag['src']

                if media_url:
                    # Корректное извлечение имени файла
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
        url = f'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&tags={tag}&limit={limit}'
        response = requests.get(url, headers=headers, cookies=cookies)
        
        if response.status_code != 200:
            print("Ошибка запроса к API")
            return

        posts = response.json()
        if not posts:
            print("Медиа не найдены.")
            return

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

if __name__ == "__main__":
    choice = input("Вы хотите скачать по тегу (1) или ссылке (2)? Введите 1 или 2: ")
    if choice == "1":
        tag = input("Введите тег для поиска: ")
        limit = int(input("Сколько файлов скачать? "))
        download_media(tag, limit)
    elif choice == "2":
        urls = input("Введите ссылки через запятую: ").split(",")
        download_media(urls=urls)
