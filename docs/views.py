from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _


api_documentation = get_schema_view(
    openapi.Info(
        title=f"Django Polls API",
        default_version="1.0",
        description=_("Offcial documentation of Django Polls API."),
        terms_of_service="",
        contact=openapi.Contact(email="john@doe.io", name="John DOE"),
        license=openapi.License(name=_("GNU License.")),
    ),
    public=True,
    permission_classes=[AllowAny],
)
