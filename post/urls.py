from django.urls import path
from . import views

urlpatterns = [
    path('create_post', views.create_post, name='create_post'),
    path('view_post/<post_id>/', views.view_post, name='view_post'),
    path('edit_post/<post_id>', views.edit_post, name='edit_post'),
    path('compare', views.compare, name='compare'),
    path('delete/<post_id>', views.delete, name='delete')
]
