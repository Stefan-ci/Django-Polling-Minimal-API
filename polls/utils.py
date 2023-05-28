from drf_yasg import openapi

def polls_query_parameters() -> list:
    page = openapi.Parameter("page", openapi.IN_QUERY, description="Page", type=openapi.TYPE_INTEGER)
    return [page]


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
