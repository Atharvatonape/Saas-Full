from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save

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

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL,null=True, blank=True)
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