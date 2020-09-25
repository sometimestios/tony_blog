# Generated by Django 2.2.5 on 2020-09-12 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('createdTime', models.DateTimeField()),
                ('modified_time', models.DateTimeField()),
                ('body', models.TextField()),
                ('excerpt', models.TextField(blank=True, max_length=400)),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category')),
                ('tag', models.ManyToManyField(to='blog.Tag')),
            ],
        ),
    ]
