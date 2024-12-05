from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('about',views.About,name='about'),
    path('advisory/', views.travel_advisory, name='travel_advisory'), # Home view
    path('booking/',views.hotel,name='hotel'),
    path('payment_success/',views.payment_success,name='hotel'),
    path('initiate-payment/<int:hotel_id>/', views.initiate_payment, name='initiate_payment'),
    path('community/', views.community, name='community'),
    path('community/create/', views.create_post, name='create_post'),
    path('community/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('community/<int:post_id>/like/', views.like_post, name='like_post'),
    path('bot/', views.bot, name='bot'),
] 
