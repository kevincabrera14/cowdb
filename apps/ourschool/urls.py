from django.urls import path
from django.contrib.auth import views as auth_views  # Agrega esta línea
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    #CRUD=============================================================================================================
    path('', views.inicio, name="inicio"),
    path('registro/', views.registrarse, name='registarse'),
    path('iniciar/', views.iniciar, name='iniciar'),
    path('pprincipal/', views.iniciar, name='pprincipal'),
    path('cerrar_session/', views.cerrar_session, name='cerrar_session'),
    path('registrarse/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('guardar/', views.guardar, name='guardar'),
    path('eliminar_usuario/<str:correo>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('admin_editar_formulario<str:correo>', views.admin_editar_formulario, name='admin_editar_formulario'),
    path('guardar_cambios/<str:correo>/', views.guardar_cambios_usuario, name='guardar_cambios'),
    path('inicio-profesor/', views.inicio_profesor, name='inicio_profesor'),
    path('inicio-estudiante/', views.inicio_estudiante, name='inicio_estudiante'),

    #OTROS=======================================================================================================================
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='ourschool/password_reset_done.html'), name='password_reset_done'),  # Aquí importamos auth_views y usamos PasswordResetDoneView
    path('correo/', views.correo, name='correo'),

    #inicio integracion CowDB==============================================================================================================
    path("mis-animales/", views.mis_animales, name="mis_animales"),
    path("crear-animal/", views.crear_animal, name="crear_animal"),
    path("editar-animal/<int:animal_id>/", views.editar_animal, name="editar_animal"),
    path("eliminar-animal/<int:animal_id>/", views.eliminar_animal, name="eliminar_animal"),
    path("animal/<int:animal_id>/", views.detalle_animal, name="detalle_animal"),
    path("animal/<int:animal_id>/agregar-evento/", views.agregar_evento, name="agregar_evento"),
    path("evento/<int:evento_id>/eliminar/", views.eliminar_evento, name="eliminar_evento"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
