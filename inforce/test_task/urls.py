from django.urls import path
from .views import RestaurantCreateView, MenuCreateView, RestaurantMenuListView, MenuByDayListView, EmployeeRegistrationView, vote, WinningMenuView

urlpatterns = [
    path('create-restaurant/', RestaurantCreateView.as_view(), name='create-restaurant'),
    path('create-menu/', MenuCreateView.as_view(), name='menu-create'),
    path('restaurant/<int:restaurant_id>/menu/', RestaurantMenuListView.as_view(), name='restaurant-menu-list'),
    path('menu-by-day/<str:day_of_week>/', MenuByDayListView.as_view(), name='menu-by-day'),
    path('register/', EmployeeRegistrationView.as_view(), name='register'),
    path('vote/', vote, name='vote'),
    path('today/', WinningMenuView.as_view(), name='winning_menu_today'),
]
