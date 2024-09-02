# Generated by Django 5.1 on 2024-08-28 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0007_alter_category_organisation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="customers",
                to="customers.category",
            ),
        ),
    ]
