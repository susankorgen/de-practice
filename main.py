import io
from io import StringIO

import pandas as pd


class QuickDemo:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_df_string(df: pd.DataFrame) -> str:
        string_buffer: StringIO = io.StringIO()
        df.info(buf=string_buffer)
        return string_buffer.getvalue()

    @classmethod
    def run_demo(
        cls,
        customer_name: str = "Customer",
        data_source: str = "input/DemoSample.csv"
    ) -> str:
        # get data
        df = pd.read_csv(data_source)
        # write output
        output: list[str] = []
        output.append(f"\nHello, {customer_name}!\n")
        output.append("\ndata frame: first few rows:")
        output.append(cls.get_df_string(df.head()))
        output.append("\n")

        # done
        return "".join(output)


if __name__ == "__main__":
    name = input("Hello customer, what is your company name? ")
    obj = QuickDemo(name)
    obj.run_demo()