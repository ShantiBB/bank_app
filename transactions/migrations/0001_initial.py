# Generated by Django 5.1.4 on 2024-12-09 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сумма перевода')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], default='RUB', max_length=10, verbose_name='Валюта')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Сообщение')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Депозит'), ('withdrawal', 'Снятие'), ('transfer', 'Перевод на счет')], default='transfer_in', max_length=20, verbose_name='Тип транзакции')),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('completed', 'Завершена'), ('failed', 'Неудачная')], default='pending', max_length=10, verbose_name='Статус перевода')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account', verbose_name='Счет')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
                'ordering': ['-created_at'],
            },
        ),
    ]
