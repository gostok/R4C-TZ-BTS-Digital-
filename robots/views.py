from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
import json
from .models import Robot
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

VALID_MODELS = ["R2", "13", "X5"]


class RobotView(View):
    template_name = "robots/index.html"

    def get(self, request):
        """
        Handles GET requests to display robot cards.

        Args:
        request: The request object.

        Returns:
        HttpResponse: Displays the page with robot cards.
        """
        robots = Robot.objects.all()
        return render(request, self.template_name, {"robots": robots})

    def post_form(self, request):
        """
        Processes POST requests to create a new robot in the form.

        Args:
        request: The request object.

        Returns:
        HttpResponse: Redirects to the page with robot cards or returns an error.
        """
        model = request.POST.get("model")
        version = request.POST.get("version")
        created = request.POST.get("created")

        # Input data validation
        if model not in VALID_MODELS:
            return JsonResponse({"error": "Invalid model."}, status=400)

        # Creating a new robot
        robot = Robot(model=model, version=version, created=created)
        robot.save()

        return redirect("robots:robot_view")  # Redirect to a page with a list of robots


class RobotApiView(View):
    @csrf_exempt
    def post(self, request):
        """
        Handles POST requests to create a new robot via the API.

        Args:
        request: The request object.

        Returns:
        JsonResponse: A response with a success or error message.
        """
        try:
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")

            model = data.get("model")
            version = data.get("version")
            created = data.get("created")

            # Input data validation
            if model not in VALID_MODELS:
                return JsonResponse({"error": "Invalid model."}, status=400)

            # Converting a date string to a datetime object
            created_date = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")

            # Creating a new robot
            robot = Robot(model=model, version=version, created=created_date)
            robot.save()

            return JsonResponse({"message": "Robot created successfully."}, status=201)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received.")
            return JsonResponse({"error": "Invalid JSON."}, status=400)
        except ValueError as ve:
            logger.error(f"Date format error: {ve}")
            return JsonResponse({"error": "Invalid date format."}, status=400)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)


class RobotJson(View):
    def get(self, request):
        """
        Processes GET requests to return a list of robots in JSON format.

        Args:
        request: The request object.

        Returns:
        JsonResponse: A list of robots in JSON format with a download button.
        """
        robots = Robot.objects.all()
        robots_list = [
            {
                "model": robot.model,
                "version": robot.version,
                "created": robot.created.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for robot in robots
        ]

        response = JsonResponse(robots_list, safe=False)

        response["Content-Disposition"] = 'attachment; filename="robots.json"'

        return response


class JsonView(View):
    template_name = "robots/json_view.html"

    def get(self, request):
        """
        Processes GET requests to display a list of robots in JSON format on a web page.

        Args:
        request: The request object.

        Returns:
        HttpResponse: Displays a page with JSON data of the robots.
        """
        robots = Robot.objects.all()
        robots_list = [
            {
                "model": robot.model,
                "version": robot.version,
                "created": robot.created.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for robot in robots
        ]
        json_data = json.dumps(robots_list, ensure_ascii=False, indent=4)
        return render(request, self.template_name, {"json_data": json_data})
