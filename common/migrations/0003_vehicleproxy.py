# Generated by Django 4.0.4 on 2022-06-22 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_alter_userproxy_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="VehicleProxy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("1", "Active"),
                            ("2", "Inactive"),
                            ("3", "Deleted"),
                            ("4", "Blocked"),
                        ],
                        default="1",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "registration",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.customerproxy",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.userproxy",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
