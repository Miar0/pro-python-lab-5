from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import ProcessingConfig, Room


def parse_room(row: dict[str, str], config: ProcessingConfig, *, line_number: int) -> Room:
    room_number = row.get("room_number", "").strip()
    if not room_number:
        raise RecordValidationError("Номер кімнати порожній", line_number=line_number, field="room_number")

    room_type = row.get("room_type", "").strip()
    if room_type not in config.allowed_types:
        raise RecordValidationError(f"Недопустимий тип кімнати: {room_type}", line_number=line_number,
                                    field="room_type")

    try:
        price = float(row["price"])
    except (KeyError, ValueError, TypeError) as error:
        raise RecordValidationError("Некоректна ціна", line_number=line_number, field="price") from error

    if price < 0:
        raise RecordValidationError("Ціна не може бути від'ємною", line_number=line_number, field="price")

    status = row.get("status", "").strip()
    if status not in config.allowed_statuses:
        raise RecordValidationError(f"Недопустимий статус: {status}", line_number=line_number, field="status")

    client = row.get("client", "").strip()
    if status == "Booked" and not client:
        raise RecordValidationError("Для заброньованої кімнати має бути вказаний клієнт", line_number=line_number,
                                    field="client")

    return Room(
        room_number=room_number,
        room_type=room_type,
        price=price,
        status=status,
        client=client
    )