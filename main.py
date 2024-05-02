from control.demo_helpers import get_markdown, write_html
from control.etl_demo import ETLDemo
from control.pipeline_quality_demo import PipelineQualityDemo
from control.quick_demo import QuickDemo
import pandas as pd

from quality.DataQualityIssueReport import data_quality_issue_report, refine_data_quality_issue_report


def quick_demo():
    """
    DEPRECATED.
    Retain to support unit tests.
    Use pipeline_quality_demo() instead.
    Task 1 demo. Predates etl_demo() and pipeline_quality_demo().
    Subset of pipeline_quality_demo() functionality.
    """
    # init
    demo = QuickDemo()

    # get the data
    demo_data = demo.read_input()

    # transform
    output = demo.transform(demo_data)

    # write the result
    demo.write_demo(output)
    write_html(demo.default_output_html, output)
    print()
    print(get_markdown(demo.default_output_md, output))
    print("\nThe above result is the result of Task 1.")
    print("For CSV, Markdown, and HTML versions of the result, see result/DemoDisplay.*\n")


def etl_demo():
    """
    DEPRECATED.
    Use pipeline_quality_demo() instead.
    Task 2 ETL demo. Subset of pipeline_quality_demo() functionality. Do not use."""
    # init
    pd.set_option("mode.copy_on_write", True)
    demo = ETLDemo()

    # read the data
    avocado_data = demo.read_input("input/avocado.csv")
    consumer_data = demo.read_input("input/consumer.csv")
    fertilizer_data = demo.read_input("input/fertilizer.csv")
    purchase_data = demo.read_input("input/purchase.csv")

    # refine the data
    (avocado_refined, consumer_refined, fertilizer_refined, purchase_refined) = demo.refine_input(
        avocado_data,
        consumer_data,
        fertilizer_data,
        purchase_data
    )

    # transform the data
    result_table = demo.transform(
        avocado_refined,
        consumer_refined,
        fertilizer_refined,
        purchase_refined
    )

    # write the result
    demo.write_demo(result_table)
    write_html(demo.default_output_html, result_table)
    print()
    print(get_markdown(demo.default_output_md, result_table))
    print("\nThe above result is the result of Task 2, Part 1 ETL")
    print("For CSV, Markdown, and HTML versions of the result, see result/ETLDisplay.*\n")


def pipeline_quality_demo():
    """
    Task 2 demo of pipeline and Data Quality Issue report.
    Superset of etl_demo() functionality.
    """
    # init
    pd.set_option("mode.copy_on_write", True)
    demo = PipelineQualityDemo()

    # read the data
    avocado_data = demo.read_input("input/avocado.csv")
    consumer_data = demo.read_input("input/consumer.csv")
    fertilizer_data = demo.read_input("input/fertilizer.csv")
    purchase_data = demo.read_input("input/purchase.csv")

    # refine the data
    (avocado_refined, consumer_refined, fertilizer_refined, purchase_refined) = demo.refine_input(
        avocado_data,
        consumer_data,
        fertilizer_data,
        purchase_data
    )

    # transform the data
    result_table = demo.transform(
        avocado_refined,
        consumer_refined,
        fertilizer_refined,
        purchase_refined
    )

    # write the result
    demo.write_csv(demo.default_output_csv, result_table)
    write_html(demo.default_output_html, result_table)
    print()
    print(get_markdown(demo.default_output_md, result_table))
    print("\nThe above result is the result of Task 2, Part 1 ETL")
    print("For CSV, Markdown, and HTML versions of the result, see result/PipelineDisplay.*\n")

    # write the DQI report
    dqi_report = refine_data_quality_issue_report()
    demo.write_csv(demo.default_dqi_csv, dqi_report)
    write_html(demo.default_dqi_html, dqi_report)
    print()
    print(get_markdown(demo.default_dqi_md, dqi_report))
    print("\nThe above result is the result of Task 2, Part 2 Data Quality")
    print("For CSV, Markdown, and HTML versions of the result, see result/QualityDisplay.*\n")


if __name__ == "__main__":
    pipeline_quality_demo()
