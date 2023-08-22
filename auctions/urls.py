from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("aboutus", views.aboutus, name="aboutus"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("viewlisting/<int:product_id>", views.viewlisting, name="viewlisting"),
    path("categories", views.categories, name="categories"),
    path("addtowatchlist/<int:product_id>",
         views.addtowatchlist, name="addtowatchlist"),
    path("addcomment/<int:product_id>", views.addcomment, name="addcomment"),
    path("category/<str:name>", views.category, name="category"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("contactus", views.contact_us, name="contactus")
   
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
