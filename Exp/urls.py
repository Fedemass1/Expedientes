from django.urls import path
from Exp import views
from Exp.views import ExpActualizacion, ExpActualizacionPrueba, ExpAgregarPrueba, ExpEliminar, Pase, CrearArea, \
    DetalleExpediente, CrearIniciador


urlpatterns = [
    path('', views.index, name='index'),
    path('prueba/', views.index_prueba, name='index_prueba'),
    path('list_expedientes/', views.list_expedientes, name='list_expedientes'),
    path('list_expedientes_prueba/', views.list_expedientes_prueba, name='list_expedientes_prueba'),
    path('edit/<int:pk>/', ExpActualizacion.as_view(), name='edit_expedientes'),
    path('edit_prueba/<int:pk>/', ExpActualizacionPrueba.as_view(), name='edit_expedientes_prueba'),
    path('agregar_prueba/', ExpAgregarPrueba.as_view(), name='edit_expedientes_prueba'),
    path('eliminar_prueba/<int:pk>/', ExpEliminar.as_view(), name='delete_expedientes_prueba'),
    path('pase/<int:pk>/', Pase.as_view(), name='pase'),
    path('crear_area/', CrearArea.as_view(), name='crear_area'),
    path('crear_iniciador/', CrearIniciador.as_view(), name='crear_iniciador'),
    path('detalle_expediente/<int:pk>/', DetalleExpediente.as_view(), name='detalle_expediente'),
]
