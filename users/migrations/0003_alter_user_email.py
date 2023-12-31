# Generated by Django 4.2.5 on 2023-11-02 22:03

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_name_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[users.models.User.csuf_email_validator]),
        ),
    ]
