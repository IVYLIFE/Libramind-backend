from datetime import date


def format_dates_in_dict(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = value.strftime("%d-%m-%Y")
    return data


def serialize(item):
    if hasattr(item, "model_dump"):
        item_dict = item.model_dump()
    elif hasattr(item, "dict"):
        item_dict = item.dict()
    else:
        item_dict = item

    if isinstance(item_dict, dict):
        return format_dates_in_dict(item_dict)
    return item_dict


def check_is_isbn(input_str: str) -> bool:
    """Check if the input string is likely an ISBN."""
    isbn_lengths = {10, 13}
    input_str = input_str.replace("-", "").strip()
    if len(input_str) not in isbn_lengths:
        return False

    if len(input_str) == 13 and input_str.startswith(('978', '979')):
        return True

    return True


# =====================================================================
