import requests
from time import sleep

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Cache long running apis"

    def handle(self, *args, **kwargs):
        def cache_clustering(time_list):
            base_url = "http://127.0.0.1:8000/api/makeCluster/"
            timeout = 300

            for time in time_list:
                params = {
                    "time": time,
                }
                try:
                    response = requests.get(base_url, params=params, timeout=timeout)
                    if response.status_code == 200:
                        print(f"Response for {time}: {response.json()}")
                    else:
                        print(
                            f"Error for {time}: {response.status_code} {response.text}"
                        )
                except requests.exceptions.RequestException as e:
                    print(f"Request failed for {time}: {e}")

                sleep(1)

        time_list = [
            "all_time",
            "1_week",
            "2_weeks",
            "1_month",
            "1_quarter",
            "6_months",
            "1_year",
        ]
        # cache_clustering(time_list)

        def cache_rankings(analytic_list, time_list, ma_analytic_list, ma_window_list):
            base_url = lambda x: f"http://127.0.0.1:8000/api/getRankings/{x}/"
            timeout = 1000

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
                                    base_url(analytic), params=params, timeout=timeout
                                )
                                if response.status_code == 200:
                                    print(f"Response for {analytic}: {response.json()}")
                                else:
                                    print(
                                        f"Error for {analytic} {time} {ma_analytic} {ma_window}: {response.status_code}"
                                    )
                            except requests.exceptions.RequestException as e:
                                print(f"Request failed for {analytic}: {e}")

                            sleep(1)

        analytic_list = [
            "daily_returns",
            "daily_price_change",
            "daily_price_gap",
            "yearly_performance",
            "daily_price_range",
        ]
        ma_analytic_list = [
            "NA",
            "daily_returns",
            "daily_price_change",
            "daily_price_gap",
            "daily_price_gap",
            "yearly_performance",
            "daily_price_range",
        ]
        ma_window_list = ["NA", "3_day", "5_day", "10_day", "30_day", "60_day"]
        cache_rankings(analytic_list, time_list, ma_analytic_list, ma_window_list)

        def cache_correlations(
            analytic_list, time_list, ma_analytic_list, ma_window_list
        ):
            base_url = (
                lambda x, y: f"http://127.0.0.1:8000/api/getCorrelationAnalytics/{x}/{y}/"
            )
            timeout = 1000

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
                                    base_url(analytic), params=params, timeout=timeout
                                )
                                if response.status_code == 200:
                                    print(f"Response for {analytic}: {response.json()}")
                                else:
                                    print(
                                        f"Error for {analytic} {time} {ma_analytic} {ma_window}: {response.status_code}"
                                    )
                            except requests.exceptions.RequestException as e:
                                print(f"Request failed for {analytic}: {e}")

                            sleep(1)

        cache_correlations(analytic_list, time_list, ma_analytic_list, ma_window_list)
