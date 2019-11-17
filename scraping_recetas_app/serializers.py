# coding=utf-8
from rest_framework import serializers
from rest_framework.reverse import reverse

from scraping_recetas_app.models import Receta, Categoria, IngredienteReceta, PreparacionReceta


class CategoriaConRecetasSerializer(serializers.ModelSerializer):
    recetas = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='scraping_recetas_app:receta-detail'
    )

    class Meta:
        model = Categoria
        fields = ['categoria', 'recetas']


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

    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request', None)
        format = self.context.get('format', None)
        kwargs = {'pk': obj.id}
        return reverse('scraping_recetas_app:receta-detail', request=request, format=format,
                       kwargs=kwargs)

    class Meta:
        model = Receta
        fields = ['id', 'categoria', 'ingredientes', 'preparacion', 'titulo', 'descripcion', 'comensales', 'duracion',
                  'tipo_comida', 'url']
