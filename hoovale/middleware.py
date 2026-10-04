"""Small production middleware for HOOVALE's canonical host.

Render handles HTTPS termination and custom-domain redirects. We therefore
avoid doing a host redirect here, which can loop when proxy headers differ.
"""

class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
