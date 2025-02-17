from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json

from .models import Test, TestAttempt, Course
from .utils import generate_diff_html_and_stats


@csrf_exempt  # Remove this if using frontend CSRF token properly
@login_required
def attempt_test_api(request, test_id):
    """API endpoint for submitting a typing or steno test attempt."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            orig_text = data.get("orig_text")
            typed_text = data.get("typed_text")
            duration_seconds = float(data.get("duration_seconds", 0))

            test = get_object_or_404(Test, id=test_id)

            # Generate diff and stats
            diff_html, stats = generate_diff_html_and_stats(
                original_text=orig_text,
                typed_text=typed_text,
                duration_seconds=duration_seconds,
            )

            # Save the attempt in the database
            attempt = TestAttempt.objects.create(
                user=request.user,
                test=test,
                score=stats.get("score", 0),
                time_taken=int(duration_seconds),
                user_input=typed_text,
                extra_info=stats,
            )

            return JsonResponse(
                {"diff_html": diff_html, "stats": stats, "attempt_id": attempt.id},
                status=200,
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def attempt_test_page(request, test_id):
    """Render the test-taking page where users can attempt a test."""
    # Reject non-GET requests
    if request.method != "GET":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    test = get_object_or_404(Test, id=test_id)

    # Check if the user has already attempted this test
    attempt = TestAttempt.objects.filter(user=request.user, test=test).first()
    has_attempted = attempt is not None

    return render(
        request, "attempt_test.html", {"test": test, "has_attempted": has_attempted}
    )


@login_required
def user_dashboard(request):
    return render(request, "dashboard.html")
