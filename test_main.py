
import os
import unittest

from _pytest.python_api import raises

import error
from main import QuickDemo


class TestMain(unittest.TestCase):
    output_to_cleanup:str

    def setUp(self) -> None:
        self.output_to_cleanup = ""

    def tearDown(self) -> None:
        if os.path.exists(self.output_to_cleanup):
            os.remove(self.output_to_cleanup)


    def test_demo_all_defaults_happy(self):
        with open("resource/echo_output.txt", "r") as sample:

            # read input
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo()

            # write output
            test_target = obj.default_output
            assert os.path.exists(test_target) is False
            display_content = obj.write_demo(demo_data=demo_data)
            assert sample.read() == display_content
            assert os.path.exists(test_target) is True

            # clean up
            self.output_to_cleanup = test_target

    def test_demo_good_input_file_name(self):  # ?
        with open("resource/echo_output.txt", "r") as sample:

            # read input
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo(data_source="input/DemoSample.csv")

            # write output
            test_target = obj.default_output
            assert os.path.exists(test_target) is False
            display_content = obj.write_demo(demo_data=demo_data)
            assert sample.read() == display_content
            assert os.path.exists(test_target) is True

            # clean up
            self.output_to_cleanup = test_target

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
            test_target = "output/DemoDeleteMe.csv"
            assert os.path.exists(test_target) is False
            display_content = obj.write_demo(demo_data=demo_data, display_target=test_target)
            assert sample.read() == display_content
            assert os.path.exists(test_target) is True

            # clean up
            self.output_to_cleanup = test_target

    def test_good_simple_output_file_name(self):
        with open("resource/echo_output.txt", "r") as sample:
            # read input
            obj = QuickDemo("Customer")
            demo_data = obj.run_demo(data_source="input/DemoSample.csv")

            # write output
            test_target = "./DemoDeleteMe.csv"
            assert os.path.exists(test_target) is False
            display_content = obj.write_demo(demo_data=demo_data, display_target=test_target)
            assert sample.read() == display_content
            assert os.path.exists(test_target) is True

            # clean up
            self.output_to_cleanup = test_target

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
        test_target = obj.default_output
        assert os.path.exists(test_target) is False
        obj.write_demo(demo_data=demo_data)

        # overwrite second time
        assert os.path.exists(test_target) is True
        obj.write_demo(demo_data=demo_data)
        assert os.path.exists(test_target) is True

        # clean up
        self.output_to_cleanup = test_target
