# Generated by Django 4.1.13 on 2024-03-21 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Pdf_Extracter_app', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(blank=True, max_length=50, null=True)),
                ('agent', models.CharField(blank=True, max_length=50, null=True)),
                ('custom_file', models.CharField(blank=True, max_length=50, null=True)),
                ('dr_file', models.CharField(blank=True, max_length=50, null=True)),
                ('excel_file', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubmitData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_company', models.CharField(blank=True, max_length=50, null=True)),
                ('shipping_company', models.CharField(blank=True, max_length=50, null=True)),
                ('booking_no', models.CharField(blank=True, max_length=50, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
