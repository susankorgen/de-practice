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
    obj.get_html_demo(output)
    print()
    print(obj.get_markdown_demo(output))
    print("\nThe above output is the result of Task 1.")
    print("For CSV, Markdown, and HTML versions of the output, see output/DemoDisplay.*\n")
