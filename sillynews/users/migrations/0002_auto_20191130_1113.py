# Generated by Django 2.0.12 on 2019-11-30 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInstaPostSeen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField(blank=True, max_length=250)),
                ('visited_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userinstapostseen',
            unique_together={('profile', 'post_id')},
        ),
    ]
