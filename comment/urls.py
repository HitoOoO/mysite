from django.urls import path
from .views import Update_comment

urlpatterns = [
    path('Update_comment',Update_comment.as_view(), name='Update_comment'),
]