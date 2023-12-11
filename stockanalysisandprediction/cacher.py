import requests
from time import sleep


def call_getRankingsApi(analytic_list, time_list, ma_analytic_list, ma_window_list):
    base_url = "http://127.0.0.1:8000/api/getRankingsApi"
    timeout = 300

    for analytic in analytic_list:
        for time in time_list:
            for ma_analytic in ma_analytic_list:
                for ma_window in ma_window_list:
                    params = {
                        "analytic": analytic,
                        "time": time,
                        "ma_analytic": ma_analytic,
                        "ma_window": ma_window,
                    }

                    try:
                        response = requests.get(
                            base_url, params=params, timeout=timeout
                        )
                        if response.status_code == 200:
                            print(f"Response for {analytic}: {response.json()}")
                        else:
                            print(f"Error for {analytic}: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"Request failed for {analytic}: {e}")

                    sleep(1)


analytic_list = ["analytic1", "analytic2", "analytic3"]
time_list = ["all_time"]
ma_analytic_list = []
ma_window_list = []
call_getRankingsApi(analytic_list, time_list, ma_analytic_list, ma_window_list)
