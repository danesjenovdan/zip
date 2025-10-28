import json

from django.http import JsonResponse
from django.views.generic import View

from .mailerlite import add_subscriber


class SubscribeToNewsletter(View):
    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return JsonResponse({"message": "Invalid content type"}, status=400)

        try:
            data = json.loads(request.body)
            email = data.pop("email")
            if not email:
                return JsonResponse({"message": "Email is required"}, status=400)
            consent = data.pop("consent", False) == "on"
            if not consent:
                return JsonResponse({"message": "Consent is required"}, status=400)
            group_names = [key for key in data if data[key] == "on"]
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        error, response = add_subscriber(email, group_names)
        if error and "message" in error:
            return JsonResponse({"message": error["message"]}, status=500)

        print(f"MailerLite response: error={error}, response={response}")

        status = response.get("data", {}).get("status", None)
        return JsonResponse({"data": {"status": status}}, status=200)
