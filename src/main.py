import argparse
from src.repositories.tender_repository import TenderRepository
from src.services.tender_service import parse_tenders


def main():
    parser = argparse.ArgumentParser(description="Tender scraper CLI")
    parser.add_argument("--max", type=int, default=100, help="Максимальное количество тендеров")
    parser.add_argument("--output", type=str, default="tenders.sqlite", help="Имя файла SQLite базы данных")
    args = parser.parse_args()

    try:
        print(f"Запускаем парсинг до {args.max} тендеров...")
        tenders = parse_tenders(max_tenders=args.max)
        print(f"Парсинг завершён, получено тендеров: {len(tenders)}")

        print(f"Сохраняем данные в базу {args.output}...")
        repo = TenderRepository(db_path=args.output)
        repo.save_tenders(tenders)
        print("Сохранение завершено успешно.")
    except Exception as e:
        raise RuntimeError(f"Произошла ошибка в процессе работы: {e}")


if __name__ == "__main__":
    main()
