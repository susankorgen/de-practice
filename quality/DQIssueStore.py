
# Data value quality issues are discoverable during daily processing.
# This global value holds definitions of data quality issues for the pipeline.
#
# Each member of the dq_issue_store dictionary is a list:
# name,
# severity,
# description
# demo_workaround
#
# example:   ["BLOCKER-1a", 50.0, "PK is not unique in table", "Mock values"]
#
dq_issue_store: dict = dict(
    {
        "BLOCKER-1a": ["BLOCKER-1a", 50.0, "PK is not unique in table", "mock values"],
        "BLOCKER-1b": ["BLOCKER-1b", 30.0, "Missing value for a field that is NOT NULLABLE (PKs and FKs)", "skip row"],
        "MISSING-2a": ["MISSING-2a", 20.0, "Missing value for a field that is NOT NULLABLE (PKs and FKs)", "skip row"],
        "MISSING-3a": ["MISSING-3a", 20.0, "Missing value for a demographic field needed for analysis", "choose random row from real data"],
        "MISSING-3b": ["MISSING-3b", 20.0, "Missing value for a date field needed for analysis", "set to today"],
        "MISSING-3c": ["MISSING-3c", 20.0, "Missing value for a 0-10 int needed for analysis", "set to 0"],
        "DATATYPE-4a": ["DATATYPE-4a", 10.0, "Inconsistent date format values", "strip time off the date strings"],
        "DATATYPE-4b": ["DATATYPE-4b", 10.0, "Inappropriate data type for identifier (float)", "convert to int"],
        "DATATYPE-4c": ["DATATYPE-4c", 10.0, "Date value that is non-empty but not parseable as a date", "use empty"],
        "RANGE-5a": ["RANGE-5a", 8.0, "Super old dates", "set to 365"],
        "RANGE-5b": ["RANGE-5b", 8.0, "Negative ages", "set to 0"],
        "RANGE-5c": ["RANGE-5c", 8.0, "Negative numbers of days", "set to 0"],
        "RANGE-5d": ["RANGE-5d", 8.0, "Ripe index > 10 or < 0", "adjust to 10 or 0 respectively"],
        "RANGE-5e": ["RANGE-5e", 8.0, "Dates in the future as of today", "set to 365"],
        "UNEXPECTED-6a": ["UNEXPECTED-6a", 5.0, "same PK or FK value in 95-100% of rows", "mock values"],
        "UNEXPECTED-6b": ["UNEXPECTED-6b", 5.0, "non-ASCII char in str but ASCII output is required", "set to 'other'"],
        "UNEXPECTED-6c": ["UNEXPECTED-6c", 5.0, "NaN in a float", "set to 0.0"],
        "UNEXPECTED-6d": ["UNEXPECTED-6d", 5.0, "NaN in an int", "set to 0"],
        "NONSTANDARD-7a": ["NONSTANDARD-7a", 3.0, "Spaces in a field name", ""],
        "NONSTANDARD-7b": ["NONSTANDARD-7b", 3.0, "Capitalized column names", ""],
    }
)
