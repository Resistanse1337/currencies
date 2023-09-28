# Generated by Django 4.2.5 on 2023-09-28 03:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rates', '0003_alter_currency_charcode'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trackedquote',
            unique_together={('user', 'currency')},
        ),
    ]