# Hotel Booking Reliable Importer

Лабораторна робота №5 з дисципліни «Професійний Python»

## Опис проєкту

Модуль надійного імпорту, експорту та конфігурації даних для системи бронювання готелю (Варіант 8).  
Проєкт демонструє побудову стійких (reliable) Python-застосунків, що коректно працюють із помилками, файловими ресурсами та структурованими форматами (CSV, JSON, YAML). Реалізовано потокову обробку даних (streaming I/O) для економії пам'яті, атомарний експорт результатів, користувацьку ієрархію винятків (custom exceptions) із підтримкою exception chaining, а також політику толерантної валідації (fail-fast / tolerant mode) із записом подій у лог.

## Структура проєкту (src-layout)

```text
hotel_booking/
│
├── pyproject.toml
├── config.yaml
├── README.md
├── .gitignore
├── data/
│   └── rooms.csv
├── output/
├── logs/
└── src/
    └── reliable_importer/
        ├── __init__.py
        ├── main.py
        ├── config.py
        ├── exceptions.py
        ├── models.py
        ├── readers.py
        ├── validators.py
        ├── exporters.py
        ├── logging_config.py
        ├── services.py
        └── utils.py
```

- `exceptions.py` — доменна ієрархія помилок застосунку (ApplicationError, ConfigurationError, RecordValidationError).
- `models.py` — dataclass-моделі для представлення кімнат готелю та конфігурації.
- `config.py` — завантаження та fail-fast валідація YAML-конфігурації.
- `readers.py` — генератор для потокового читання великих CSV-файлів без переповнення пам'яті.
- `validators.py` — перевірка бізнес-правил Варіанта 8 (валідність типу кімнати, ціна >= 0, статус, наявність клієнта).
- `services.py` — оркестрація імпорту з підрахунком статистики (valid/invalid records) та логуванням збоїв.
- `exporters.py` — потоковий JSON-експорт із використанням механізму атомарного запису (через .tmp файл).
- `utils.py` — власний context manager для логування часу виконання операцій.

## Вимоги

- Python 3.12+
- uv
- pyyaml

## Встановлення та запуск

1. Встановлення залежностей через `uv`:

```bash
uv sync
```

2. Запуск процесу імпорту/експорту:

```bash
uv run python src/reliable_importer/main.py
```

## Приклад роботи програми

```text
2026-09-30 11:18:49,325 | INFO | reliable_importer.utils | Імпорт та експорт системи бронювання розпочато
2026-09-30 11:18:49,326 | WARNING | reliable_importer.services | Некоректний запис у рядку 5: Недопустимий тип кімнати: Unknown
2026-09-30 11:18:49,327 | WARNING | reliable_importer.services | Некоректний запис у рядку 6: Ціна не може бути від'ємною
2026-09-30 11:18:49,327 | WARNING | reliable_importer.services | Некоректний запис у рядку 7: Для заброньованої кімнати має бути вказаний клієнт
2026-09-30 11:18:49,328 | INFO | reliable_importer.utils | Імпорт та експорт системи бронювання завершено за 0.001895 с
2026-09-30 11:18:49,328 | INFO | __main__ | Total=6, valid=3, invalid=3, exported=3
```

## Автор

Студент: Івасів Данило  
Група: ФеП-32  
Викладач: доц. Куньо І. М.