from django.urls import path		 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [			 
    path('', views.index, name='index'),                                                #made pages
    path('items/<int:item_id>', views.item),
    path('checkOut', views.checkOut, name='checkOut'),
    path('aboutUs', views.aboutUs, name='aboutUs'),

    path('cartHelper/<int:reply_id>', views.cartHelper),                                
    path('add/<int:reply_id>', views.add),
    path('items/add/<int:reply_id>', views.add),

    path('checkOut/delete/<int:item_id>', views.deleteItm),

    path('nwuser', views.addUser),
    path('pay', views.pay),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
