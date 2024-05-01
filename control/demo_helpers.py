import datetime
import math
import random
from io import StringIO

import pandas as pd
from dateutil.relativedelta import relativedelta


def diff_days(start_date, end_date) -> int:
    return int((start_date - end_date).days)


def get_random_gender(index: int) -> str:
    """Use a snapshot of a past random result to support consistent output for unit tests"""
    gender = [
        "Unknown",
        "Non-binary",
        "Female",
        "Unknown",
        "Unknown",
        "Male",
        "Female",
        "Female",
        "Non-binary",
        "Unknown",
        "Unknown",
        "Male",
        "Male",
        "Male",
        "Male",
        "Unknown",
        "Unknown",
        "Non-binary",
        "Non-binary",
        "Male",
        "Female",
        "Non-binary",
        "Female",
        "Unknown",
        "Male",
        "Male",
        "Female",
        "Unknown",
        "Male",
        "Non-binary",
        "Male",
        "Unknown",
        "Non-binary",
        "Male",
        "Non-binary",
        "Male",
        "Non-binary",
        "Female",
        "Unknown",
        "Non-binary",
        "Non-binary",
        "Male",
        "Male",
        "Female",
        "Non-binary",
        "Female",
        "Male",
        "Non-binary",
        "Female",
        "Non-binary",
        "Female",
        "Unknown"
    ]
    return gender[index]


def get_random_age(index: int) -> int:
    """Use a snapshot of a past random result to support consistent output for unit tests"""
    age = [
        40,
        43,
        1,
        26,
        23,
        62,
        35,
        16,
        56,
        85,
        26,
        79,
        77,
        8,
        97,
        53,
        67,
        4,
        11,
        48,
        87,
        72,
        77,
        9,
        23,
        98,
        45,
        98,
        62,
        5,
        49,
        86,
        48,
        34,
        82,
        48,
        97,
        99,
        80,
        14,
        56,
        76,
        23,
        16,
        33,
        64,
        66,
        96,
        33,
        50,
        37,
        92
    ]
    return age[index]


def get_random_fertilizer(index: int) -> str:
    """Use a snapshot of a past random result to support consistent output for unit tests"""
    fertilizer = [
        "inorganic 1 mg ONCE PRN",
        "heavy metal 100 mg EVERY 6 HOURS SCHEDULED",
        "heavy metal 1 mg PRN",
        "inorganic 100 mg EVERY 6 HOURS PRN",
        "other",
        "dry 1 mg EVERY 6 HOURS PRN",
        "heavy metal 100 mg EVERY 6 HOURS",
        "heavy metal 100 mg EVERY 4 HOURS PRN",
        "inorganic 1 mg 3 TIMES DAILY PRN",
        "inorganic 100 mg EVERY 15 MIN PRN",
        "heavy metal 100 mg EVERY 4 HOURS PRN",
        "other",
        "heavy metal 1 mg DAILY PRN",
        "organic 1 mg CONTINUOUS",
        "organic 1 mg EVERY 6 HOURS",
        "heavy metal 10000 mg EVERY MON, WED, AND FRI",
        "organic 100 mg DAILY",
        "inorganic 10000 mg ONCE PRN",
        "organic 1 mg EVERY 24 HOURS",
        "heavy metal 100 mg 2 TIMES DAILY",
        "organic 10000 mg EVERY 6 HOURS SCHEDULED",
        "other",
        "organic 10000 mg CONTINUOUS",
        "heavy metal 10000 mg NIGHTLY",
        "dry 10000 mg CONTINUOUS PRN",
        "other",
        "dry 100 mg EVERY MORNING 1 HOUR BEFORE BREAKFAST",
        "organic 10000 mg EVERY 24 HOURS",
        "heavy metal 10000 mg EVERY MON, WED, AND FRI",
        "inorganic 100 mg EVERY 8 HOURS PRN",
        "organic 100 mg EVERY 8 HOURS",
        "other",
        "dry 10000 mg ONCE",
        "other",
        "dry 100 mg NIGHTLY",
        "heavy metal 100 mg 3 TIMES DAILY PRN",
        "heavy metal 100 mg PIB AND PCEA",
        "other",
        "inorganic 1 mg CONTINUOUS PRN",
        "dry 100 mg EVERY 24 HOURS",
        "other",
        "inorganic 1 mg ONCE PRN",
        "heavy metal 1 mg PIB AND PCEA",
        "inorganic 1 mg EVERY 15 MIN PRN",
        "other",
        "dry 1 mg EVERY 8 HOURS PRN",
        "organic 1 mg DAILY",
        "inorganic 1 mg EVERY 6 HOURS PRN",
        "dry 1 mg PRN",
        "organic 1 mg EVERY MORNING 1 HOUR BEFORE BREAKFAST",
        "heavy metal 10000 mg CONTINUOUS PRN",
        "dry 100 mg EVERY 6 HOURS PRN"
    ]
    return fertilizer[index]


def safe_int(original_value) -> int:
    # TODO: detect original_value data type: if null or not str, log the correct DQI
    try:
        output_value = int(math.floor(original_value))
    except ValueError:
        output_value = 0
    if output_value < 0:
        output_value = 0
    return output_value


def safe_number_string(input_value) -> str:
    # TODO: detect input_value data type: if null or not int, log the correct DQI
    if input_value is None or input_value == "":
        return "Empty"
    try:
        output_value = f"{int(input_value)}"
    except ValueError:
        return "Unknown"
    return safe_string(output_value)


def safe_string(input_value) -> str:
    """Addresses UNICODE character problems for the required ASCII output format."""
    # TODO: detect input_value characteristics: if invalid, log the correct DQI
    try:
        input_value.encode("ascii")
        output_value = input_value
    except UnicodeEncodeError:
        output_value = "other"
    return output_value


def safe_demo_date(original_string, default, offset: int = 0):
    # TODO: detect input_string characteristics: if invalid, log the correct DQI
    # TODO: revisit datetime day counts for consistent results, remove workaround in today_date
    if original_string is None:
        return default
    if type(original_string) is not str:
        return default
    input_string = original_string.split(" ")[0]
    try:
        output_value = datetime.datetime.strptime(input_string, "%Y-%m-%d")
        output_value += relativedelta(years=offset)
    except TypeError:
        output_value = default
    return output_value


def get_markdown_demo(default_output_md, demo_data: pd.DataFrame) -> str:
    demo_data.to_markdown(buf=default_output_md)
    buffer = StringIO()
    demo_data.to_markdown(buf=buffer)
    buffer.seek(0)
    return buffer.read()


def get_html_demo(default_output_html, demo_data: pd.DataFrame) -> None:
    demo_data.to_html(buf=default_output_html)