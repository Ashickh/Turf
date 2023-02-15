from django.contrib import admin
from django.urls import path
from Turff import views

from django.conf import settings
from django.conf.urls.static import static

# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('turf/user/registration',views.UserView.as_view()),
    path('turf/ground',views.GroundView.as_view()),
    path('turf/pitch', views.PitchView.as_view()),
    path('turf/timeslot',views.TimeSlotView.as_view()),
    path('turf/timeslot/<id>',views.TimeSlotDetailView.as_view()),
    path('turf/booking_dates',views.BookingDatesView.as_view()),
    path('turf/booking_dates/<id>',views.BookingDatesDetailView.as_view()),
    path('turf/booking',views.BookingView.as_view()),
    path('turf/teams',views.TeamsView.as_view()),
    path('turf/teams/<int:id>',views.TeamsView.as_view()),
    path('turf/matches',views.MatchView.as_view()),
    path('turf/matches/<int:id>',views.MatchView.as_view()),
    path('turf/league',views.LeagueView.as_view()),
    path('turf/booking/<id>',views.BookingDetailView.as_view()),
    path('turf/login', TokenObtainPairView.as_view()),
    path('turf/token/refresh', TokenRefreshView.as_view()),
    


] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)