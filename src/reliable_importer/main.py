import logging
from pathlib import Path
import sys

from reliable_importer.config import load_config
from reliable_importer.exceptions import ApplicationError
from reliable_importer.exporters import export_rooms_json
from reliable_importer.logging_config import configure_logging
from reliable_importer.services import ImportStatistics, import_rooms
from reliable_importer.utils import logged_operation

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        config = load_config(BASE_DIR / "config.yaml")
        configure_logging(config.logging.level, config.logging.path)
        statistics = ImportStatistics()

        with logged_operation("Імпорт та експорт системи бронювання"):
            rooms = import_rooms(
                config.input_path,
                config=config.processing,
                statistics=statistics,
            )
            exported = export_rooms_json(rooms, config.output_path)

        logger.info(
            "Total=%s, valid=%s, invalid=%s, exported=%s",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            exported,
        )

    except ApplicationError as error:
        logger.error("Помилка програми: %s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()