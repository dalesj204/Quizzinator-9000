# Generated by Django 4.1.6 on 2023-02-22 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_home', '0007_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='gradebook',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quiz_home.grade'),
        ),
    ]