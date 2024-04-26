from django.urls import path
from .views import get_friends, create_harem, get_harem, join_harem, delete_harem, leave_harem


urlpatterns = [
    path('<int:id>/friends/', get_friends),
    path('<int:id>/harem/create/', create_harem),
    path('harem/<str:name>/', get_harem),
    path('<int:id>/harem/join/', join_harem),
    path('<int:id>/harem/delete/<str:name>/<str:password>/', delete_harem),
    path('<int:id>/harem/leave/<str:name>/', leave_harem)
]
