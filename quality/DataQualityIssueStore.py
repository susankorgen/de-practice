
# Data value quality issues are discoverable during daily processing.
# This global value holds definitions of data quality issues for the pipeline.
#
# Each member of the data_quality_issue_store dictionary is a list:
# name,
# severity,
# description
# demo_workaround
#
# example:   ["BLOCKER-1a", 50.0, "PK is not unique in table", "Mock values"]
#
data_quality_issue_store: dict = dict(
    {
        "UNKNOWN": ["UNKNOWN", 0.0, "Invalid issue key in issue report", "ignore"],
        "BLOCKER-1a": ["BLOCKER-1a", 50.0, "PK is not unique in table", "mock values"],
        "BLOCKER-1b": ["BLOCKER-1b", 40.0, "Missing value for a field that is NOT NULLABLE (PKs and FKs)", "skip row"],
        "MISSING-2a": ["MISSING-2a", 28.0, "Missing value for a field that is NOT NULLABLE (PKs and FKs)", "skip row"],
        "MISSING-3a": ["MISSING-3a", 25.0, "Missing value for a field required for analysis", "choose random row from real data"],
        "MISSING-3b": ["MISSING-3b", 23.0, "Missing value for a date field needed for analysis", "set to today"],
        "MISSING-3c": ["MISSING-3c", 20.0, "Missing value for a 0-10 int needed for analysis", "set to 0"],
        "DATATYPE-4a": ["DATATYPE-4a", 15.0, "Inconsistent date format values", "strip time off the date strings"],
        "DATATYPE-4b": ["DATATYPE-4b", 13.0, "Inappropriate data type for identifier (float)", "convert to int"],
        "DATATYPE-4c": ["DATATYPE-4c", 10.0, "Date value that is non-empty but not parseable as a date", "use empty"],
        "RANGE-5a": ["RANGE-5a", 8.0, "Value too low, out of range", "set to minimum in range"],
        "RANGE-5b": ["RANGE-5b", 7.5, "Value too high, out of range", "set to maximum in range"],
        "RANGE-5c": ["RANGE-5c", 7.0, "Dates in the future as of today", "set to today"],
        "UNEXPECTED-6a": ["UNEXPECTED-6a", 5.0, "same PK or FK value in 95-100% of rows", "mock values"],
        "UNEXPECTED-6b": ["UNEXPECTED-6b", 4.75, "non-ASCII char in str but ASCII output is required", "set to 'other'"],
        "UNEXPECTED-6c": ["UNEXPECTED-6c", 4.50, "NaN in a number", "set to 0"],
        "UNEXPECTED-6d": ["UNEXPECTED-6d", 4.25, "Empty number value,  could not cast to str", "use 'Empty'"],
        "UNEXPECTED-6e": ["UNEXPECTED-6e", 4.12, "Invalid number value, could not cast to str", "use 'Unknown'"],
        "UNEXPECTED-6f": ["UNEXPECTED-6f", 4.0, "Empty string where a date should be", "may use empty, or today"],
        "UNEXPECTED-6g": ["UNEXPECTED-6g", 3.14159, "Invalid string where a date should be", "may use empty, or today"],
        "NONSTANDARD-7a": ["NONSTANDARD-7a", 2.0, "Spaces in a field name", ""],
        "NONSTANDARD-7b": ["NONSTANDARD-7b", 1.0, "Capitalized column name", ""],
    }
)
