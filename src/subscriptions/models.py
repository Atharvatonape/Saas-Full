from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
import helpers.billing
from django.urls import reverse


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


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL,null=True, blank=True)
    stripe_id = models.CharField(max_length=120, null=True, blank = True)
    active = models.BooleanField(default=True)

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