from django.shortcuts import render
from subscriptions.models import SubscriptionPrice
from django.urls import reverse

# Create your views here.
def subscription_price_view(request, interval ="month"):
    qs = SubscriptionPrice.objects.filter(featured= True)
    inv_mo =  SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr =  SubscriptionPrice.IntervalChoices.YEARLY
    object_qs = qs.filter(interval = inv_mo)

    url_path_name = "pricing_interval"
    mo_url = reverse(url_path_name, kwargs={"interval": inv_mo})
    yr_url = reverse(url_path_name, kwargs={"interval": inv_yr})

    active = inv_mo
    if interval == inv_yr:
        active = inv_yr
        object_qs = qs.filter(interval = inv_yr)

    return render(request, 'subscription/pricing.html', {
        "object_qs" : object_qs,
        "month_url" : mo_url,
        "yearly_url": yr_url,
        "active": active
    })