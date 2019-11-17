# coding=utf-8
from rest_framework import serializers
from rest_framework.reverse import reverse

from scraping_recetas_app.models import Receta, Categoria, IngredienteReceta, PreparacionReceta


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class RecetaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    ingredientes = serializers.SlugRelatedField(
        many=True,
        queryset=IngredienteReceta.objects.all(),
        slug_field='ingrediente')

    preparacion = serializers.SlugRelatedField(
        many=True,
        queryset=PreparacionReceta.objects.all().order_by('orden'),
        slug_field='descripcion')

    class Meta:
        model = Receta
        fields = ['id', 'categoria', 'ingredientes', 'preparacion' ,'titulo', 'descripcion', 'comensales', 'duracion', 'tipo_comida', ]
