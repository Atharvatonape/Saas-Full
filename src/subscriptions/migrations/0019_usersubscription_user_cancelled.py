# Generated by Django 5.0.6 on 2024-07-25 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0018_usersubscription_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='user_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
