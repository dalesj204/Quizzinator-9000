# Generated by Django 4.1.6 on 2023-03-01 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_home', '0011_teacher_alter_stats_options_remove_class_instructor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
