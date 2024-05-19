# Generated by Django 4.1 on 2024-04-29 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_remove_post_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                null=True, upload_to="post/pic/", verbose_name="图片"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="create_time",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="update_time",
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]
