from django.urls import path
from easychoiceapp import views
from easychoice import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home),
    path('pdetails/<pid>', views.pdetails),
    path('cart', views.cart),
    path('login', views.ulogin),
    path('register', views.register),
    path('profile', views.profile),
    path('logout', views.ulogout),
    path('catfilter/<cv>', views.catfilter),
    path('addtocart/<pid>', views.addtocart),
    path('updateqty/<qv>/<cid>', views.updateqty),
    path('remove/<uid>', views.remove),
    path('remove_cart/<uid>', views.remove_cart),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    path('sendusermail',views.sendusermail),
    path('search',views.search),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
