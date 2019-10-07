# Generated by Django 2.1.7 on 2019-07-05 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUserExtend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, max_length=5, null=True)),
                ('bdate', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'auth_user_extend',
                'managed': False,
            },
        ),
    ]