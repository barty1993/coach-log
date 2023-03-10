# Generated by Django 4.1.5 on 2023-02-03 08:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoachInGum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_agree', models.BooleanField(default=False)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KindOfSport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('title', models.CharField(max_length=255)),
                ('about_gum', models.TextField(blank=True, null=True)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city', to='gum.city')),
                ('coaches', models.ManyToManyField(through='gum.CoachInGum', to=settings.AUTH_USER_MODEL)),
                ('kind_of_sport', models.ManyToManyField(related_name='kind_of_sports', to='gum.kindofsport')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='o_gums', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='coachingum',
            name='gum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gum.gum'),
        ),
    ]
