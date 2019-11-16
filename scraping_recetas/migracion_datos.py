# coding=utf-8
import django

django.setup()
from scraping_recetas.extraccion_datos import extraccion_datos
from scraping_recetas_app.models import Receta, Categoria, IngredienteReceta, PreparacionReceta
from django.db import transaction


@transaction.atomic
def migracion_datos():
    sid = transaction.savepoint()
    datos = extraccion_datos()
    print("Iniciando extracción...")
    for categoria, recetas in datos.items():
        print("Guardando categoría: " + categoria)
        try:
            c = Categoria(categoria=categoria)
            c.save()
        except Exception as e:
            print(str(e))
            transaction.savepoint_rollback(sid)
            break

        for r in recetas:
            titulo = r.get("titulo")
            tipo_comida = r.get("tipo_comida")
            comensales = r.get("comensales")
            duracion = r.get("duracion")
            ingredientes = r.get("ingredientes")
            descripcion = r.get("descripcion")
            prepacacion = r.get("preparacion")
            try:
                rec = Receta(titulo=titulo, tipo_comida=tipo_comida, comensales=comensales, duracion=duracion,
                             descripcion=descripcion, categoria=c)
                rec.save()
            except Exception as e:
                print(str(e))
                transaction.savepoint_rollback(sid)
                break

            for i in ingredientes:
                try:
                    IngredienteReceta(receta=rec, ingrediente=i).save()
                except Exception as e:
                    print(str(e))
                    transaction.savepoint_rollback(sid)
                    break

            for p in prepacacion:
                try:
                    PreparacionReceta(receta=rec, orden=p.get("orden"), descripcion=p.get("descripcion")).save()
                except Exception as e:
                    print(str(e))
                    transaction.savepoint_rollback(sid)
                    break

    print("Guardado con éxito.")


if __name__ == "__main__":
    migracion_datos()
