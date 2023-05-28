from drf_yasg import openapi
from django.http import Http404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import Response, APIView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from polls.models import Poll, Answer
from polls.utils import polls_query_parameters, get_client_ip
from polls.serializers import PollSerializer, PollListSerializer, CreatePollSerializer




class PollListView(APIView):
    """ List active polls in DB (API View) """
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(manual_parameters=polls_query_parameters(), responses={200: PollListSerializer})
    def get(self, request, format=None):
        """ GET Active Polls """
        
        polls = Poll.objects.filter(is_active=True)
        
        paginator = Paginator(polls, 10)
        page = request.GET.get("page")
        polls_obj = paginator.get_page(page)
        try:
            polls = paginator.page(page)
        except PageNotAnInteger:
            polls = paginator.page(1)
        except EmptyPage:
            polls = paginator.page(paginator.num_pages)
        
        data = {
            "total_pages": paginator.num_pages,
            "current_page": polls_obj.number,
            "has_next": polls_obj.has_next(),
            "has_prev": polls_obj.has_previous(),
            "page_items_count": polls_obj.__len__(),
            "items_per_page": paginator.per_page,
            "data": PollListSerializer(polls_obj, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        "question": openapi.Schema(type=openapi.TYPE_STRING, description="Poll's question"),
        "answers": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="List of answers to this question (minimum 1)")
    }), responses={200: PollSerializer})
    def post(self, request, format=None):
        """ Create a new Poll with answers """
        if request.user.is_authenticated and request.user.is_superuser:
            serializer = CreatePollSerializer(data=request.data)
            if serializer.is_valid():
                serialized_data = serializer.validated_data
                
                poll = Poll.objects.create(
                    question=serialized_data["question"],
                    is_active=True,
                    extra_data={
                        "HEADERS":{
                            "User-Agent": request.headers["User-Agent"],
                            "ABSOLUTE_URI": request.build_absolute_uri()
                        },
                        "METADATA": {
                            "CREATED_WITH": "API",
                            "IP_ADDRESS": get_client_ip(request),
                            "CONTENT_LENGTH": request.META["CONTENT_LENGTH"],
                            "CONTENT_TYPE": request.META["CONTENT_TYPE"],
                            "HTTP_ACCEPT": request.META["HTTP_ACCEPT"],
                            "HTTP_ACCEPT_ENCODING": request.META["HTTP_ACCEPT_ENCODING"],
                            "HTTP_HOST": request.META["HTTP_HOST"],
                            "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"],
                            "QUERY_STRING": request.META["QUERY_STRING"],
                            "REMOTE_ADDR": request.META["REMOTE_ADDR"],
                            "REMOTE_HOST": request.META["REMOTE_HOST"],
                            "REQUEST_METHOD": request.META["REQUEST_METHOD"],
                            "SERVER_NAME": request.META["SERVER_NAME"],
                            "SERVER_PORT": request.META["SERVER_PORT"],
                        },
                    }
                )
                
                for answer in serialized_data["answers"]:
                    Answer.objects.create(
                        poll=poll,
                        answer=answer,
                        is_active=True
                    )
                
                data = {
                    "data": PollSerializer(poll, many=False).data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # serializer is not valid
        return Response({"msg": "You're unauthorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED) # User is not superuser







class PollDetailView(APIView):
    """ Detail active poll in DB (API View) """
    permission_classes = [AllowAny]
    
    def get_poll(self, slug, pk):
        try:
            return Poll.objects.get(slug=slug, pk=pk)
        except Poll.DoesNotExist:
            raise Http404
    
    @swagger_auto_schema(responses={200: PollSerializer})
    def get(self, request, slug, pk, format=None):
        """ GET Details of current Poll with its similar polls """
        data = {
            "data": PollSerializer(self.get_poll(slug, pk), many=False).data,
        }
        return Response(data, status=status.HTTP_200_OK)
