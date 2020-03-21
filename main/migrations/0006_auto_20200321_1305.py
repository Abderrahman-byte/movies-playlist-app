# Generated by Django 3.0.4 on 2020-03-21 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20200320_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='playlistitem',
            constraint=models.UniqueConstraint(fields=('playlist', 'item_id', 'media_type'), name='non_duplicate_items_in_playlist'),
        ),
    ]
