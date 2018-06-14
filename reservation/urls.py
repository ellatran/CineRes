from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_view, name='liste'),
    path('list/<int:pk>/', views.detail, name='detail'),
    path('list/<int:pk>/screening/', views.screenings, name='screenings'),
    path('screen/<int:scrID>/seat_selection/', views.seat_selection, name='seat_selection'),
    path('booking/<int:b_id>', views.booking, name='booking'),
]
