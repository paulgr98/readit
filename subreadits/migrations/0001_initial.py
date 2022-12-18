# Generated by Django 4.1.2 on 2022-11-30 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subreadit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('moderators', models.ManyToManyField(blank=True, related_name='moderated_subreadits', to='users.readituser')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subreadits', to='users.readituser')),
            ],
        ),
    ]