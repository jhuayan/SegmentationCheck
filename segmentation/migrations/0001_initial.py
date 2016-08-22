# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('char', models.CharField(max_length=4, db_index=True)),
                ('image', models.CharField(max_length=512)),
                ('left', models.SmallIntegerField()),
                ('right', models.SmallIntegerField()),
                ('top', models.SmallIntegerField()),
                ('bottom', models.SmallIntegerField()),
                ('line_no', models.SmallIntegerField()),
                ('char_no', models.SmallIntegerField()),
                ('is_correct', models.SmallIntegerField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterStatistics',
            fields=[
                ('char', models.CharField(max_length=4, serialize=False, primary_key=True, db_index=True)),
                ('total_cnt', models.IntegerField(default=0)),
                ('uncheck_cnt', models.IntegerField(default=0)),
                ('err_cnt', models.IntegerField(default=0)),
                ('uncertainty_cnt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OPage',
            fields=[
                ('no', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('discription', models.CharField(max_length=128)),
                ('number', models.SmallIntegerField()),
                ('image_path', models.CharField(max_length=512)),
                ('image_upload', models.ImageField(max_length=512, null=True, upload_to=b'opage_images')),
                ('width', models.SmallIntegerField()),
                ('height', models.SmallIntegerField()),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('image', models.CharField(max_length=512)),
                ('image_upload', models.ImageField(max_length=512, null=True, upload_to=b'page_images')),
                ('text', models.TextField()),
                ('width', models.SmallIntegerField(default=0)),
                ('height', models.SmallIntegerField(default=0)),
                ('left', models.SmallIntegerField(default=0)),
                ('right', models.SmallIntegerField(default=0)),
                ('is_correct', models.SmallIntegerField(default=0)),
                ('erro_char_cnt', models.IntegerField(default=0)),
                ('o_page', models.ForeignKey(blank=True, to='segmentation.OPage', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sutra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='SutraInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('discription', models.CharField(max_length=512)),
                ('author', models.CharField(max_length=64)),
                ('start', models.SmallIntegerField()),
                ('end', models.SmallIntegerField()),
                ('sutra', models.ForeignKey(to='segmentation.Sutra')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display', models.CharField(max_length=16)),
                ('is_base', models.BooleanField(default=False)),
                ('semanteme', models.ForeignKey(related_name='Text', blank=True, to='segmentation.Text')),
            ],
        ),
        migrations.CreateModel(
            name='Tripitaka',
            fields=[
                ('no', models.CharField(max_length=8, serialize=False, verbose_name='Tripitaka|no', primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Tripitaka|name')),
                ('n_volumes', models.SmallIntegerField(default=0, verbose_name='Tripitaka|n_volumes')),
                ('start', models.SmallIntegerField(verbose_name='Tripitaka|start')),
                ('end', models.SmallIntegerField(verbose_name='Tripitaka|end')),
            ],
            options={
                'verbose_name': 'tripitaka',
                'verbose_name_plural': 'tripitakas',
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('no', models.CharField(max_length=16, serialize=False, verbose_name='Volume|no', primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Volume|name')),
                ('number', models.SmallIntegerField(verbose_name='Volume|number')),
                ('n_pages', models.SmallIntegerField(verbose_name='Volume|n_pages')),
                ('start', models.SmallIntegerField(verbose_name='Volume|start')),
                ('end', models.SmallIntegerField(verbose_name='Volume|end')),
                ('tripitaka', models.ForeignKey(verbose_name='Volume|tripitaka', to='segmentation.Tripitaka')),
            ],
            options={
                'verbose_name': 'Segmentation|volume',
                'verbose_name_plural': 'Segmentation|volumes',
            },
        ),
        migrations.AddField(
            model_name='sutrainfo',
            name='tripitaka',
            field=models.ForeignKey(to='segmentation.Tripitaka'),
        ),
        migrations.AddField(
            model_name='opage',
            name='sutra_info',
            field=models.ForeignKey(to='segmentation.SutraInfo'),
        ),
        migrations.AddField(
            model_name='opage',
            name='tripitaka',
            field=models.ForeignKey(to='segmentation.Tripitaka'),
        ),
        migrations.AddField(
            model_name='opage',
            name='volume',
            field=models.ForeignKey(to='segmentation.Volume'),
        ),
        migrations.AddField(
            model_name='character',
            name='page',
            field=models.ForeignKey(to='segmentation.Page'),
        ),
        migrations.AddField(
            model_name='character',
            name='text',
            field=models.ForeignKey(blank=True, to='segmentation.Text', null=True),
        ),
    ]
