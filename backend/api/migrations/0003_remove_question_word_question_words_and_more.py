# Generated by Django 4.0.6 on 2022-09-12 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_word_linked_alter_question_difficulty_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='word',
        ),
        migrations.AddField(
            model_name='question',
            name='words',
            field=models.ManyToManyField(to='api.word'),
        ),
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1),
        ),
        migrations.AlterField(
            model_name='tag',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1),
        ),
        migrations.AlterField(
            model_name='userquestion',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1),
        ),
        migrations.AlterField(
            model_name='userscreenflow',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1),
        ),
        migrations.AlterField(
            model_name='usersentence',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1),
        ),
        migrations.AlterField(
            model_name='word',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1),
        ),
    ]
