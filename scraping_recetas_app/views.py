from django.shortcuts import render
from scraping_recetas_app.models import Receta, Categoria, PreparacionReceta, IngredienteReceta
from scraping_recetas_app.serializers import CategoriaSerializer, RecetaSerializer, CategoriaConRecetasSerializer
from rest_framework import generics, viewsets, filters


class RecetaViewSet(viewsets.ReadOnlyModelViewSet):
    def get_view_name(self):
        return 'Recetas'

    serializer_class = RecetaSerializer
    queryset = Receta.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['titulo', ]
    ordering_fields = ['titulo', 'categoria']


class CategoriaListView(generics.ListAPIView):
    def get_view_name(self):
        return 'Categorias'

    serializer_class = CategoriaConRecetasSerializer
    queryset = Categoria.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['categoria', ]
    ordering_fields = ['categoria', ]
