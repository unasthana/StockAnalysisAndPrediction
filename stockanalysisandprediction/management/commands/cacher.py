import requests
from time import sleep

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Cache long running apis"

    def handle(self, *args, **kwargs):
        def cache_rankings(analytic_list, time_list, ma_analytic_list, ma_window_list):
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
                                    print(
                                        f"Error for {analytic}: {response.status_code}"
                                    )
                            except requests.exceptions.RequestException as e:
                                print(f"Request failed for {analytic}: {e}")

                        sleep(1)

        analytic_list = ["daily_returns", "daily_price_change", "daily_price_gap"]
        time_list = [
            "all_time",
            "1_week",
            "2_week",
            "1_month",
            "1_quarter",
            "6_months",
            "1_year",
        ]
        ma_analytic_list = ["daily_returns", "daily_price_change", "daily_price_gap"]
        ma_window_list = ["3_day", "5_day", "10_day", "30_day", "60_day"]
        cache_rankings(analytic_list, time_list, ma_analytic_list, ma_window_list)
