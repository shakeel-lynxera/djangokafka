from django.urls import path, include

urlpatterns = [
    path("driver/", include("driver.urls")),
    path("shifts/", include("shifts.urls")),
    path("jobs/", include("jobs.urls")),
    path("tools/", include("tools.urls")),
    path("audit-logs/", include("audit_logs.urls")),
    path("driver-mobile-app/", include("driver_mobile_app.urls")),
    path("reports/",include("reports.urls"))
]
