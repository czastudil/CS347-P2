# Generated by Django 2.1.7 on 2019-04-03 17:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tahours.models


class Migration(migrations.Migration):

    dependencies = [
        ('tahours', '0002_shiftswap'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayOfWeek', tahours.models.DayOfWeekField(choices=[(1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday')], max_length=1)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TaInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_hours', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('max_hours', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('availability', models.ManyToManyField(to='tahours.Availability')),
                ('courses', models.ManyToManyField(to='tahours.Course')),
            ],
            options={
                'ordering': ['ta'],
            },
        ),
        migrations.RemoveField(
            model_name='ta',
            name='courses',
        ),
        migrations.AddField(
            model_name='ta',
            name='ta_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tahours.TaInfo'),
        ),
    ]