
from django.contrib import admin
from django.urls import path
from My_App import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('sign/',views.sign,name="signin"),
    path('homepage/',views.home,name='home'),
    path('register/', views.register_complaint, name='register_complaint'), 
    path('track/', views.track_complaint, name='track_complaint'),
    path('edit_complaint/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'), 
    path('delete_complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('super_admin_dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('error/', views.error_page, name='error_page'),
    path('view_complaint/<int:complaint_id>/', views.view_complaint, name='view_complaint'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
   # path('logout/', views.logout_view, name='logout_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)