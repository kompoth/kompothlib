import re

ISO_DATE_RE = re.compile(r"^(\d{2,4})(-(\d{1,2}))?(-\d{1,2})?$")

def extract_year(date: str | int) -> int:
    if isinstance(date, int):
        return date
    match = re.search(ISO_DATE_RE, date)
    return int(match.group(1))
