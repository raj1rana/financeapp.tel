from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profilePic = models.ImageField(upload_to='static/profile', default='staic/profile/default_user.jpg')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='financeapp_tel_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='financeapp_tel_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"


class Transactions(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_from_budget = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.name}"


class Budget(models.Model):
    name = models.CharField(max_length=255)
    month = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.month} ({self.amount})"


class Rules(models.Model):
    name = models.CharField(max_length=255)
    conditions = models.TextField()
    actions = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.conditions}, {self.actions})"


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lender = models.CharField(max_length=255)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Loan from {self.lender} ({self.user.username}, {self.account.name}, {self.interest_rate}, {self.start_date}, {self.installment_amount})"
