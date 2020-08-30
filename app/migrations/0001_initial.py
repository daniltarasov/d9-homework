# Generated by Django 2.2.5 on 2020-08-30 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('status', models.CharField(choices=[('D', 'draft'), ('P', 'published')], max_length=10)),
                ('content', models.TextField()),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='app.Category')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='app.Album')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('album', 'order')},
            },
        ),
    ]