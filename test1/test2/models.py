from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, Group

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class Client(models.Model):
    full_name = models.CharField("ФИО", max_length=150)
    login = models.CharField("Логин", max_length=50, unique=True)
    password = models.CharField("Пароль", max_length=128)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, verbose_name="Роль")

    def __str__(self):
        return f"{self.full_name} ({self.login})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Category(models.Model):
    name = models.CharField("Категория", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Supplier(models.Model):
    name = models.CharField("Поставщик", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Manufacturers(models.Model):
    name = models.CharField("Производитель", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Product(models.Model):
    # ID — автоинкрементный PK (по умолчанию в Django)
    article = models.CharField("Артикул", max_length=50, unique=True)
    name = models.CharField("Наименование", max_length=200)
    unit = models.CharField("Единица измерения", max_length=20)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="Поставщик")
    manufacturer = models.ForeignKey(Manufacturers, on_delete=models.PROTECT, verbose_name="Производитель")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    discount = models.PositiveSmallIntegerField("Скидка (%)", default=0)
    stock = models.PositiveIntegerField("Остаток на складе")
    description = models.TextField("Описание", blank=True)
    image_path = models.CharField("Путь к фото", max_length=255, default="picture.png")

    def __str__(self):
        return f"{self.article} – {self.name}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Pickup_point(models.Model):
    address = models.CharField("Адрес пункта выдачи", max_length=255, unique=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"


class Order(models.Model):
    order_number = models.CharField("Номер заказа", max_length=50, unique=True)
    order_date = models.DateTimeField("Дата заказа", auto_now_add=True)
    delivery_date = models.DateTimeField("Дата доставки", null=True, blank=True)
    pickup_point = models.ForeignKey(Pickup_point, on_delete=models.PROTECT, verbose_name="Пункт выдачи")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    code = models.CharField("Код для получения", max_length=10)
    status = models.CharField("Статус заказа", max_length=50)

    def __str__(self):
        return f"Заказ №{self.order_number} от {self.client.full_name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Order_composition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("Количество", validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    class Meta:
        verbose_name = "Состав заказа"
        verbose_name_plural = "Составы заказов"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('client', 'Авторизованный клиент' )
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
