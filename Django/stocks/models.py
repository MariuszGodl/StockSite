from django.db import models

class StockExchange(models.Model):
    id = models.AutoField(primary_key=True)
    exchangename = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    class Meta:
        db_table = "StockExchange"


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    identifier = models.CharField(max_length=10, unique=True)
    companyname = models.CharField(max_length=100)
    ceo = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    info = models.TextField()
    nrofsheres = models.IntegerField(db_column="NrOfShares") 
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    creationdate = models.DateField()
    destructiondate = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "Company"


class StockExchangeEntering(models.Model):
    stockexchangeid = models.ForeignKey(StockExchange, on_delete=models.CASCADE, db_column="StockExchangeID")
    companyid = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="CompanyID")
    dateofentry = models.DateField()
    dateofexit = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "StockExchangeEntering"
        unique_together = ("stockexchangeid", "companyid")


class DayValue(models.Model):
    id = models.AutoField(primary_key=True)
    companyid = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="CompanyID")
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    min = models.DecimalField(max_digits=10, decimal_places=2)
    max = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    trades = models.IntegerField()
    turnover = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "DayValue"
        unique_together = ("companyid", "date")
