# Generated by Django 4.2 on 2023-06-09 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignee',
            old_name='board',
            new_name='boards',
        ),
    ]