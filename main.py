from control.demo_helpers import get_markdown_demo, get_html_demo
from control.etl_demo import ETLDemo
from control.quick_demo import QuickDemo


def quick_demo():
    # init
    obj = QuickDemo()

    # get the data
    demo_data = obj.get_demo_input()

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
    obj = ETLDemo()

    # get the data
    demo_data = obj.get_demo_input()

    # transform
    output = obj.transform(demo_data)

    # write the output
    obj.write_demo(output)
    get_html_demo(obj.default_output_html, output)
    print()
    print(get_markdown_demo(obj.default_output_md, output))
    print("\nThe above output is the result of Task 1.")
    print("For CSV, Markdown, and HTML versions of the output, see output/ETLDisplay.*\n")


def pipeline_demo():
    """Stub"""
    pass


if __name__ == "__main__":
    # Task 1
    # quick_demo()

    # Task 2 ETL
    etl_demo()

    # Task 2 Pipeline
    # pipeline_demo()
