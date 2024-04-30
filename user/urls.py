from django.urls import path
from .views import get_friends, create_harem, get_harem, join_harem, delete_harem, leave_harem, get_statistics, get_button, select_button
from market.views import get_tasks, get_boosts, get_boost, buy_boost

urlpatterns = [
    path('friends/', get_friends),
    path('harem/create/', create_harem),
    path('harem/<str:name>/', get_harem),
    path('harem/join/', join_harem),
    path('harem/delete/<str:name>/<str:password>/', delete_harem),
    path('harem/leave/<str:name>/', leave_harem),
    path('statistics/', get_statistics),
    path('tasks/', get_tasks),
    path('boosts/<str:extra>', get_boosts),
    path('boost/<str:name>/', get_boost),
    path('buy/<str:name>/', buy_boost),
    path('select/<str:name>/', select_button),
    path('button/', get_button)
]
