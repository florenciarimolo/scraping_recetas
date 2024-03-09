# coding=utf-8
from rest_framework import serializers
from rest_framework.reverse import reverse

from scraping_recetas_app.models import Receta, Categoria, IngredienteReceta, PreparacionReceta, Subcategoria

class SubcategoriaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'id_categoria': obj.categoria.id}
        return reverse('scraping_recetas_app:subcategoria-detail', request=request, format=format,
                       kwargs=kwargs)
    class Meta:
        model = Subcategoria
        fields = ['id', 'nombre', 'url']

class CategoriaConSubcategoriasSerializer(serializers.ModelSerializer):
    subcategorias = SubcategoriaSerializer(many=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'subcategorias']

class SubcategoriaConRecetasSerializer(serializers.ModelSerializer):
    recetas = serializers.SerializerMethodField()

    def get_recetas(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'id_subcategoria': obj.id, 'id_categoria': obj.categoria.id}
        return reverse('scraping_recetas_app:receta-list', request=request, format=format,
                       kwargs=kwargs)

    class Meta:
        model = Subcategoria
        fields = ['id', 'nombre', 'recetas']


class RecetaSerializer(serializers.ModelSerializer):
    subcategoria = SubcategoriaSerializer
    ingredientes = serializers.SlugRelatedField(
        many=True,
        queryset=IngredienteReceta.objects.all(),
        slug_field='ingrediente')

    preparacion = serializers.SlugRelatedField(
        many=True,
        queryset=PreparacionReceta.objects.all().order_by('orden'),
        slug_field='descripcion')

    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id, 'id_subcategoria': obj.subcategoria.id, 'id_categoria': obj.subcategoria.categoria.id}
        return reverse('scraping_recetas_app:receta-detail', request=request, format=format,
                       kwargs=kwargs)

    class Meta:
        model = Receta
        fields = ['id', 'subcategoria', 'ingredientes', 'preparacion', 'titulo', 'descripcion', 'comensales', 'duracion',
                  'tipo_comida', 'url']
