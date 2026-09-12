from django.urls import path
from . import views 

urlpatterns = [
    path(
        '',
        views.scanner,
        name='scanner'
    ),
     path(
            'dashboard/',
            views.dashboard,
            name='dashboard'
        ),
     path(
            'dashboard/clear/',
            views.clear_scans,
            name='clear_scans'
        ),
]