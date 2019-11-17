from django.shortcuts import render
from scraping_recetas_app.models import Receta, Categoria, PreparacionReceta, IngredienteReceta
from scraping_recetas_app.serializers import CategoriaSerializer, RecetaSerializer, CategoriaConRecetasSerializer
from rest_framework import generics, viewsets, filters
from django_filters import rest_framework


class RecetaViewSet(viewsets.ReadOnlyModelViewSet):
    __doc__ = (u"""
    Lista con todas las recetas. Filtros:
    
    - categoría: Dado el ID de una categoría, podemos filtrar todas las recetas de esa categoría. Por ejemplo
    [/recetas?categoria=36](?categoria=36) nos devolvería todas las recetas de la categoría 'Verduras'. Podemos
    ver todas las categorías y sus IDs en [/categorias/recetas/](/categorias/recetas/)
    - ingredientes: Podemos filtrar por los ingredientes de las recetas. Por ejemplo, si queremos las recetas que tengan
    como ingredientes acelgas o leche aplicaríamos el filtro [/recetas?ingrediente=acelgas&ingrediente=leche](?ingrediente=acelgas&ingrediente=leche)
    """)

    def get_view_name(self):
        return 'Recetas'

    serializer_class = RecetaSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['titulo', ]
    ordering_fields = ['titulo', 'categoria']
    filter_fields = ['categoria', ]

    def get_queryset(self):
        ingredientes = self.request.GET.getlist('ingrediente')
        if ingredientes is None or ingredientes == []:
            return Receta.objects.all()
        objs_ingredientes = []
        for i in ingredientes:
            objs_ingredientes.extend(IngredienteReceta.objects.filter(ingrediente__contains=i))

        id_recetas = [ing.receta_id for ing in objs_ingredientes]
        return Receta.objects.filter(id__in=id_recetas)


class CategoriaListView(generics.ListAPIView):
    def get_view_name(self):
        return 'Categorías'

    serializer_class = CategoriaConRecetasSerializer
    queryset = Categoria.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = ['nombre', ]
    ordering_fields = ['nombre', ]
