# Generated by Django 2.2 on 2020-01-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_person_ispresent'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='photo',
            field=models.ImageField(default='/home/anuraag/sih/sih/photos/default.png', upload_to=''),
        ),
    ]
