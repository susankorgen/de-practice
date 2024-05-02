from control.demo_helpers import get_markdown_demo, get_html_demo
from control.etl_demo import ETLDemo
from control.pipeline_quality_demo import PipelineQualityDemo
from control.quick_demo import QuickDemo
import pandas as pd


def quick_demo():
    # init
    obj = QuickDemo()

    # get the data
    demo_data = obj.read_input()

    # transform
    output = obj.transform(demo_data)

    # write the output
    obj.write_demo(output)
    get_html_demo(obj.default_output_html, output)
    print()
    print(get_markdown_demo(obj.default_output_md, output))
    print("\nThe above output is the result of Task 1.")
    print("For CSV, Markdown, and HTML versions of the output, see output/DemoDisplay.*\n")


def etl_demo():
    # init
    pd.set_option("mode.copy_on_write", True)
    obj = ETLDemo()

    # read the data
    avocado_data = obj.read_input("input/avocado.csv")
    consumer_data = obj.read_input("input/consumer.csv")
    fertilizer_data = obj.read_input("input/fertilizer.csv")
    purchase_data = obj.read_input("input/purchase.csv")

    # refine the data
    (avocado_refined, consumer_refined, fertilizer_refined, purchase_refined) = obj.refine_input(
        avocado_data,
        consumer_data,
        fertilizer_data,
        purchase_data
    )

    # transform the data
    result_table = obj.transform(
        avocado_refined,
        consumer_refined,
        fertilizer_refined,
        purchase_refined
    )

    # write the result
    obj.write_demo(result_table)
    get_html_demo(obj.default_output_html, result_table)
    print()
    print(get_markdown_demo(obj.default_output_md, result_table))
    print("\nThe above output is the result of Task 2, Part 1 ETL")
    print("For CSV, Markdown, and HTML versions of the output, see output/ETLDisplay.*\n")


def pipeline_quality_demo():
    # init
    pd.set_option("mode.copy_on_write", True)
    obj = PipelineQualityDemo()

    # read the data
    avocado_data = obj.read_input("input/avocado.csv")
    consumer_data = obj.read_input("input/consumer.csv")
    fertilizer_data = obj.read_input("input/fertilizer.csv")
    purchase_data = obj.read_input("input/purchase.csv")

    # refine the data
    (avocado_refined, consumer_refined, fertilizer_refined, purchase_refined) = obj.refine_input(
        avocado_data,
        consumer_data,
        fertilizer_data,
        purchase_data
    )

    # transform the data
    result_table = obj.transform(
        avocado_refined,
        consumer_refined,
        fertilizer_refined,
        purchase_refined
    )

    # write the result
    obj.write_demo(result_table)
    get_html_demo(obj.default_output_html, result_table)
    print()
    print(get_markdown_demo(obj.default_output_md, result_table))
    print("\nThe above output is the result of Task 2, Part 1 ETL")
    print("For CSV, Markdown, and HTML versions of the output, see output/ETLDisplay.*\n")

    # write the DQI report
    # TODO: implement
    print()
    print("To be supplied")
    print("\nThe above output is the result of Task 2, Part 2 Data Quality")
    print("For CSV, Markdown, and HTML versions of the output, see output/DQIDisplay.*\n")


if __name__ == "__main__":
    # Task 1
    quick_demo()

    # Task 2 ETL
    etl_demo()

    # Task 2 Pipeline
    pipeline_quality_demo()
