# Generated by Django 5.1.4 on 2024-12-09 17:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название счета')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание счета')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Сумма перевода')),
                ('account_type', models.CharField(choices=[('checking', 'Текущий счет'), ('savings', 'Сберегательный счет'), ('credit', 'Кредитный счет')], default='checking', max_length=10, verbose_name='Тип счета')),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], default='RUB', max_length=10, verbose_name='Валюта')),
                ('status_account', models.CharField(choices=[('active', 'Активно'), ('blocked', 'Заблокирован'), ('closed', 'Закрыт')], default='active', max_length=10, verbose_name='Статус счета')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец счета')),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
            },
        ),
    ]
