from django.urls import path
from .views import UserLoginView, UserSignupView, UserProfileView,UserProfileEditView, UserLogoutView, ActivateAccount 
app_name = 'accounts'

urlpatterns = [
    
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('signup/', UserSignupView.as_view(), name = 'signup'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name = 'profile'),
    path('profile-edit/<slug:slug>/', UserProfileEditView.as_view(), name = 'profile-edit'),
    path('logout/', UserLogoutView, name ='logout'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]