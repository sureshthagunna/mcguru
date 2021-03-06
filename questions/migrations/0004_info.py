# Generated by Django 2.1.7 on 2019-06-16 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20190615_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('total_questions', models.PositiveIntegerField(default=0)),
                ('last_answered', models.CharField(default=0, max_length=255)),
                ('iteration_num', models.PositiveIntegerField(default=1, editable=False)),
            ],
        ),
    ]
