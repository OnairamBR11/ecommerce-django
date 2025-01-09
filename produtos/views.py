from django.shortcuts import render
from rest_framework import generics
from .models import Produto
from .serializers import ProdutoSerializer

class ProdutoListCreateView(generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# Create your views here.
