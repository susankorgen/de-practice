import datetime
import os
import random

from control.demo_helpers import safe_positive_int, safe_demo_date, safe_string, safe_int_range
from error import InvalidOutputFile
from io import StringIO
import pandas as pd

from quality.DataQualityIssueReport import report_quality_issue


class PipelineQualityDemo:
    customer_name = "Unknown"
    default_input = "input/demo.csv"
    default_output_csv = "result/PipelineDisplay.csv"
    default_output_md = "result/PipelineDisplay.md"
    default_output_html = "result/PipelineDisplay.html"
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
    default_dqi_csv = "report/QualityDisplay.csv"
    default_dqi_md = "report/QualityDisplay.md"
    default_dqi_html = "report/QualityDisplay.html"

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

    def read_input(self, data_source: str = None) -> pd.DataFrame:
        """This is the READ segment of the data pipeline (1st of 3 segments)"""
        if data_source is None:
            data_source = self.default_input
        demo_input = pd.read_csv(data_source)
        return demo_input

    @staticmethod
    def refine_input(
        avocado_data: pd.DataFrame,
        consumer_data: pd.DataFrame,
        fertilizer_data: pd.DataFrame,
        purchase_data: pd.DataFrame,
    ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
        """This is the REFINE segment of the data pipeline (2nd of 3 segments)

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
        avocado_refined = avocado_data[[
            "avocado_bunch_id",
            "sold_date",
            "born_date",
            "ripe index when picked",
            "picked_date"
        ]]
        avocado_refined["avocado_bunch_id"] = avocado_refined["avocado_bunch_id"].apply(safe_positive_int, pipeline_segment="refine_input", table_name="avocado", field_name="avocado_bunch_id")
        avocado_refined["ripe index when picked"] = avocado_refined["ripe index when picked"].apply(safe_positive_int, pipeline_segment="refine_input", table_name="avocado", field_name="ripe index when picked")
        report_quality_issue("NONSTANDARD-7a", "refine_input", "consumer", "ripe index when picked")

        consumer_refined = consumer_data[["consumerid", "Sex", "Age"]]
        consumer_refined["consumerid"] = consumer_refined["consumerid"].apply(safe_positive_int, pipeline_segment="refine_input", table_name="consumer", field_name="consumerid")
        consumer_refined["Sex"] = consumer_refined["Sex"].apply(safe_string, pipeline_segment="refine_input", table_name="consumer", field_name="Sex")
        consumer_refined["Age"] = consumer_refined["Age"].apply(safe_positive_int, pipeline_segment="refine_input", table_name="consumer", field_name="Age")

        purchase_refined = purchase_data[["purchaseid", "avocado_bunch_id"]]
        purchase_refined["purchaseid"] = purchase_refined["purchaseid"].apply(safe_positive_int, pipeline_segment="refine_input", table_name="purchase", field_name="purchaseid")
        purchase_refined["avocado_bunch_id"] = purchase_refined["avocado_bunch_id"].apply(safe_positive_int, pipeline_segment="refine_input", table_name="purchase", field_name="avocado_bunch_id")

        fertilizer_refined = fertilizer_data[["purchaseid", "fertilizerid", "type"]]
        fertilizer_refined["purchaseid"] = fertilizer_refined["purchaseid"].apply(safe_positive_int, pipeline_segment="refine_input", table_name="fertilizer", field_name="purchaseid")
        fertilizer_refined["type"] = fertilizer_refined["type"].apply(safe_string, pipeline_segment="refine_input", table_name="fertilizer", field_name="type")

        return avocado_refined, consumer_refined, fertilizer_refined, purchase_refined

    def transform(
        self,
        avocado_refined: pd.DataFrame,
        consumer_refined: pd.DataFrame,
        fertilizer_refined: pd.DataFrame,
        purchase_refined: pd.DataFrame,
    ) -> pd.DataFrame:
        """This is the ETL segment of the data pipeline (3rd of 3 segments)"""

        result_list: list[list] = []
        for a, avocado in avocado_refined.iterrows():

            # query
            merged_df = avocado_refined.merge(purchase_refined, on="avocado_bunch_id")
            filtered_df = merged_df[merged_df["avocado_bunch_id"] == avocado["avocado_bunch_id"]]
            merged_df = filtered_df.merge(fertilizer_refined, on="purchaseid")
            select_df = merged_df[["sold_date", "born_date", "picked_date", "ripe index when picked", "type"]]

            # customer: get values from a random consumer row and assign a 12-digit unique ID
            report_quality_issue("BLOCKER-1a", "transform", "consumer", "consumerid")
            report_quality_issue("MISSING-3a", "transform", "consumer", "consumerid")
            random_consumer_index = random.randint(0, len(consumer_refined) - 1)
            consumer_id = random_consumer_index + 100000000001
            consumer_sex = consumer_refined.at[random_consumer_index, "Sex"]
            consumer_age = consumer_refined.at[random_consumer_index, "Age"]
            consumer_age = safe_int_range(consumer_age, min_value=1, max_value=120, pipeline_segment="transform", table_name="consumer", field_name="Age")

                           # avocado: calculate day counts
            (avocado_days_sold, ripe_index, avocado_days_picked) = PipelineQualityDemo.transform_avocado(
                avocado["sold_date"],
                avocado["born_date"],
                avocado["ripe index when picked"],
                avocado["picked_date"]
            )

            # fertilizer: combine the >= 1 values into 1 value
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
        sold_datetime = safe_demo_date(sold_date, default=PipelineQualityDemo.today_date, pipeline_segment="transform", table_name="avocado", field_name="sold_date")
        born_datetime = safe_demo_date(born_date, default=PipelineQualityDemo.today_date, pipeline_segment="transform", table_name="avocado", field_name="born_date")
        ripe_index = safe_int_range(ripe_index, min_value=0, max_value=10, pipeline_segment="transform", table_name="avocado", field_name="ripe index when picked")
        picked_datetime = safe_demo_date(picked_date, default=PipelineQualityDemo.today_date, pipeline_segment="transform", table_name="avocado", field_name="picked_date")
        avocado_days_picked = safe_positive_int((sold_datetime - born_datetime).days, pipeline_segment="transform", table_name="result", field_name="avocado_days_picked")
        avocado_days_sold = safe_positive_int((sold_datetime - picked_datetime).days, pipeline_segment="transform", table_name="result", field_name="avocado_days_sold")
        return avocado_days_sold, ripe_index, avocado_days_picked

    def write_csv(
        self,
        default_output_csv: str,
        demo_data: pd.DataFrame
    ) -> None:
        """
        Does minor validation of the folder and file string, not airtight for all cases.
        To make airtight, would test a regex against the folder and file path string.
        """
        if default_output_csv is None:
            default_output_csv = self.default_output_csv

        # validate result file
        position = default_output_csv.find(".csv")
        if position == -1 or position == 0:
            raise InvalidOutputFile()

        # create result folder from the prefix to the file name
        if 0 < default_output_csv.find("/") < position:
            os.makedirs(name=self.get_folder_path(default_output_csv), exist_ok=True)

        # prepare target file
        created_file = os.path.exists(default_output_csv)
        if created_file:
            os.remove(default_output_csv)

        # write result
        demo_data.to_csv(
            path_or_buf=default_output_csv,  # TODO: target_{iteration}_{date}.csv
            sep="|",
            lineterminator="\n",
            quotechar='"',
            encoding="ascii",
            header=self.output_columns,
        )
