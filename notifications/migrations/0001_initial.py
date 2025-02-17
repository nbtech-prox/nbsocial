# Generated by Django 5.0.2 on 2025-02-17 20:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('like', 'Gosto'), ('comment', 'Comentário'), ('follow', 'Seguir'), ('mention', 'Menção')], max_length=20, verbose_name='tipo')),
                ('text', models.CharField(max_length=255, verbose_name='texto')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('read', models.BooleanField(default=False, verbose_name='lido')),
                ('read_at', models.DateTimeField(blank=True, null=True, verbose_name='lido em')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='posts.comment', verbose_name='comentário')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='posts.post', verbose_name='publicação')),
            ],
            options={
                'verbose_name': 'notificação',
                'verbose_name_plural': 'notificações',
                'ordering': ['-created_at'],
            },
        ),
    ]
