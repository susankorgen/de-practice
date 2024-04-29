import datetime
import random

from dateutil.relativedelta import relativedelta


def diff_days(start_date, end_date) -> int:
    return int((start_date - end_date).days)


def get_random_gender() -> str:
    gender = ["Male", "Female", "Non-binary", "Unknown"]
    return random.choice(gender)


def get_random_age() -> int:
    return random.randint(0, 105)


def get_random_fertilizer() -> str:
    poop_type = [
        "dry",
        "heavy metal",
        "organic",
        "inorganic",
        "ʑebrafish chub"
    ]
    mg = [
        "1",
        "100",
        "10000"
    ]
    frequency = [
        "ONCE",
        "ONCE PRN",
        "EVERY 6 HOURS PRN",
        "EVERY 8 HOURS",
        "EVERY 24 HOURS",
        "CONTINUOUS",
        "EVERY 6 HOURS SCHEDULED",
        "PRN",
        "DAILY",
        "2 TIMES DAILY",
        "DAILY PRN",
        "2 TIMES DAILY PRN",
        "EVERY 4 HOURS PRN",
        "3 TIMES DAILY PRN",
        "EVERY 6 HOURS",
        "CONTINUOUS PRN",
        "EVERY 8 HOURS PRN",
        "EVERY MON, WED, AND FRI",
        "EVERY 15 MIN PRN",
        "EVERY MORNING 1 HOUR BEFORE BREAKFAST",
        "NIGHTLY",
        "PIB AND PCEA"
    ]
    return safe_string(
        f"{random.choice(poop_type)} {random.choice(mg)} mg {random.choice(frequency)}"
    )


def safe_int(input_value) -> int:
    try:
        output_value = int(input_value)
    except ValueError:
        output_value = 0
    if output_value < 0:
        output_value = 0
    return output_value


def safe_number_string(input_value) -> str:
    if input_value is None or input_value == "":
        return "Empty"
    try:
        output_value = f"{int(input_value)}"
    except ValueError:
        return "Unknown"
    return safe_string(output_value)


def safe_string(input_value) -> str:
    """Addresses UNICODE character problems for the required ASCII output format."""
    try:
        input_value.encode("ascii")
        output_value = input_value
    except UnicodeEncodeError:
        output_value = "Invalid Format"
    return output_value


def safe_demo_date(input_string: str, default, offset: int = 0):
    if input_string is None:
        output_value = default
    else:
        try:
            output_value = datetime.datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
            output_value += relativedelta(years=offset)
        except TypeError:
            output_value = default
    return output_value
