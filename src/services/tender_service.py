import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from src.config import BASE_URL, URL


def parse_tenders(max_tenders=100) -> List[Dict]:
    tenders = []
    page = 1

    while len(tenders) < max_tenders:
        url = f"{BASE_URL}?page={page}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка запроса страницы {page}: {e}")

        try:
            soup = BeautifulSoup(resp.text, "html.parser")
            table = soup.find("table", class_="table table-hover table-filled search-results")
            if not table:
                raise RuntimeError("Таблица с тендерами не найдена на странице")

            rows = table.find_all("tr")
            if not rows:
                raise RuntimeError("На странице нет строк с тендерами")

            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 4:
                    continue  # пропускаем заголовки и служебные строки

                goods_info = cells[0].get_text(separator=" ", strip=True)
                link_tag = cells[0].find("a", class_="search-results-title")
                tender_link = None
                tender_number = None
                if link_tag:
                    tender_link = URL + link_tag.get("href", "")
                    match = re.search(r"№\s*(\d+)", link_tag.text)
                    if match:
                        tender_number = match.group(1)

                organizer = cells[1].get_text(strip=True)
                publish_date = cells[2].get_text(strip=True)
                end_date = cells[3].get_text(strip=True)

                tenders.append({
                    "number": tender_number,
                    "link": tender_link,
                    "goods_description": goods_info,
                    "organizer": organizer,
                    "publish_date": publish_date,
                    "end_date": end_date,
                })

                if len(tenders) >= max_tenders:
                    break
        except Exception as e:
            raise RuntimeError(f"Ошибка парсинга страницы {page}: {e}")

        page += 1

    return tenders
