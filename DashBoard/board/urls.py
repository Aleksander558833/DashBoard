from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, ResponseList, ResponseCreate, \
    ResponseDelete, response_status

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('response/', ResponseList.as_view(), name='response_list'),
    path('response/<int:pk>/create/', ResponseCreate.as_view(), name='response_create'),
    path('response/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('response/<int:pk>/status/', response_status, name='response_status'),
]

