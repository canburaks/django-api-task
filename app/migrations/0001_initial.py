# Generated by Django 3.1 on 2022-07-01 11:39

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
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=90, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=32, null=True)),
                ('last_name', models.CharField(blank=True, max_length=32, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('liked', models.ManyToManyField(blank=True, db_table='profile_post_1', related_name='liked_by', to='app.Post')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='app.profile'),
        ),
    ]