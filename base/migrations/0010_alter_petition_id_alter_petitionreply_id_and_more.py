# Generated by Django 4.2.5 on 2023-11-03 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_petition_id_alter_petitionreply_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='id',
            field=models.UUIDField(default='uuid.uuid4', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='petitionreply',
            name='id',
            field=models.UUIDField(default='uuid.uuid4', editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='signature',
            name='id',
            field=models.UUIDField(default='uuid.uuid4', editable=False, primary_key=True, serialize=False),
        ),
    ]
