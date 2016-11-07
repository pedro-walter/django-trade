# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-02 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_bidmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='accepted_for_trade',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='bidder_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='offerer_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[(b'OF', b'Offered'), (b'BA', b'Bid Accepted'), (b'CO', b'Completed'), (b'CA', b'Canceled')], default=b'OF', max_length=2),
        ),
    ]