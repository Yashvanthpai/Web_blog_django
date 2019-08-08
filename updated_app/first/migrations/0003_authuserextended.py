# Generated by Django 2.1.7 on 2019-07-14 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_authuserextend'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUserExtended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bdate', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=5, null=True)),
                ('profilepic', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'auth_user_extended',
                'managed': False,
            },
        ),
    ]
