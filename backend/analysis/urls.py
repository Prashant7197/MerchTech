from django.urls import path
from .views import analyze_all, analyze_product
from .views_insights import get_auto_insights

urlpatterns = [
    path("analyze/", analyze_all, name="analyze_all"),
    path("analyze/<str:asin>/", analyze_product, name="analyze_product"),
    path("auto-insights/", get_auto_insights, name="auto_insights"),
]
