from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index1, name = 'index1'),
    path("upload_structures/", views.upload_structures_file, name = 'upload_structures_file'),
    path("upload_template/", views.upload_template_file, name = 'upload_template_file'),
    path("upload_pipes/", views.upload_pipes_file, name = 'upload_pipes_file'),
    path("order/", views.order_pipes_create_systems, name = 'order_pipes_create_systems'),
    path("analyse/", views.analyse_systems, name = 'analyse_systems'),
    path("new-project-name/", views.create_new_project_name, name = 'create_new_project_name'),
    path("select-project/", views.select_project, name = 'select_project'),
    path("developer/", views.developer, name = 'developer'),
    path("login/", views.login_page, name = 'login_page'),
    path("register/", views.register_user, name = 'register'),
    path("logout/", views.logout_user, name = 'logout'),
    path("export/", views.export_design, name='export_design'),
    path("pipes/", views.pipes_list, name='pipes_list'),
    path('pipes/<int:pk>/', views.pipes_detail),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)