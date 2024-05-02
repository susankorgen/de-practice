
# Each member of the dq_issue_report list is a list:
#
# name,
# severity,
# description
# demo_workaround
# pipeline_segment (where issue was found).
# table_name (where issue was found).
# All but the last item come from the dq_issue_store.
#
# The pipeline_segment and table_name items gets appended to
# the dq_issue_store entry when the report entry is logged by
# that pipeline segment regarding that particular table.
#
# Possible pipeline_segment values are:
#   "read_input" (the function used for the READ segment)
#   "refine_input" (the function used for the REFINE segment)
#   "transform" (the function used for the ETL segment)
# Possible table_name values are:
#   "avocado"
#   "consumer"
#   "fertilizer"
#   "purchase"
#
# example:   ["BLOCKER-1a", 50.0, "PK is not unique in table", "Mock values", "read_input", "consumer"]
#
dq_issue_report: list[list] = []

# headers for when we make dq_issue_report into a DataFrame for output to csv
dq_issue_report_headers: list[str] = [
    "name",
    "severity",
    "description",
    "demo_workaround",
    "pipeline_segment",
    "table_name"
]
