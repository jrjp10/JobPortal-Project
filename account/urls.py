from django.urls  import path, include
from .import views
from account.views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login' ),
]
