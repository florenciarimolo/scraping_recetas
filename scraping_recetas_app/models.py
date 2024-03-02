from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'categoria'
        app_label = 'scraping_recetas'


class Receta(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    comensales = models.IntegerField(null=True)
    duracion = models.CharField(max_length=20, null=True)
    tipo_comida = models.CharField(max_length=50, null=True)
    categoria = models.ForeignKey(Categoria, related_name='recetas', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'receta'
        app_label = 'scraping_recetas'


class IngredienteReceta(models.Model):
    receta = models.ForeignKey(Receta, related_name='ingredientes', on_delete=models.CASCADE)
    ingrediente = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'ingrediente_receta'
        app_label = 'scraping_recetas'


class PreparacionReceta(models.Model):
    receta = models.ForeignKey(Receta, related_name='preparacion', on_delete=models.CASCADE)
    orden = models.IntegerField()
    descripcion = models.TextField()

    class Meta:
        managed = True
        db_table = 'preparacion_receta'
        app_label = 'scraping_recetas'
