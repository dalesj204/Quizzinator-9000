# Generated by Django 3.2.16 on 2023-03-03 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_home', '0013_subjecttags_questions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MultipleChoiceQuestion',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='question_type',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='subject_tag',
        ),
        migrations.DeleteModel(
            name='QuestionBank',
        ),
        migrations.DeleteModel(
            name='Questions',
        ),
        migrations.DeleteModel(
            name='SubjectTags',
        ),
    ]