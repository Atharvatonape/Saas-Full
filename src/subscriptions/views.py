from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from subscriptions.models import SubscriptionPrice, UserSubscription
from django.urls import reverse
import helpers.billing
from django.contrib import messages

@login_required
def user_subscription_view(request,):
    user_sub_obj , created = UserSubscription.objects.get_or_create(user=request.user)
    sub_data = user_sub_obj.serialize()
    if request.method == "POST":
        print("refreh sub")
        if user_sub_obj.stripe_id:
            sub_data = helpers.billing.get_checkout_subscription(user_sub_obj.stripe_id, raw=False)
            for k,v in sub_data.items():
                setattr(user_sub_obj, k,v)
            user_sub_obj.save()
            return redirect(user_sub_obj.get_absolute_url())
    return render(request, 'subscription/user_detail_view.html',
                  {
                      "subscription": user_sub_obj
                  })

@login_required
def user_subscription_cancel_view(request,):
    user_sub_obj , created = UserSubscription.objects.get_or_create(user=request.user)
    sub_data = user_sub_obj.serialize()
    if request.method == "POST":
        print("refreh sub")
        if user_sub_obj.stripe_id and user_sub_obj.is_active_status:
            sub_data = helpers.billing.cancel_subscription(
                user_sub_obj.stripe_id,
                cancel_at_period_end = True,
                reason ="User wanted to cancel",
                feedback="other",
                raw=False
                )
            for k,v in sub_data.items():
                setattr(user_sub_obj, k,v)
            user_sub_obj.save()
            messages.success(request, "Your plan has been cancelled")
        return redirect(user_sub_obj.get_absolute_url())
    return render(request, 'subscription/user_cancel_view.html',
                  {
                      "subscription": user_sub_obj
                  })

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