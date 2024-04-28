import pytest

from main import QuickDemo


class TestMain:

    def test_run_demo(self):
        with open("./resource/echo_output.txt", "r") as sample:
            obj = QuickDemo("Customer")
            output = obj.run_demo(
                customer_name="Customer",
                data_source="../input/DemoSample.csv"
            )
            assert sample.read() == output

