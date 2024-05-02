import datetime
import math
import numbers
from io import StringIO

import pandas as pd
from dateutil.relativedelta import relativedelta

from quality.DataQualityIssueReport import report_quality_issue


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


def safe_positive_int(original_value, pipeline_segment: str = "", table_name: str = "", field_name: str = "") -> int:
    output_value = safe_int_type_or_none(original_value, pipeline_segment, table_name, field_name)
    if output_value is None:
        try:
            output_value = int(math.floor(original_value))
        except ValueError:
            output_value = 0
    else:
        if output_value < 0:
            report_quality_issue("RANGE-5a", pipeline_segment, table_name, field_name)
            output_value = 0
    return output_value


def safe_int_range(original_value, min_value: int = 0, max_value: int = None, pipeline_segment: str = "", table_name: str = "", field_name: str = "") -> int:
    output_value = safe_int_type_or_none(original_value, pipeline_segment, table_name, field_name)
    if output_value is None:
        try:
            output_value = int(math.floor(original_value))
        except ValueError:
            if isinstance(original_value, numbers.Real):
                report_quality_issue("UNEXPECTED-6c", pipeline_segment, table_name, field_name)
            elif isinstance(original_value, numbers.Integral):
                report_quality_issue("UNEXPECTED-6z", pipeline_segment, table_name, field_name)
            else:
                report_quality_issue("UNEXPECTED-6k", pipeline_segment, table_name, field_name)
            output_value = 0
    if output_value < min_value:
        report_quality_issue("RANGE-5a", pipeline_segment, table_name, field_name)
        output_value = min_value
    if max_value is not None and output_value > max_value:
        report_quality_issue("RANGE-5b", pipeline_segment, table_name, field_name)
        output_value = max_value
    return output_value


def safe_int_type_or_none(original_value, pipeline_segment: str = "", table_name: str = "", field_name: str = "") -> int:
    output_value = original_value
    if original_value is None:
        report_quality_issue("MISSING-3c", pipeline_segment, table_name, field_name)
        output_value = None
    elif type(original_value) == str:
        report_quality_issue("UNEXPECTED-6h", pipeline_segment, table_name, field_name)
        output_value = int(original_value)
    elif type(original_value) != int:
        if isinstance(original_value, numbers.Real):
            report_quality_issue("UNEXPECTED-6i", pipeline_segment, table_name, field_name)
            output_value = None
        elif isinstance(original_value, numbers.Integral):
            report_quality_issue("UNEXPECTED-6j", pipeline_segment, table_name, field_name)
            output_value = int(original_value)
        else:
            report_quality_issue("UNEXPECTED-6k", pipeline_segment, table_name, field_name)
            output_value = None
    return output_value


def safe_number_string(input_value, pipeline_segment: str = "", table_name: str = "", field_name: str = "") -> str:
    if input_value is None or input_value == "":
        report_quality_issue("UNEXPECTED-6d", pipeline_segment, table_name, field_name)
        return "Empty"
    try:
        output_value = f"{int(input_value)}"
    except ValueError:
        report_quality_issue("UNEXPECTED-6e", pipeline_segment, table_name, field_name)
        return "Unknown"
    return safe_string(output_value, pipeline_segment, table_name, field_name)


def safe_string(input_value, pipeline_segment: str = "", table_name: str = "", field_name: str = "") -> str:
    """Addresses UNICODE character problems for the required ASCII output format."""
    try:
        input_value.encode("ascii")
        output_value = input_value
    except UnicodeEncodeError:
        report_quality_issue("UNEXPECTED-6b", pipeline_segment, table_name, field_name)
        output_value = "other"
    return output_value


def safe_demo_date(original_string, default, offset: int = 0, pipeline_segment: str = "", table_name: str = "", field_name: str = ""):
    if original_string is None:
        report_quality_issue("UNEXPECTED-6f", pipeline_segment, table_name, field_name)
        return default
    if type(original_string) is not str:
        report_quality_issue("UNEXPECTED-6g", pipeline_segment, table_name, field_name)
        return default
    input_string = original_string.split(" ")[0]
    try:
        output_value = datetime.datetime.strptime(input_string, "%Y-%m-%d")
        output_value += relativedelta(years=offset)
    except TypeError:
        report_quality_issue("DATATYPE-4c", pipeline_segment, table_name, field_name)
        output_value = default
    return output_value


def get_markdown(default_output_md: str, demo_data: pd.DataFrame) -> str:
    demo_data.to_markdown(buf=default_output_md)
    buffer = StringIO()
    demo_data.to_markdown(buf=buffer)
    buffer.seek(0)
    return buffer.read()


def write_html(default_output_html: str, demo_data: pd.DataFrame) -> None:
    demo_data.to_html(buf=default_output_html)