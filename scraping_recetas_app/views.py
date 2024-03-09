from collections import OrderedDict

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.reverse import reverse

from scraping_recetas_app.models import Receta, Categoria, IngredienteReceta, Subcategoria
from scraping_recetas_app.serializers import RecetaSerializer, CategoriaConSubcategoriasSerializer, SubcategoriaConRecetasSerializer, SubcategoriaSerializer
from rest_framework import generics, viewsets, filters
from django_filters import rest_framework


class APIRoot(generics.GenericAPIView):
    __doc__ = ("""
    Esta API muestra la información de las recetas obtenidas en la web [https://www.recetasgratis.net/](https://www.recetasgratis.net/).
    """)

    def get_view_name(self):
        return 'API Recetas'

    def get(self, request, format=None):
        data = OrderedDict((
            ('categorias', reverse('scraping_recetas_app:categorias-recetas', request=request, format=format)),
        ))
        return Response(data, )

class CategoriaListView(generics.ListAPIView):
    __doc__ = ("""
    Lista de categorías de recetas. 
    
    Filtros:
               
    - Nombre: se puede utilizar un filtro de búsqueda por nombre, por ejemplo [/categorias?search=aperitivo](?search=aperitivo),
               que buscaría todas las categorías que contengan "aperitivo" como nombre. 
               
    Ordenación:
               
    - Nombre: ascendente
               [/categorias?ordering=nombre](?ordering=nombre) y descendente [/categorias?ordering=-nombre](?ordering=-nombre)
    """)
    def get_view_name(self):
        return 'Categorías'

    serializer_class = CategoriaConSubcategoriasSerializer
    queryset = Categoria.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['nombre', ]
    ordering_fields = ['nombre', ]
    search_fields = ['nombre', ]

class SubcategoriaListView(generics.ListAPIView):
    serializer_class = SubcategoriaSerializer
    __doc__ = ("""
    Lista de subcategorías para una categoría de recetas. 
            
    Filtros:
               
    - Nombre: se puede utilizar un filtro de búsqueda por nombre, por ejemplo [subcategorias?search=patata](?search=patata),
               que buscaría todas las categorías que contengan "patata" como nombre.
               
    Ordenación:
               
    - Nombre: ascendente
    [subcategorias?ordering=nombre](?ordering=nombre) y descendente [subcategorias?ordering=-nombre](?ordering=-nombre)
    """)
    def get_view_name(self):
        return 'Subcategorías'
    
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['id', ]
    ordering_fields = ['nombre', ]
    search_fields = ['nombre', ]
    
    def get_queryset(self):
        id_categoria = self.kwargs['id_categoria']
        return Subcategoria.objects.filter(categoria__id=id_categoria)

class SubcategoriaView(generics.RetrieveAPIView):
    serializer_class = SubcategoriaConRecetasSerializer
    def get_view_name(self):
        return 'Subcategoría'
    
    queryset = Subcategoria.objects.all()
        
class RecetaListView(generics.ListAPIView):
    __doc__ = (u"""
    Lista con todas las recetas de una subcategoría. 
    
    Filtros:

    - Ingredientes: podemos filtrar por los ingredientes de las recetas. Por ejemplo, si queremos las recetas que tengan
    como ingredientes acelgas o leche aplicaríamos el filtro [recetas?ingrediente=acelgas&ingrediente=leche](?ingrediente=acelgas&ingrediente=leche)
    
    Ordenación:

    - Título: ascendente [recetas?ordering=titulo](?ordering=titulo) y descendente [recetas?ordering=-titulo](?ordering=-titulo).
    """)

    filter_backends = [filters.OrderingFilter]
    ordering = ['titulo', ]
    ordering_fields = ['titulo', ]

    serializer_class = RecetaSerializer
    def get_view_name(self):
        return 'Recetas'
    
    def get_queryset(self):
        id_subcategoria = self.kwargs['id_subcategoria']

        ingredientes = self.request.GET.getlist('ingrediente')
        if ingredientes is None or ingredientes == []:
            return Receta.objects.filter(subcategoria__id=id_subcategoria)
        objs_ingredientes = []
        for i in ingredientes:
            objs_ingredientes.extend(IngredienteReceta.objects.filter(receta__subcategoria__id=id_subcategoria, ingrediente__contains=i))

        id_recetas = [ing.receta_id for ing in objs_ingredientes]
        return Receta.objects.filter(id__in=id_recetas)
    
    
class RecetaView(generics.RetrieveAPIView):
    serializer_class = RecetaSerializer
    def get_view_name(self):
        return 'Receta'
    
    queryset = Receta.objects.all()
