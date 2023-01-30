from datetime import datetime


def set_validate_birthday_or_none(birthday):
    if birthday:
        current_year = datetime.now().strftime('%Y')
        birthday_year = str(birthday)[:4]
        if (int(birthday_year) + 18) > int(current_year):
            return None
    return birthday
