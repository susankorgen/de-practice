from copy import deepcopy

import pandas as pd

from quality import DataQualityIssueStore
from quality.DataQualityIssueStore import data_quality_issue_store

# Each member of the data_quality_issue_report list is a list:
#
# name,
# severity,
# description,
# demo_workaround,
# pipeline_segment (where issue was found),
# table_name (where issue was found),
# field_name (where issue was found).
# The first 4 items are copied from the data_quality_issue_store entry for the name.
# The remaining items are input by the caller.
#
# The pipeline_segment and table_name items gets appended to
# the data_quality_issue_store entry when the report entry is logged by
# that pipeline segment regarding that particular table.
#
# Possible pipeline_segment values are:
#   "read_input" (the pipeline READ segment)
#   "refine_input" (the pipeline REFINE segment)
#   "transform" (the pipeline ETL segment)
# Possible table_name values are:
#   "avocado"
#   "consumer"
#   "fertilizer"
#   "purchase"
#
# example:   ["BLOCKER-1a", 50.0, "PK is not unique in table", "mock values", "read_input", "consumer", "consumerid"]
#
data_quality_issue_report: list[list] = []

# headers for when we make data_quality_issue_report into a DataFrame for output to csv
data_quality_issue_report_columns: list[str] = [
    "name",
    "severity",
    "description",
    "demo_workaround",
    "pipeline_segment",
    "table_name",
    "field_name"
]


def report_quality_issue(issue_key: str, pipeline_segment: str = "", table_name: str = "", field_name: str = ""):
    data_quality_store_item = data_quality_issue_store.get(issue_key)
    if data_quality_store_item is None:
        data_quality_item = data_quality_issue_store["UNKNOWN"].copy()
    else:
        data_quality_item = data_quality_store_item.copy()
    data_quality_item.append(pipeline_segment)
    data_quality_item.append(table_name)
    data_quality_item.append(field_name)
    # TODO: add time_logged column
    data_quality_issue_report.append(data_quality_item)


def refine_data_quality_issue_report() -> pd.DataFrame:
    report = pd.DataFrame(data_quality_issue_report, columns=data_quality_issue_report_columns)
    report = report.sort_values(by=["severity", "name"], ascending=[False, True])
    return report
