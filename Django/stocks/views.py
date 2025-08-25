from django.shortcuts import render, get_object_or_404
from .models import Company, DayValue
from datetime import date, timedelta

def company_detail(request, identifier='06MAGNA', value_date=None):
    """
    Show company detail and DayValue for a specific date.
    If value_date is None, show the latest (or 2 days ago).
    """
    company = get_object_or_404(Company, identifier=identifier)
    print(company.companyname)
    # Default date = 2 days ago if not provided
    if value_date is None:
        value_date = date.today() - timedelta(days=70)

    else:
        # Convert string from URL to date object
        value_date = date.fromisoformat(value_date)

    print(value_date)
    day_value = get_object_or_404(DayValue, companyid=company, date=value_date)
    context = {
        "Company": company,
        "DayValue": day_value
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

