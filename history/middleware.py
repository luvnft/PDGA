from django.http import HttpResponse
from django.core.cache import cache
from django.conf import settings
from django.urls import resolve

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is a POST to the specific view
        if request.method == 'POST' and resolve(request.path_info).view_name == 'index':
            ip_address = request.META.get('REMOTE_ADDR')
            cache_key = f'ratelimit_{ip_address}'
            
            # Get the current request count for this IP
            request_count = cache.get(cache_key, 0)

            # Define your rate limit (e.g., 5 requests per minute)
            rate_limit = getattr(settings, 'RATE_LIMIT', 5)
            rate_limit_period = 60  # 1 minute

            if request_count >= rate_limit:
                return HttpResponse("Rate limit exceeded. Please try again later.", status=429)

            # Increment the request count
            cache.set(cache_key, request_count + 1, rate_limit_period)

        response = self.get_response(request)
        return response