# Generated by Django 3.0.4 on 2020-03-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='profil',
            constraint=models.UniqueConstraint(fields=('user',), name='user_unique_profil'),
        ),
        migrations.AddConstraint(
            model_name='profil',
            constraint=models.UniqueConstraint(fields=('email',), name='email_unique_profil'),
        ),
    ]
