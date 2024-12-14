from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.views import View
import json
from .models import Robot
import logging
from datetime import datetime, timedelta

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

    def post(self, request):
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
            return HttpResponse({"error": "Invalid model."}, status=400)

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


# -------------------------------------------------------------------------------------------------------------
"""Task 2."""


import pandas as pd


class RobotExcel(View):
    def get(self, request):
        """
        Processes GET requests to generate and download an Excel file with a summary of robot production for the last week.

        Args:
            request: Request object.
        Returns:
            HttpResponse: Excel file to download.
        """
        robots_data = self.get_robots_data()
        excel_file_path = self.create_excel_file(robots_data)
        return self.send_excel_file(excel_file_path)

    def get_robots_data(self):
        """
        Gets robot production data for the last week.

        Returns:
            dict: A dictionary containing data about robot models and versions.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        robots = Robot.objects.filter(created__range=[start_date, end_date])
        data = {}

        for robot in robots:
            model = robot.model
            version = robot.version

            if model not in data:
                data[model] = {}

            if version not in data[model]:
                data[model][version] = 0
            data[model][version] += 1

        return data

    def create_excel_file(self, data):
        """
        Creates an Excel file with a summary of robot production.

        Args:
            data (dict): Data about robot models and versions.

        Returns:
            str: Path to the created Excel file.
        """
        excel_file_path = "robots.xlsx"
        with pd.ExcelWriter(excel_file_path) as writer:
            for model, versions in data.items():
                df = pd.DataFrame(
                    list(versions.items()), columns=["Версия", "Количество за неделю"]
                )
                df.insert(0, "Модель", model)
                df.to_excel(writer, sheet_name=model, index=False)

        return excel_file_path

    def send_excel_file(self, file_path):
        """
        Sends an Excel file to the user.

        Args:
            file_path (str): Path to the Excel file.

        Returns:
            HttpResponse: Response with the file to download.
        """
        with open(file_path, "rb") as f:
            response = HttpResponse(
                f.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=robots.xlsx"
            return response
