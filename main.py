from control.demo_helpers import get_markdown_demo, get_html_demo
from control.quick_demo import QuickDemo


if __name__ == "__main__":
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
