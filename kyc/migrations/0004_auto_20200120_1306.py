# Generated by Django 3.0.2 on 2020-01-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0003_input_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='error',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='output',
            name='status',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='output',
            name='number',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
