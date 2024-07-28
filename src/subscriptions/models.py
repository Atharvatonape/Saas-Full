import datetime
import helpers.billing
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.utils import timezone



User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUP = True
# Create your models here.
# Create your models here.
SUBSCRIPTION_PERMISSIONS = [
            ("advanced", "Advanced Perm"),
            ("pro", "Pro Perm"),
            ("basic", "Basic Perm"),
            ("basic_ai", "Basic AI Perm"),
]



    # def by_user_ids(self, user_ids=None):
    #     pass



class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={"content_type__app_label": "subscriptions", "codename__in": [x[0] for x in SUBSCRIPTION_PERMISSIONS]})
    subtitle = models.TextField(blank=True, null=True)

    stripe_id = models.CharField(max_length=120, null=True, blank = True)
    order = models.IntegerField(default=-1, help_text="Ordering on Django Pricing Page")
    featured = models.BooleanField(default=True, help_text="Featured on Django pricing page")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    features = models.TextField(help_text="Features for pricing, separated by new line", blank=True, null=True)


    def __str__(self) -> str:
        return f"{self.name}"

    def get_features_as_list(self):
        if not self.features:
            return []
        return [x.strip() for x in self.features.split("\n")]

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS
        ordering = ['order', 'featured', '-updated']


    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_id = helpers.billing.create_product(name = self.name ,metadata = {"subscription_plan_id" : self.id},raw = False)
            self.stripe_id = stripe_id
            print(stripe_id)
        super().save(*args, **kwargs)

class SubscriptionPrice(models.Model):

    class IntervalChoices(models.TextChoices):
        MONTHLY = "month", "Monthly"
        YEARLY = "year", "Yearly"

    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    stripe_id = models.CharField(max_length=120, null=True, blank = True)
    interval = models.CharField(max_length=120, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    order = models.IntegerField(default=-1, help_text="Ordering on Django Pricing Page")
    featured = models.BooleanField(default=True, help_text="Featured on Django pricing page")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subscription__order','order', 'featured', '-updated']

    def get_checkout_url(self):
        return reverse("sub-price-checkout",
                       kwargs = {"price_id": self.id}
                    )

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def stripe_price(self):
        """
        remove Decimal places
        """
        return int(self.price * 100)

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    @property
    def display_features_list(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()

    @property
    def display_sub_name(self):
        if not self.subscription:
            return "Price"
        return self.subscription.name

    @property
    def display_sub_subtitle(self):
        if not self.subscription:
            return "Price"
        return self.subscription.subtitle

    def save(self, *args, **kwargs):
        if self.stripe_id is None and self.product_stripe_id is not None:

            stripe_id = helpers.billing.create_price(
            currency=self.stripe_currency,
            unit_amount=self.stripe_price,
            interval= self.interval,
            product=self.product_stripe_id,
            metadata={
                "subscription_plan_price_id" : self.id
                }
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)
        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription = self.subscription,
                interval = self.interval
            ).exclude(id=self.id)
            qs.update(featured = False)

class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        TRIALING = 'trialing', 'Trialing'
        INCOMPLETE  = 'incomplete', 'Incomplete'
        INCOMPLETE_EXPIRED = 'incomplete_expired', 'Incomplete Expired'
        PAST_DUE = 'past_due', 'Past Due'
        CANCELLED = 'canceled', 'Canceled'
        UNPAID = 'unpaid', 'Unpaid'
        PAUSED = 'paused', 'Paused'

class UserSubscriptionQuerySet(models.QuerySet):
    def by_range(self, days_start=7, days_end=120):
        now = timezone.now()
        days_start_from_now = now + datetime.timedelta(days=days_start)
        days_end_from_now = now + datetime.timedelta(days=days_end)
        range_start = days_start_from_now.replace(hour=0, minute=0, second=0, microsecond=0)
        range_end = days_end_from_now.replace(hour=23, minute=59, second=59, microsecond=59)
        return self.filter(
            current_period_end__gte=range_start,
            current_period_end__lte=range_end
        )

    def by_days_left(self, days_left=7):
        now = timezone.now()
        in_n_days = now + datetime.timedelta(days=days_left)
        day_start = in_n_days.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = in_n_days.replace(hour=23, minute=59, second=59, microsecond=59)
        return self.filter(
            current_period_end__gte=day_start,
            current_period_end__lte=day_end
        )

    def by_days_ago(self, days_ago=3):
        now = timezone.now()
        in_n_days = now - datetime.timedelta(days=days_ago)
        day_start = in_n_days.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = in_n_days.replace(hour=23, minute=59, second=59, microsecond=59)
        return self.filter(
            current_period_end__gte=day_start,
            current_period_end__lte=day_end
        )

    def by_active_trialing(self):
        active_qs_lookup = (
            Q(status = SubscriptionStatus.ACTIVE) |
            Q(status = SubscriptionStatus.TRIALING)
        )
        return self.filter(active_qs_lookup)

    def by_user_ids(self, user_ids=None):
        qs = self
        if isinstance(user_ids, list):
            qs = self.filter(user_id__in=user_ids)
        elif isinstance(user_ids, int):
            qs = self.filter(user_id__in=[user_ids])
        elif isinstance(user_ids, str):
            qs = self.filter(user_id__in=[user_ids])
        return qs

class UserSubscriptionManager(models.Manager):

    def get_queryset(self):
        return UserSubscriptionQuerySet(self.model, using=self._db)

    # def by_user_ids(self,user_ids=None):
    #     return self.get_queryset().by_user_ids(user_ids=user_ids)

class UserSubscription(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL,null=True, blank=True)
    stripe_id = models.CharField(max_length=120, null=True, blank = True)
    active = models.BooleanField(default=True)
    user_cancelled = models.BooleanField(default=False)
    original_period_start = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    current_period_start = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    current_period_end = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    status = models.CharField(max_length=120, null=True, blank=True, choices=SubscriptionStatus.choices)

    cancel_at_period_end = models.BooleanField(default=False)

    @property
    def plan_name(self):
        if not self.subscription:
            return None
        return self.subscription.name

    def serialize(self):
        return{
            "plan_name": self.plan_name,
            "status": self.status,
            "current_period_start": self.current_period_start,
            "current_period_end": self.current_period_end
        }

    def get_absolute_url(self):
        return reverse('user_subscription')

    def get_cancel_url(self):
        return reverse('user_subscription_cancel')

    @property
    def is_active_status(self):
        return self.status in [SubscriptionStatus.ACTIVE , SubscriptionStatus.TRIALING]

    @property
    def billing_cycle_anchor(self):
        """
        option to start subscription later in stripe
        """
        if not self.current_period_end:
            return
        return int(self.current_period_end.timestamp())

    def save(self, *args, **kwargs):
        if (self.original_period_start is None and self.current_period_start is not None):
            self.original_period_start = self.current_period_start
        super().save(*args, **kwargs)


# def user_sub_post_save(sender, instance, *args, **kwargs):
#     user_sub_instance = instance
#     user = user_sub_instance.user
#     subscription_obj = user_sub_instance.subscription
#     groups = subscription_obj.groups.all()
#     if not ALLOW_CUSTOM_GROUP:
#         user.groups.set(groups)
#     else:
#         # subs_qs = Subscription.objects.filter(active = True).exclude(id = subscription_ob.id)
#         # subs_groups = subs_qs.values_list("group__id", flat=True)
#         # subs_groups_set = set(subs_groups)
#         groups_ids = groups.values_list('id', flat= True)
#         current_groups = user.groups.all().values_list('id', flat= True)
#         groups_ids_set = set(groups_ids)
#         current_groups_set = set(current_groups) 
#         final_group_ids = list(groups_ids_set  | current_groups_set)
#         user.groups.sets(final_group_ids)

# post_save.connect(user_sub_post_save, sender=UserSubscription)