# Generated by Django 4.2 on 2023-06-10 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_rename_board_assignee_boards'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='status',
            new_name='description',
        ),
    ]
