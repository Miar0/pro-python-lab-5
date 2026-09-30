from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class Room:
    room_number: str
    room_type: str
    price: float
    status: str
    client: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    skip_invalid: bool
    allowed_types: list[str]
    allowed_statuses: list[str]

@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    path: Path

@dataclass(frozen=True, slots=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig