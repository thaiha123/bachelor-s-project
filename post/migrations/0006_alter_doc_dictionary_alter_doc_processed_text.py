# Generated by Django 5.0.3 on 2024-04-01 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_doc_dictionary_alter_doc_processed_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc',
            name='dictionary',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='doc',
            name='processed_text',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
