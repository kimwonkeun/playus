# Generated by Django 4.0 on 2021-12-14 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniqueid', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=5)),
                ('kakaochat', models.CharField(max_length=50)),
                ('level', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='userlogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=50)),
                ('recentlog', models.DateField()),
                ('recenpos', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='playerdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth', models.DateField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playus.player')),
            ],
        ),
        migrations.CreateModel(
            name='playdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('starttime', models.DateTimeField()),
                ('gpsX', models.CharField(max_length=20)),
                ('gpsY', models.CharField(max_length=20)),
                ('detail', models.TextField()),
                ('kakaochat', models.CharField(max_length=50)),
                ('zoneXY', models.CharField(max_length=10)),
                ('zoneX', models.CharField(max_length=5)),
                ('zoneY', models.CharField(max_length=5)),
                ('party', models.SmallIntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playus.player')),
            ],
        ),
        migrations.CreateModel(
            name='partytable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=50)),
                ('partyindate', models.DateField()),
                ('p_gender', models.CharField(max_length=5)),
                ('p_nick', models.CharField(max_length=50)),
                ('playdata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playus.playdata')),
            ],
        ),
    ]
