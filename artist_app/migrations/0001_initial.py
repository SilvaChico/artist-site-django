# Generated by Django 3.0.6 on 2020-06-02 11:31

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Died')),
                ('photograph', models.ImageField(upload_to='images/', verbose_name='what is this ?')),
                ('portfolio', models.FileField(upload_to='documents/', verbose_name='what is this ?')),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='ArtPiece',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Enter a description of the artpiece', max_length=1000)),
                ('medium_technique', models.CharField(help_text='Enter the medium used in this art-piece', max_length=30, verbose_name='medium/technique')),
                ('date', models.DateField(help_text='When was this artpiece made', verbose_name='')),
                ('image', models.ImageField(upload_to='images/', verbose_name='')),
                ('made_by', models.ManyToManyField(null=True, to='artist_app.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='images/logos/')),
                ('address', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('dates', django.contrib.postgres.fields.ranges.DateRangeField()),
            ],
        ),
        migrations.CreateModel(
            name='ArtPieceInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular artpiece across whole archive', primary_key=True, serialize=False)),
                ('bought_by', models.CharField(max_length=200)),
                ('bought_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('n', 'Not for sale'), ('o', 'Being exhibited'), ('a', 'Available'), ('r', 'Reserved'), ('s', 'Sold')], default='n', help_text='ArtPiece availability', max_length=1)),
                ('artpiece', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='artist_app.ArtPiece')),
            ],
            options={
                'ordering': ['bought_date'],
            },
        ),
        migrations.AddField(
            model_name='artpiece',
            name='project',
            field=models.ForeignKey(help_text='Select a project for this artpiece', on_delete=django.db.models.deletion.DO_NOTHING, to='artist_app.Project'),
        ),
        migrations.AddField(
            model_name='artist',
            name='represented_by',
            field=models.ForeignKey(help_text='Select a gallery that represents the artist, if any', on_delete=django.db.models.deletion.DO_NOTHING, to='artist_app.Gallery'),
        ),
    ]