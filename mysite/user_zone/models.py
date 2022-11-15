from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # Create user
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user
    # Create admin
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser):
    # Storage of users
    email = models.EmailField(max_length=300, unique=True, verbose_name="Email")
    is_admin = models.BooleanField(default=False, verbose_name="Admin")

    class Meta:
        verbose_name = "Uživatel"
        verbose_name_plural = "Uživatelé"

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "{}".format(self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class GeneralData(models.Model):
    # Storage of general data of users
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="Email")
    name = models.CharField(max_length=200, verbose_name="Jméno")
    surname = models.CharField(max_length=200, verbose_name="Příjmení")
    telephone_number = models.CharField(max_length=200, verbose_name="Telefon")
    company_name = models.CharField(max_length=200, verbose_name="Název firmy")
    register_id = models.CharField(max_length=200, verbose_name="IČO")
    vat_id = models.CharField(max_length=200, verbose_name="DIČ")
    street = models.CharField(max_length=200, verbose_name="Ulice")
    building_number = models.CharField(max_length=200, verbose_name="Číslo popisné")
    zip_code = models.CharField(max_length=200, verbose_name="PSČ")
    city = models.CharField(max_length=200, verbose_name="Město")
    country = models.CharField(max_length=200, verbose_name="Země")

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Osobní údaje"

    def __str__(self):
        return "{}".format(self.user)

class ProductProperty(models.Model):
    # Storage of products properties
    product_name = models.CharField(max_length=200, verbose_name="Název produktu")

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

class ProductSales(models.Model):
    # Storage of all products sold
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="Email")
    product_name = models.ForeignKey(ProductProperty, on_delete=models.RESTRICT, verbose_name="Název produktu")
    order_date = models.DateTimeField(verbose_name="Datum objednávky")
    payment_date = models.DateTimeField(verbose_name="Datum platby")
    expiration_date = models.DateTimeField(verbose_name="Datum expirace")

    class Meta:
        verbose_name = "Prodej produktu"
        verbose_name_plural = "Prodeje produktů"
