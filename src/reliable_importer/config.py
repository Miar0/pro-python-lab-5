from pathlib import Path
import yaml
from reliable_importer.exceptions import ConfigurationError
from reliable_importer.models import AppConfig, LoggingConfig, ProcessingConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def load_config(path: Path) -> AppConfig:
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"Файл конфігурації не знайдено: {path}") from error
    except yaml.YAMLError as error:
        raise ConfigurationError("Некоректний YAML формат") from error

    try:
        # Додаємо BASE_DIR / до кожного шляху, щоб зробити його абсолютним
        config = AppConfig(
            input_path=BASE_DIR / str(raw["input"]["path"]),
            output_path=BASE_DIR / str(raw["output"]["path"]),
            processing=ProcessingConfig(
                skip_invalid=bool(raw["processing"]["skip_invalid"]),
                allowed_types=list(raw["processing"]["allowed_types"]),
                allowed_statuses=list(raw["processing"]["allowed_statuses"]),
            ),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=BASE_DIR / str(raw["logging"]["path"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError("Неправильна структура конфігурації") from error

    validate_config(config)
    return config


def validate_config(config: AppConfig) -> None:
    if not config.input_path.exists():
        raise ConfigurationError(f"Вхідний файл не знайдено: {config.input_path}")
    if not config.processing.allowed_types or not config.processing.allowed_statuses:
        raise ConfigurationError("Списки дозволених типів або статусів не можуть бути порожніми")