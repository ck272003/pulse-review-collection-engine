from datetime import datetime

def parse_iso_date(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", ""))
    except ValueError:
        return None
