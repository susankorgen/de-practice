import datetime
import os

from control.helpers import safe_number_string, \
    get_random_gender, get_random_age, safe_int, \
    safe_demo_date, get_random_fertilizer
from error import InvalidOutputFile
from io import StringIO
import pandas as pd


class QuickDemo:
    customer_name = "Unknown"
    default_input = "input/DemoSample.csv"
    default_output_csv = "output/DemoDisplay.csv"
    default_output_md = "output/DemoDisplay.md"
    default_output_html = "output/DemoDisplay.html"
    output_columns = [
        "consumer_id",
        "Sex",
        "age",
        "avocado_days_sold",
        "ripe_index",
        "avocado_days_picked",
        "fertilizer_type"
    ]
    today_date = datetime.datetime.today()

    @staticmethod
    def get_df_string(df: pd.DataFrame) -> str:
        string_buffer: StringIO = StringIO()
        df.info(buf=string_buffer)
        return string_buffer.getvalue()

    @staticmethod
    def get_folder_path(path: str) -> str:
        if path.find("/") > 0:
            return "/".join(path.split("/")[:-1])
        else:
            return ""

    def get_demo_input(self, data_source: str = None) -> pd.DataFrame:
        if data_source is None:
            data_source = self.default_input
        return pd.read_csv(data_source)

    def transform(self, demo_data: pd.DataFrame) -> pd.DataFrame:
        result = []
        for index, row in demo_data.iterrows():
            result.append(self.etl_input_1_to_output_1(
                row["consumerid"],
                row["avocado_bunch_id"],
                row["price_index"],
                row["graphed_date"]
            )
            )
        return pd.DataFrame(result, columns=self.output_columns)

    def etl_input_1_to_output_1(
            self,
            consumerid,
            avocado_bunch_id,
            price_index,
            graphed_date
    ) -> list:
        consumer_id = safe_number_string(consumerid)
        sex = get_random_gender()
        age = get_random_age()
        avocado_ripe_index = safe_int(price_index)
        past_date = safe_demo_date(input_string=graphed_date, default=self.today_date, offset=25)
        avocado_days_picked = safe_int((self.today_date - past_date).days)
        avocado_days_sold = safe_int(avocado_days_picked + avocado_bunch_id)
        fertilizer_type = get_random_fertilizer()

        return [
            consumer_id,
            sex,
            age,
            avocado_days_sold,
            avocado_ripe_index,
            avocado_days_picked,
            fertilizer_type
        ]

    def write_demo(
        self,
        demo_data: pd.DataFrame,
        display_target: str = None
    ) -> None:
        """
        Demo simple validation of the folder and file string, not airtight for all cases.
        To make airtight, would test a regex for folder and file path string before using it.
        todo: write_demo() caller needs to format display_target as target_{iteration}_{date}.csv
        """
        if display_target is None:
            display_target = self.default_output_csv

        # validate output file
        position = display_target.find(".csv")
        if position == -1 or position == 0:
            raise InvalidOutputFile()

        # create output folder from the prefix to the file name
        if 0 < display_target.find("/") < position:
            os.makedirs(name=self.get_folder_path(display_target), exist_ok=True)

        # prepare target file
        created_file = os.path.exists(display_target)
        if created_file:
            os.remove(display_target)

        # write output
        demo_data.to_csv(
            path_or_buf=display_target,  # todo: target_{iteration}_{date}.csv
            sep="|",
            lineterminator="\n",
            quotechar='"',
            encoding="ascii",
            header=self.output_columns,
        )

    def get_markdown_demo(self, demo_data: pd.DataFrame) -> str:
        demo_data.to_markdown(buf=self.default_output_md)
        buffer = StringIO()
        demo_data.to_markdown(buf=buffer)
        buffer.seek(0)
        return buffer.read()

    def get_html_demo(self, demo_data: pd.DataFrame) -> None:
        demo_data.to_html(buf=self.default_output_html)
