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
