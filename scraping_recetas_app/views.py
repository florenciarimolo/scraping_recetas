from django.shortcuts import render
from scraping_recetas_app.models import Receta, Categoria, PreparacionReceta, IngredienteReceta
from scraping_recetas_app.serializers import CategoriaSerializer, RecetaSerializer, CategoriaConRecetasSerializer
from rest_framework import generics, viewsets, filters
from django_filters import rest_framework


class RecetaViewSet(viewsets.ReadOnlyModelViewSet):
    def get_view_name(self):
        return 'Recetas'

    serializer_class = RecetaSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['titulo', ]
    ordering_fields = ['titulo', 'categoria']
    filter_fields = ['categoria', 'ingredientes']

    def get_queryset(self):
        ingredientes = self.request.GET.getlist('ingrediente')
        if ingredientes is None:
            return Receta.objects.all()
        objs_ingredientes = []
        for i in ingredientes:
            objs_ingredientes.extend(IngredienteReceta.objects.filter(ingrediente__contains=i))

        id_recetas = [ing.receta_id for ing in objs_ingredientes]
        return Receta.objects.filter(id__in=id_recetas)


class CategoriaListView(generics.ListAPIView):
    def get_view_name(self):
        return 'Categorias'

    serializer_class = CategoriaConRecetasSerializer
    queryset = Categoria.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['categoria', ]
    ordering_fields = ['categoria', ]
