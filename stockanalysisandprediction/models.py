from django.db import models


class Stock(models.Model):
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.date}"


class CompanyInfo(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ticker} - {self.company_name} - {self.sector}"


class APICache(models.Model):
    api_name = models.CharField(max_length=100)
    params = models.TextField()  # JSON string of parameters
    response = models.JSONField()
