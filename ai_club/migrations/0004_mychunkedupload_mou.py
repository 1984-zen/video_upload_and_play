# Generated by Django 2.2 on 2021-12-27 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ai_club', '0003_mous_mou_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='mychunkedupload',
            name='mou',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chunked_uploads', to='ai_club.mous'),
        ),
    ]
