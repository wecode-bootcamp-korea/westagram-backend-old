from django.db import models


class Account(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=400)

    class Meta:
        db_table = "menus"


class Category(models.Model):
    name = models.CharField(max_length=45)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)

    class Meta:
        db_table = "categories"


class Drink(models.Model):
    category     = models.ForeignKey('Category', on_delete=models.CASCADE)
    korean_name  = models.CharField(max_length=45)
    english_name = models.CharField(max_length=45)
    description  = models.TextField()

    class Meta:
        db_table = "drinks"


class Nutrition(models.Model):
    drink            = models.ForeignKey('Drink', on_delete=models.CASCADE)
    one_serving_kcal = models.DecimalField(max_digits=6, decimal_places=2)
    sodium_mg        = models.DecimalField(max_digits=6, decimal_places=2)
    saturated_fat_g  = models.DecimalField(max_digits=6, decimal_places=2)
    sugars_g         = models.DecimalField(max_digits=6, decimal_places=2)
    protein_g        = models.DecimalField(max_digits=6, decimal_places=2)
    caffeine_mg      = models.DecimalField(max_digits=6, decimal_places=2)
    size_ml          = models.CharField(max_length=45)
    size_fluid_ounce = models.CharField(max_length=45)

    class Meta:
        db_table = "nutritions"


class Image(models.Model):
    drink     = models.ForeignKey('Drink', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2000)

    class Meta:
        db_table = "images"


class Allergy(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "allergies"


class Allergy_drink(models.Model):
    allergy = models.ForeignKey('Allergy', on_delete=models.CASCADE)
    drink   = models.ForeignKey('Drink', on_delete=models.CASCADE)

    class Meta:
        db_table = "allergies_drink"