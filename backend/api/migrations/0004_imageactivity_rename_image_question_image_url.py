# Generated by Django 4.0.6 on 2022-09-14 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_question_word_question_words_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageActivity',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='questions_data/images')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='question',
            old_name='image',
            new_name='image_url',
        ),
    ]
