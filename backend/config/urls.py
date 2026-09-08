from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

def health_check(request):
    return JsonResponse({"status": "ok", "service": "cracked-backend"})

urlpatterns = [
    path("", health_check),
    path("healthz", health_check),
    path("api/healthz", health_check),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("curriculum.urls")),
    path("api/", include("progress.urls")),
    # Support /api/backend/ prefix for Vercel service rewrites
    path("api/backend/healthz", health_check),
    path("api/backend/auth/", include("accounts.urls")),
    path("api/backend/api/auth/", include("accounts.urls")),
    path("api/backend/api/", include("curriculum.urls")),
    path("api/backend/api/", include("progress.urls")),
    path("api/backend/", include("curriculum.urls")),
    path("api/backend/", include("progress.urls")),
]
