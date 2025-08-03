from django.shortcuts import redirect


def toggle_dark_mode(request):
    request.session["dark_mode"] = not request.session.get("dark_mode", False)
    return redirect(request.META.get("HTTP_REFERER", "/"))
