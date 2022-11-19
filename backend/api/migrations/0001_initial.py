# Generated by Django 4.0.6 on 2022-11-18 18:15

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
            name='InfoCard',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_url', models.TextField()),
                ('voice_url', models.TextField()),
            ],
            options={
                'db_table': 'info_cards',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('rate', models.PositiveSmallIntegerField(default=5)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Normal'), (1, 'Describe the image'), (2, 'You are a teacher')])),
                ('difficulty', models.PositiveSmallIntegerField(choices=[(0, 'Easy'), (1, 'Moderate'), (2, 'Complex'), (3, 'Unknown')], default=0)),
                ('image_url', models.TextField()),
                ('voice_url', models.TextField()),
            ],
            options={
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='ShortVideo',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('cover', models.TextField()),
                ('url', models.TextField()),
            ],
            options={
                'db_table': 'short_videos',
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
                ('word', models.CharField(max_length=20)),
                ('meaning', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('difficulty', models.PositiveSmallIntegerField(choices=[(0, 'Easy'), (1, 'Moderate'), (2, 'Complex'), (3, 'Unknown')])),
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
                ('meaning', models.CharField(blank=True, default='', max_length=200)),
                ('extras', models.TextField(blank=True, default='')),
                ('total_uses', models.PositiveSmallIntegerField(default=0)),
                ('last_time_used', models.DateTimeField(null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Normal'), (1, 'Group')])),
                ('origin', models.PositiveSmallIntegerField(choices=[(0, 'Random generated'), (1, 'Saved from library'), (2, 'Created by user')])),
                ('source_type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Short video'), (1, 'Info card')], null=True)),
                ('info_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.infocard')),
                ('short_video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.shortvideo')),
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
            name='UserHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_uses', models.PositiveSmallIntegerField(default=0)),
                ('last_time_used', models.DateTimeField()),
                ('question_id', models.IntegerField()),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Normal'), (1, 'Describe the image'), (2, 'You are a teacher')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_history',
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('background_screen', models.CharField(max_length=20)),
                ('background_challenge', models.CharField(blank=True, max_length=20, null=True)),
                ('use_gradient', models.BooleanField(default=False)),
                ('bottom_gradient_color', models.CharField(blank=True, max_length=20, null=True)),
                ('top_gradient_color', models.CharField(blank=True, max_length=20, null=True)),
                ('question_position', models.DecimalField(decimal_places=2, default=0.3, max_digits=3)),
                ('image_position', models.DecimalField(decimal_places=2, default=0.1, max_digits=3)),
                ('question_font_size', models.DecimalField(decimal_places=1, default=21.0, max_digits=3)),
                ('question_opacity', models.DecimalField(decimal_places=2, default=0.4, max_digits=3)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.question')),
            ],
            options={
                'db_table': 'styles',
            },
        ),
        migrations.CreateModel(
            name='ResourceSentence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('sentence', models.CharField(max_length=20)),
                ('meaning', models.CharField(blank=True, default='', max_length=200)),
                ('extras', models.TextField(blank=True, default='')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Normal'), (1, 'Group')])),
                ('source_type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Short video'), (1, 'Info card')], null=True)),
                ('info_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.infocard')),
                ('short_video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.shortvideo')),
            ],
            options={
                'db_table': 'resource_sentences',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='api.tag'),
        ),
        migrations.AddField(
            model_name='question',
            name='words',
            field=models.ManyToManyField(to='api.word'),
        ),
        migrations.CreateModel(
            name='FavoriteResource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('source_type', models.PositiveSmallIntegerField(choices=[(0, 'Short video'), (1, 'Info card')])),
                ('info_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.infocard')),
                ('short_video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.shortvideo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite_resources',
            },
        ),
        migrations.CreateModel(
            name='Example',
            fields=[
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('example', models.JSONField()),
                ('voice_url', models.TextField()),
                ('word_text', models.CharField(blank=True, max_length=20, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.question')),
            ],
            options={
                'db_table': 'examples',
            },
        ),
        migrations.CreateModel(
            name='Collocation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Deleted'), (1, 'Active')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(blank=True, max_length=150, null=True)),
                ('source_type', models.PositiveSmallIntegerField(choices=[(0, 'Short video'), (1, 'Info card')])),
                ('info_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.infocard')),
                ('short_video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.shortvideo')),
            ],
            options={
                'db_table': 'collocations',
            },
        ),
    ]
