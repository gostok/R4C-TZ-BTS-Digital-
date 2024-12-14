from django.urls import path
from .views import RobotView, RobotJson, JsonView, RobotApiView


app_name = "robots"

urlpatterns = [
    path("", RobotView.as_view(), name="robot_view"),
    path(
        "json/", JsonView.as_view(), name="json_view"
    ),  # To display robots in JSON format
    path("download/", RobotJson.as_view(), name="robot_json"),  # To download JSON
    path(
        "api/robots/", RobotApiView.as_view(), name="robot_api"
    ),  # endpoint for working with JSON with API
]
