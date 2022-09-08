# Generated by Django 4.1 on 2022-09-02 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemPhoto', models.ImageField(blank=True, null=True, upload_to='ChickenFarmApp/uploadedItemImages')),
                ('itemName', models.CharField(blank=True, max_length=20, null=True)),
                ('itemDesc', models.CharField(blank=True, max_length=500, null=True)),
                ('itemQty', models.IntegerField(blank=True, null=True)),
                ('itemPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, null=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ChickenFarmApp.cart')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ChickenFarmApp.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='carts',
            field=models.ManyToManyField(through='ChickenFarmApp.ItemCart', to='ChickenFarmApp.cart'),
        ),
    ]
