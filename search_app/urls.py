from django.urls import path
from . import views

app_name = "search_app"

urlpatterns = [
    path('', views.search_view, name='search'),
    path('add_search_history/', views.add_search_history, name='add_search_history'),
    path('toggle_favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites_api/', views.favorites_api, name='favorites_api'),  # 追加
]
urlpatterns += [
    path('favorites_list_api/', views.favorites_list_api, name='favorites_list_api'),
]