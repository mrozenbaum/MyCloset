from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name="closetclient"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^view_account$', views.view_account, name='view_account'),
    # url(r'^add_item$', views.add_item, name='add'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
