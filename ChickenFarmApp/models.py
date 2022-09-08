from django.db import models

# Create your models here.

class Cart(models.Model):
    user = models.CharField(max_length=20,null=True, blank=True)
    passW = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return self.user

class Item(models.Model):
    carts = models.ManyToManyField(Cart, through='ItemCart')
    itemPhoto = models.ImageField(upload_to='ChickenFarmApp/uploadedItemImages',null=True, blank=True)
    itemName = models.CharField(max_length=20,null=True, blank=True)
    itemDesc = models.CharField(max_length=500,null=True, blank=True)
    itemQty = models.IntegerField(null=True, blank=True)
    itemPrice = models.DecimalField(max_digits=19, decimal_places=2,null=True, blank=True)

    def __str__(self):
        return self.itemName

class ItemCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
