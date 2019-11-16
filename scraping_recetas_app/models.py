from django.db import models


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'categoria'


class Receta(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    comensales = models.IntegerField(null=True)
    duracion = models.CharField(max_length=20, null=True)
    tipo_comida = models.CharField(max_length=50, null=True)
    categoria = models.ForeignKey(Categoria, related_name='receta', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'receta'


class IngredienteReceta(models.Model):
    receta = models.ForeignKey(Receta, related_name='ingrediente', on_delete=models.CASCADE)
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
