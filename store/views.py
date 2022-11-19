from store.serializers import ProductSerializer
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from store.models import Product


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer



# class ProductViewSet(ModelViewSet):
#     queryset= Product.objects.all()
#     serializer_class = ProductSerializer