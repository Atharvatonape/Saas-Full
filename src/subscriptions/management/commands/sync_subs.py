from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.models import Subscription

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        print('Hello World')
        qs =Subscription.objects.all()
        for obj in qs:
            sub_perms= obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(sub_perms)
            #print(obj.permissions.all())