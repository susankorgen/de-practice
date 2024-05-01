import datetime
import os
import random

from control.demo_helpers import safe_number_string, \
    get_random_gender, get_random_age, safe_int, \
    safe_demo_date, get_random_fertilizer, safe_string
from error import InvalidOutputFile
from io import StringIO
import pandas as pd


class ETLDemo:
    customer_name = "Unknown"
    default_input = "input/DemoSample.csv"
    default_output_csv = "output/ETLDisplay.csv"
    default_output_md = "output/ETLDisplay.md"
    default_output_html = "output/ETLDisplay.html"
    output_columns = [
        "consumer_id",
        "Sex",
        "age",
        "avocado_days_sold",
        "ripe_index",
        "avocado_days_picked",
        "fertilizer_type"
    ]
    today_date = datetime.datetime(year=2024, month=4, day=30)  # see demo_helpers.safe_demo_date()
    mock_random_index = -1

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
        demo_input = pd.read_csv(data_source)
        return demo_input


    def refine_input(
            self,
            avocado_data: pd.DataFrame,
            consumer_data: pd.DataFrame,
            fertilizer_data: pd.DataFrame,
            purchase_data: pd.DataFrame,
    ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """
        For each avocado row in the daily load, logic is similar to
        the following SQL (with input parameter row_id):
        ```
        select
            a.sold_date,
            a.born_date,
            a.picked_date,
            a."ripe index when picked",
            f.fertilizerid
            f.type,
        from avocado as a
            join purchase as p on a.avocado_bunch_id = p.avocado_bunch_id
            join fertilizer as f on p.purchaseid = f.purchaseid
        where avocado.avocado_bunch_id = :row_id
        ```
        We are not selecting any consumer column values in this query.
        The consumerid data in the sample CSV files is so suspect that for demo purposes,
        we are simulating the needed consumer data by selecting a consumer row at random.
        """
        avocado_refined = avocado_data[["avocado_bunch_id", "sold_date", "born_date", "ripe index when picked", "picked_date"]]
        avocado_refined["avocado_bunch_id"] = avocado_refined["avocado_bunch_id"].apply(safe_int)

        # avocado_refined["ripe index when picked"] = avocado_refined["ripe index when picked"].apply(safe_int)

        consumer_refined = consumer_data[["consumerid", "Sex", "Age"]]
        consumer_refined["consumerid"] = consumer_refined["consumerid"].apply(safe_int)
        consumer_refined["Sex"] = consumer_refined["Sex"].apply(safe_string)
        consumer_refined["Age"] = consumer_refined["Age"].apply(safe_int)

        purchase_refined = purchase_data[["purchaseid", "avocado_bunch_id"]]
        purchase_refined["purchaseid"] = purchase_refined["purchaseid"].apply(safe_int)
        purchase_refined["avocado_bunch_id"] = purchase_refined["avocado_bunch_id"].apply(safe_int)

        fertilizer_refined = fertilizer_data[["purchaseid", "fertilizerid", "type"]]
        fertilizer_refined["purchaseid"] = fertilizer_refined["purchaseid"].apply(safe_int)
        fertilizer_refined["type"] = fertilizer_refined["type"].apply(safe_string)

        return avocado_refined, consumer_refined, fertilizer_refined, purchase_refined

    def transform(
        self,
        avocado_refined: pd.DataFrame,
        consumer_refined: pd.DataFrame,
        fertilizer_refined: pd.DataFrame,
        purchase_refined: pd.DataFrame,
    ) -> pd.DataFrame:

        result_list: list[list] = []
        for a, avocado in avocado_refined.iterrows():

            # query
            merged_df = avocado_refined.merge(purchase_refined, on="avocado_bunch_id")
            filtered_df = merged_df[merged_df["avocado_bunch_id"] == avocado["avocado_bunch_id"]]
            merged_df = filtered_df.merge(fertilizer_refined, on="purchaseid")
            select_df = merged_df[["sold_date", "born_date", "picked_date", "ripe index when picked", "type"]]

            # customer: get values from a random consumer row and assign a 12-digit unique ID
            # TODO: self.transform_consumer()
            random_consumer_index = random.randint(0, len(consumer_refined) - 1)
            consumer_id = random_consumer_index + 100000000001  # workaround for demo for bad PKs
            consumer_sex = consumer_refined.at[random_consumer_index, "Sex"]

            consumer_age = consumer_refined.at[random_consumer_index, "Age"]

            # avocado: calculate day counts
            (avocado_days_sold, ripe_index, avocado_days_picked) = ETLDemo.transform_avocado(
                avocado["sold_date"],
                avocado["born_date"],
                avocado["ripe index when picked"],
                avocado["picked_date"]
            )

            # fertilizer: combine the >= 1 values into 1 value
            # TODO: self.transform_consumer()
            fertilizer_type = ", ".join(select_df["type"].unique())
            new_row = [
                consumer_id,
                consumer_sex,
                consumer_age,
                avocado_days_sold,
                ripe_index,
                avocado_days_picked,
                fertilizer_type
            ]

            # all results
            result_list.append(new_row)

        return pd.DataFrame(result_list, columns=self.output_columns)

    @staticmethod
    def transform_avocado(sold_date, born_date, ripe_index, picked_date: str) -> (int, int, int):
        # TODO: check values for DQI, log issues
        sold_datetime = safe_demo_date(sold_date, default=ETLDemo.today_date)
        born_datetime = safe_demo_date(born_date, default=ETLDemo.today_date)
        ripe_index = safe_int(ripe_index)
        picked_datetime = safe_demo_date(picked_date, default=ETLDemo.today_date)
        avocado_days_picked = safe_int((sold_datetime - born_datetime).days)
        avocado_days_sold = safe_int((sold_datetime - picked_datetime).days)
        return avocado_days_sold, ripe_index, avocado_days_picked

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
