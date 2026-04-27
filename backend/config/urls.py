from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/modules/', include('modules_app.urls')),
    path('api/certificates/', include('certificates.urls')),
    path('api/locations/', include('locations.urls')),
]