ACCOUNT_TYPES = [
    ('checking', 'Текущий счет'),
    ('savings', 'Сберегательный счет'),
    ('credit', 'Кредитный счет'),
]

STATUS_CHOICES = [
    ('active', 'Активно'),
    ('blocked', 'Заблокирован'),
    ('closed', 'Закрыт'),
]

CURRENCY_CHOICES = [
    ('USD', 'USD'),
    ('RUB', 'RUB'),
]

TRANSACTION_TYPES = [
        ('deposit', 'Депозит'),
        ('withdrawal', 'Снятие'),
        ('transfer', 'Перевод на счет'),
    ]

TRANSACTION_STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('completed', 'Завершена'),
        ('failed', 'Неудачная'),
    ]
