# Generated by Django 5.0.6 on 2024-07-22 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0014_alter_subscription_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionprice',
            options={'ordering': ['subscription__order', 'order', 'featured', '-updated']},
        ),
    ]
