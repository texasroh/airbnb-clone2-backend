# Generated by Django 4.1.1 on 2022-10-08 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='genter',
            new_name='gender',
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(choices=[('won', 'Korean Won'), ('usd', 'Dollar')], max_length=5),
        ),
    ]
