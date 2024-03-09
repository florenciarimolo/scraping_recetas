from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'categoria'

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, related_name='subcategorias', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'subcategoria'

class Receta(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    comensales = models.IntegerField(null=True)
    duracion = models.CharField(max_length=20, null=True)
    tipo_comida = models.CharField(max_length=50, null=True)
    subcategoria = models.ForeignKey(Subcategoria, related_name='recetas', on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = 'receta'


class IngredienteReceta(models.Model):
    receta = models.ForeignKey(Receta, related_name='ingredientes', on_delete=models.CASCADE)
    ingrediente = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'ingrediente_receta'


class PreparacionReceta(models.Model):
    receta = models.ForeignKey(Receta, related_name='preparacion', on_delete=models.CASCADE)
    orden = models.IntegerField()
    descripcion = models.TextField()

    class Meta:
        managed = True
        db_table = 'preparacion_receta'
