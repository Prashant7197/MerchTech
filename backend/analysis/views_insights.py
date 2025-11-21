import os
import json
from django.http import JsonResponse
from django.conf import settings

def get_auto_insights(request):
    file_path = os.path.join(getattr(settings, "DATA_DIR"), "insights_auto.json")

    if not os.path.exists(file_path):
        return JsonResponse({"error": "Insights file not generated yet"}, status=404)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return JsonResponse(data, safe=False)
