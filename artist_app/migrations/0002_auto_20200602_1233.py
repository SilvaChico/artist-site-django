# Generated by Django 3.0.6 on 2020-06-02 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artpiece',
            name='made_by',
            field=models.ManyToManyField(blank=True, null=True, to='artist_app.Artist'),
        ),
    ]
