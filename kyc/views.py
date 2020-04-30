from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from .serializers import InputSerializer, OutputSerializer
from .models import Input, Output
from .tasks import process_pan


class KYCApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = InputSerializer
    queryset = Input.objects.all()
    def post(self, requests):
        serializer = InputSerializer(data=requests.data)
        if serializer.is_valid():
            input_query = serializer.save()
            print(input_query)
            out = process_pan(input_query)
            return Response(OutputSerializer(out).data)
        else:
            return Response(serializer.errors)