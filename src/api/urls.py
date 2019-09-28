from django.urls import include, path

from api.auth.views import LoginView, SignupView, ChangePasswordView, SendResetPasswordEmailView, ResetPasswordView
from api.matches.views import MatchesView
from api.videos.views import VideosView
from api.highlights.views import HighlightsView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('send_reset_password_email/', SendResetPasswordEmailView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('matches/', MatchesView.as_view()),
    path('videos/', VideosView.as_view()),
    path('highlights/', HighlightsView.as_view()),
]
