from django.contrib import admin

# Register your models here.
from .models import Item , Cart , ItemCart

# class ItemGroup(admin.ModelAdmin):         #showed id
#     readonly_fields = ('id',)

class StoreInline(admin.TabularInline):
    model = Item.carts.through

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

    inlines = [
        StoreInline,
    ]

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

    inlines = [
        StoreInline,
    ]
    
    exclude = ('carts',)                    #models methods to leaveout

class ItemCartAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

    
admin.site.register(Item,ItemAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(ItemCart,ItemCartAdmin)



