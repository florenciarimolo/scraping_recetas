from django.shortcuts import render
from scraping_recetas_app.models import Receta, Categoria, PreparacionReceta, IngredienteReceta
from scraping_recetas_app.serializers import CategoriaSerializer, RecetaSerializer
from rest_framework import generics, viewsets
from rest_framework import filters


class RecetaListView(viewsets.ModelViewSet):
    def get_view_name(self):
        return 'Recetas'

    serializer_class = RecetaSerializer
    queryset = Receta.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering = ('titulo')
    ordering_fields = ('titulo')


class RecetaView(generics.RetrieveAPIView):
    def get_view_name(self):
        return 'Receta'

    serializer_class = RecetaSerializer
    queryset = Receta.objects.all()
    lookup_field = 'pk'
