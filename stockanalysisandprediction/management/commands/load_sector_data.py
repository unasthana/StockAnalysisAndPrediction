import os
import pandas as pd
from django.core.management.base import BaseCommand
from stockanalysisandprediction.models import Stock, CompanyInfo


class Command(BaseCommand):
    help = "Load sector csv file into the database"

    def handle(self, *args, **kwargs):
        if not CompanyInfo.objects.exists():
            data = pd.read_csv(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "sector_data.csv"
                )
            )
            data.dropna(inplace=True)
            for _, row in data.iterrows():
                CompanyInfo.objects.get_or_create(
                    ticker=row["Name"], sector=row["Sector"]
                )
            self.stdout.write(
                self.style.SUCCESS("Successfully loaded stock sector data")
            )
