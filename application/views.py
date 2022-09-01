from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SampleSerializer
from .models import SampleModel
from .permissions import AccessProductTwo, AccessProductOne

# Create your views here.
class SampleView(APIView):
    def get(self, request):
        queryset = SampleModel.objects.all()
        serializer = SampleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SampleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ProductOne(APIView):
    permission_classes = [IsAuthenticated, AccessProductOne]

    def get(self, request):
        return Response({"product": "one"})


class ProductTwo(APIView):
    permission_classes = [IsAuthenticated, AccessProductTwo]

    def get(self, request):
        return Response({"product": "two"})
