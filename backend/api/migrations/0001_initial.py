# Generated by Django 4.0.6 on 2022-09-29 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DescribeImageActivity',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_url', models.TextField()),
            ],
            options={
                'db_table': 'describeimage_activities',
            },
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Question'), (1, 'Describe Image')])),
                ('example', models.JSONField()),
                ('voice_url', models.TextField()),
                ('question_id', models.IntegerField(null=True)),
                ('word_id', models.IntegerField(null=True)),
                ('image_id', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'examples',
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('background_word', models.CharField(max_length=20)),
                ('background_screen', models.CharField(max_length=20)),
                ('activity_id', models.IntegerField()),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Question'), (1, 'Describe Image')])),
            ],
            options={
                'db_table': 'styles',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('linked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('word', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'words',
            },
        ),
        migrations.CreateModel(
            name='UserSentence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sentence', models.CharField(max_length=20)),
                ('meaning', models.CharField(blank=True, default='', max_length=100)),
                ('total_uses', models.PositiveSmallIntegerField(default=0)),
                ('last_time_used', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_sentences',
            },
        ),
        migrations.CreateModel(
            name='UserScreenFlow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_screenflow',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_words', models.PositiveSmallIntegerField(default=0)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profiles',
            },
        ),
        migrations.CreateModel(
            name='UserActivityHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_uses', models.PositiveSmallIntegerField(default=0)),
                ('last_time_used', models.DateTimeField()),
                ('activity_id', models.IntegerField()),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Question'), (1, 'Describe Image')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_activity_history',
            },
        ),
        migrations.CreateModel(
            name='QuestionActivity',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('rate', models.PositiveSmallIntegerField(default=5)),
                ('difficulty', models.PositiveSmallIntegerField(choices=[(0, 'Easy'), (1, 'Moderate'), (2, 'Complex')], default=0)),
                ('image_url', models.TextField()),
                ('voice_url', models.TextField()),
                ('tags', models.ManyToManyField(to='api.tag')),
                ('words', models.ManyToManyField(to='api.word')),
            ],
            options={
                'db_table': 'question_activities',
            },
        ),
    ]
