
import os

from _pytest.python_api import raises

import error
from main import QuickDemo


class TestMain:

    def test_demo_all_defaults_happy(self):
        with open("resource/echo_output.txt", "r") as sample:
            # read input
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo()

            # write output
            assert os.path.exists(obj.default_output) is False
            display_content = obj.write_demo(demo_data=demo_data)
            assert sample.read() == display_content

            # check output, then clean up
            created_file = os.path.exists(obj.default_output)
            assert created_file is True
            if created_file:
                os.remove(obj.default_output)
            assert os.path.exists(obj.default_output) is False

    def test_demo_good_input_file_name(self):  # ?
        with open("resource/echo_output.txt", "r") as sample:
            # read input
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo(data_source="input/DemoSample.csv")

            # write output
            assert os.path.exists(obj.default_output) is False
            display_content = obj.write_demo(demo_data=demo_data)
            assert sample.read() == display_content

            # check output, then clean up
            created_file = os.path.exists(obj.default_output)
            assert created_file is True
            if created_file:
                os.remove(obj.default_output)
            assert os.path.exists(obj.default_output) is False

    def test_demo_bad_input_file_name(self):
        with open("resource/echo_output.txt", "r") as sample:
            obj = QuickDemo("Customer")
            with raises(FileNotFoundError) as e:
                obj.run_demo(data_source="DemoSample.csv")
            assert "DemoSample.csv" == e.value.filename

    def test_good_output_file_name(self):
        with open("resource/echo_output.txt", "r") as sample:
            # read input
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo(data_source="input/DemoSample.csv")

            # write output
            assert os.path.exists("output/DemoDeleteMe.csv") is False
            display_content = obj.write_demo(demo_data=demo_data, display_target="output/DemoDeleteMe.csv")
            assert sample.read() == display_content

            # check output, then clean up
            created_file = os.path.exists("output/DemoDeleteMe.csv")
            assert created_file is True
            if created_file:
                os.remove("output/DemoDeleteMe.csv")
            assert os.path.exists("output/DemoDeleteMe.csv") is False

    def test_good_simple_output_file_name(self):
        with open("resource/echo_output.txt", "r") as sample:
            # read input
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo(data_source="input/DemoSample.csv")

            # write output
            assert os.path.exists("./DemoDeleteMe.csv") is False
            display_content = obj.write_demo(demo_data=demo_data, display_target="DemoDeleteMe.csv")
            assert sample.read() == display_content

            # check output, then clean up
            created_file = os.path.exists("./DemoDeleteMe.csv")
            assert created_file is True
            if created_file:
                os.remove("./DemoDeleteMe.csv")
            assert os.path.exists("./DemoDeleteMe.csv") is False

    def test_bad_output_file_name_case_0(self):
        with open("resource/echo_output.txt", "r") as sample:
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo(data_source="input/DemoSample.csv")
            with raises(error.InvalidOutputFile) as e:
                obj.write_demo(demo_data=demo_data, display_target=".csv")
            assert "An invalid CSV output filename or folder was provided" == e.value.message

    def test_bad_output_file_name_case_minus_1(self):
        with open("resource/echo_output.txt", "r") as sample:
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo(data_source="input/DemoSample.csv")
            with raises(error.InvalidOutputFile) as e:
                obj.write_demo(demo_data=demo_data, display_target="DemoDeleteMe.pdf")
            assert "An invalid CSV output filename or folder was provided" == e.value.message

    def test_demo_all_defaults_overwrite_output_happy(self):
        # read input
        obj = QuickDemo("Customer")
        demo_data = obj.run_demo()

        # write first time
        assert os.path.exists(obj.default_output) is False
        obj.write_demo(demo_data=demo_data)

        # overwrite second time
        assert os.path.exists(obj.default_output) is True
        obj.write_demo(demo_data=demo_data)

        # now clean up
        created_file = os.path.exists(obj.default_output)
        assert created_file is True
        if created_file:
            os.remove(obj.default_output)
        assert os.path.exists(obj.default_output) is False