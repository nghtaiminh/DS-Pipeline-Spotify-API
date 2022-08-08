from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.papermill_operator import PapermillOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 4, 1),
    'depends_on_past': False,
    'email_on_past': 'airflow@example.com',
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retries_delay': timedelta(minutes=5)

}

with DAG(
    'spotify_data_extraction',
    default_args = default_args,
    description = 'Data extraction and transformation from Spotify API',
    schedule_interval='@daily',
) as dag:
    t1 = PapermillOperator(
        task_id="run_data_extraction_notebook",
        input_nb="path_to_your_notebook/SpotifyDataExtraction.ipynb",
        output_nb="path_to_your_temp_folder/tmp/out-{{ execution_date }}.ipynb",
        parameters={"msgs": "Ran from Airflow at {{ execution_date }}!"}
    )

    # Run the dag
    t1 

