from django.shortcuts import render, get_object_or_404
from .models import Company, DayValue
from datetime import date, timedelta, datetime
import random


def get_random_companies(n_of_companies):
    #get the number of Company objects, and randomly chose n of them
    return list(Company.objects.order_by('?')[:n_of_companies])

def get_day_values(day_values, value_date, company):
    if value_date:
        try:
            value_date_parsed = datetime.strptime(value_date, "%m-%d-%Y").date()
        except ValueError:
            value_date_parsed = None
    else:
        value_date_parsed = None
    # Get the specific DayValue
    if value_date:
        try:
            day_value = DayValue.objects.get(companyid=company, date=value_date)
        except DayValue.DoesNotExist:
            # fallback to latest available day
            day_value = day_values.last()
    else:
        # default: latest available day
        day_value = day_values.last()

    num_objects = day_values.count()

    if value_date:
        try:
            value_date_parsed = datetime.strptime(value_date, "%Y-%m-%d").date()
        except ValueError:
            print('incorrect data format YYYY-MM-DD')

        try:
            day_before_value = DayValue.objects.get(companyid=company, date=value_date_parsed - timedelta(days=1))
        except DayValue.DoesNotExist:
            # fallback to latest available day
            second_last_value = day_values[num_objects - 2] if len(day_values) >= 2 else None
    else:
        # default: latest available day
        day_before_value = day_values[num_objects - 2]
    ratio = f'{(day_value.close / day_before_value.close - 1)* 100:.2f}%' # i need that ass strting in decimal format no matter if it is a whole number like 18.00 %, convert it to procentages as well
    ratio_numeric = day_value.close / day_before_value.close - 1

    return day_value, ratio, ratio_numeric

def company_detail(request, identifier='06MAGNA', value_date=None):
    company = get_object_or_404(Company, identifier=identifier)

    # All historical prices for chart
    day_values = DayValue.objects.filter(companyid=company).order_by("date")

    # Extract dates and closing prices
    chart_labels = [dv.date.strftime("%Y-%m-%d") for dv in day_values]
    chart_data = [float(dv.close) for dv in day_values]
    
    day_value, ratio, ratio_numeric = get_day_values(day_values, value_date, company)
    promote_companies = get_random_companies(3)
    for i in range(len(promote_companies)):
        print(promote_companies[i - 1].identifier)

    capitalization = f"{company.capitalization:,} PLN".replace(',', ' ')
    context = {
        "Company": company,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
        "DayValue": day_value,
        "Ratio": ratio,
        "NrRatio": ratio_numeric,
        "Capitalization": capitalization,
        "PromoteCompanies": promote_companies,
    }
    return render(request, "stocks/company_detail.html", context)



def contact(request):
    context = {

    }
    return render(request, "stocks/contact.html", context)



def about_me(request):
    context = {

    }
    return render(request, "stocks/about_me.html", context)

