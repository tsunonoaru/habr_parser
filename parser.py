import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm  


def parse_habr_news(max_pages):
    base_url = "https://habr.com/ru/articles/page"
    headers = {"User-Agent": "Mozilla/5.0"}
    all_data = []

    try:
        for page in tqdm(range(1, max_pages + 1), desc="Парсинг страниц"):
            url = f"{base_url}{page}/"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"Страница {page} не загружается (код {response.status_code})")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all("article")

            for article in articles:
                title_tag = article.find("h2")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = "https://habr.com" + title_tag.find("a")["href"]
                    all_data.append({"Заголовок": title, "Ссылка": link})

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n Парсинг остановлен пользователем.")

    df = pd.DataFrame(all_data)
    df.to_csv("habr_all_news.csv", index=False, encoding='utf-8-sig')
    print(f"\nГотово! Собрано {len(all_data)} статей. Результат в habr_all_news.csv")


def main():
    try:
        max_pages = int(input("Сколько страниц спарсить? Введите число: "))
        parse_habr_news(max_pages)
    except ValueError:
        print("Ошибка: Введите целое число.")


if __name__ == '__main__':
    main()