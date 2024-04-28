import os

from error import InvalidOutputFile
from io import StringIO
from os import makedirs
import pandas as pd

class QuickDemo():
    customer_name = "Unknown"
    default_input = "input/DemoSample.csv"
    default_output = "output/DemoDisplay.csv"

    def __init__(self, customer_name):
        # self.name = customer_name
        self.customer_name = customer_name

    @staticmethod
    def get_df_string(df: pd.DataFrame) -> str:
        string_buffer: StringIO = StringIO()
        df.info(buf=string_buffer)
        return string_buffer.getvalue()

    def run_demo(self, data_source: str = None) -> pd.DataFrame:
        if data_source is None:
            data_source = self.default_input
        return pd.read_csv(data_source)

    def write_demo(
        self,
        demo_data: pd.DataFrame,
        display_target: str = None
    ) -> str:
        """
        Demo simple validation of the folder and file string, not airtight for all cases.
        Could do a regex test for folder and file path string.
        """
        if display_target is None:
            display_target = self.default_output

        # validate output file
        position = display_target.find(".csv")
        if position == -1 or position == 0:
            raise InvalidOutputFile()

        # create output folder from the prefix to the file name
        if 0 < display_target.find("/") < position:
            folder_path = "/".join(display_target.split("/")[:-1])
            makedirs(name=folder_path, exist_ok=True)

        # write output to file
        created_file = os.path.exists(display_target)
        if created_file:
            os.remove(display_target)
        demo_data.to_csv(display_target)

        # return display text
        output = []
        output.append(f"\nHello, {self.customer_name}!\n")
        output.append("\ndata frame: first few rows:")
        output.append(self.get_df_string(demo_data.head()))
        output.append("\n")
        return "".join(output)


if __name__ == "__main__":
    customer_name = input("Hello customer, what is your company name? ")
    obj = QuickDemo(customer_name)
    demo_data = obj.run_demo()
    display_content = obj.write_demo(demo_data)
