# Generated by Django 4.1.2 on 2022-11-30 09:56

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
            name='ReaditUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('about_text', models.TextField(blank=True, default='', help_text='Tell us about yourself', max_length=500, null=True, verbose_name='About')),
                ('avatar_url', models.URLField(blank=True, default='', max_length=500, null=True, verbose_name='Avatar URL')),
                ('karma', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]