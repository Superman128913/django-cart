# Generated by Django 4.0.4 on 2022-07-11 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllowRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(choices=[('on', 'Register Enabled'), ('off', 'Register Disabled')], default='on', max_length=3)),
                ('Note', models.CharField(default='', help_text='Enter note', max_length=128)),
            ],
        ),
    ]
