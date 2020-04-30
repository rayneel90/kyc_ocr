# Generated by Django 3.0.2 on 2020-01-19 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('PAN', 'PAN Card'), ('Aadhar', 'Aadhar Card'), ('Passport', 'Passport')], max_length=8, verbose_name='KYC Type')),
                ('image', models.FileField(upload_to='', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30)),
                ('input', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kyc.Input')),
            ],
        ),
    ]