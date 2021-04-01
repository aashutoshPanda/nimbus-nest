# Generated by Django 3.1.2 on 2021-03-31 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0003_folder_present_in_shared_me_of'),
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_file', to='folder.folder'),
        ),
    ]