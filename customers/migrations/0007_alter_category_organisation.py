# Generated by Django 5.1 on 2024-08-28 12:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0006_category_organisation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="customers.userprofile"
            ),
        ),
    ]
