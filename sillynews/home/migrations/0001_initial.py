# Generated by Django 2.0.12 on 2019-11-30 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20191130_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('content-type', 'ContentType'), ('news_group', 'NewsGroup'), ('tweets', 'Tweets'), ('insta_feed', 'InstaFeed')], max_length=32)),
                ('item_id', models.IntegerField(db_index=True, default=-1)),
                ('sequence_no', models.IntegerField(db_index=True, default=1)),
                ('login_required', models.BooleanField(db_index=True, default=False)),
                ('is_active', models.BooleanField(db_index=True, default=False)),
                ('home_version', models.IntegerField(db_index=True, default=1)),
            ],
        ),
        migrations.CreateModel(
            name='NewsChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.TextField(null=True)),
                ('icon_url', models.CharField(max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('icon_url', models.CharField(max_length=512, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=False)),
                ('rank', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsRssLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=512)),
                ('title', models.CharField(max_length=255, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(null=True)),
                ('link_rank', models.IntegerField(db_index=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.NewsContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('time', models.DateTimeField(null=True)),
                ('icon_url', models.CharField(max_length=512, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('deleted', 'Deleted')], db_index=True, default='active', max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('deleted', 'Deleted')], db_index=True, default='pending', max_length=255)),
                ('rank', models.IntegerField(null=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Schedule')),
            ],
        ),
    ]