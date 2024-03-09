# coding=utf-8
from bs4 import BeautifulSoup
import requests
import requests_cache

# Guardaremos las peticiones en cache, para no tener que hacerlas cada vez que se ejecuta el script
from rest_framework.utils import json

requests_cache.install_cache('cache', backend='sqlite', expire_after=-1)


def get_datos():
    """
    Este método realiza web scraping sobre la web https://www.recetasgratis.net/ para obtener toda la información de
    las recetas de la página.
    :return: Un diccionario donde la key es el nombre de la categoría de las recetas y el valor otro diccionario con
    la información de las recetas.
    """
    # Cogemos todos los links de las categorias

    html_inicio = requests.get('https://www.recetasgratis.net/')
    html_inicio_soup = BeautifulSoup(html_inicio.text, features="html.parser")
    categorias_resultset = html_inicio_soup.findAll("div", {"class": "categoria ga"})
    recetas = {}

    for categoria in categorias_resultset:
        nombre_categoria = categoria.find("a", {"class": "titulo"}).text.replace('Recetas de', '').strip()
        if nombre_categoria == 'Consejos de cocina':
            continue

        print('Obteniendo datos de la categoría ' + nombre_categoria)

        subcategorias = categoria.find("ul", {"class": "sub-categorias"}).findAll("li")
        recetas[nombre_categoria] = {}

        for subcategoria in subcategorias:
            
            link = subcategoria.find("a")
            nombre_subcategoria = link.text
        
            recetas[nombre_categoria][nombre_subcategoria] = []
            print('Obteniendo subcategoría ' + nombre_subcategoria)
            html_recetas = requests.get(link.get("href"))  # La pagina principal de la categoria
            html_recetas_soup = BeautifulSoup(html_recetas.text, features="html.parser")

            recetas_resultset = html_recetas_soup.findAll("a", {
                "class": "titulo titulo--resultado"})  # Guardamos los links de cada receta de la primera pagina

            i = 2
            paginador_div = html_recetas_soup.find("div", {"class": "paginator"})
            hay_mas_recetas = paginador_div != None
            while hay_mas_recetas:
                next_pagina = html_recetas_soup.find("div", {"class": "paginator"}).find("a", {"class": "next ga"})
                if (next_pagina == None):
                    hay_mas_recetas = False
                    break
                print("Obteniendo recetas de la página " + str(i) + " de la subcategoría " + nombre_subcategoria)
                html_recetas = requests.get(next_pagina.get("href"))
                html_recetas_soup = BeautifulSoup(html_recetas.text, features="html.parser")
                recetas_resultset.extend(
                    html_recetas_soup.findAll("a", {
                        "class": "titulo titulo--resultado"}))
                i += 1


            recetas_info = []  # Aqui guardaremos la informacion parseada de las recetas de la categoria actual
            print('Se han encontrado ' + str(len(recetas_resultset)) + ' recetas para la subcategoría ' + nombre_subcategoria)
        
            for idx, receta in enumerate(recetas_resultset):
            # Visitamos cada receta guardada de la categoria actual
                link_receta = receta.get("href")
                print('Obteniendo receta #' + str(idx) + ': ' + link_receta)
                html_receta = requests.get(link_receta)

                if html_receta.status_code != 200:
                    print('Error obteniendo el contenido. Status code: ' + str(html_receta.status_code))
                    continue

                html_receta_soup = BeautifulSoup(html_receta.content.decode('utf-8'),
                                                features="html.parser")
                
                # Titulo
                titulo = html_receta_soup.find("h1", {"class": "titulo titulo--articulo"}).text.strip()
                if not titulo.startswith('Receta de'):
                    continue
            

                # Intro
                try:
                    intro_resultset = html_receta_soup.find("div", {"class": "intro"})("p")
                    intro = ""
                    for p in intro_resultset:
                        intro += p.text.strip()
                except:
                    intro = None


                # Comensales
                try:
                    comensales = html_receta_soup.find("span", {"class": "comensales"}).text.strip()
                    comensales = comensales.replace(" comensales", "")
                    comensales = comensales.replace(" comensal", "")
                    comensales = int(comensales)
                except:
                    comensales = None

                # Duracion
                try:
                    duracion = html_receta_soup.find("span", {"class": "duracion"}).text.strip()
                except:
                    duracion = None

                # Tipo de comida (entrante, primer plato...)
                try:
                    tipo_comida = html_receta_soup.find("span", {"class": "para"}).text.strip()
                except:
                    tipo_comida = None

                # Ingredientes
                ingredientes = []
                for i in html_receta_soup.findAll("li", {"class": "ingrediente"}):
                    try:
                        ingredientes.append(i.find("label").text.strip())
                    except:
                        continue

                # Preparacion
                preparacion_resultset = html_receta_soup.findAll("div", {"class": "apartado"})
                preparacion = []

                for p in preparacion_resultset:
                    try:
                        orden = p.find("div", {"class": "orden"}).text.strip()
                    except:
                        continue
                    try:
                        descripcion = p.find("p").text.strip()
                    except:
                        continue
                    preparacion.append({"orden": orden,
                                        "descripcion": descripcion})

                # Una vez obtenidos los datos deseados, los guardamos en nuestra lista de recetas
                recetas_info.append({"titulo": titulo,
                                    "descripcion": intro,
                                    "comensales": comensales,
                                    "duracion": duracion,
                                    "tipo_comida": tipo_comida,
                                    "ingredientes": ingredientes,
                                    "preparacion": preparacion})

            recetas[nombre_categoria][nombre_subcategoria] = recetas_info
    #print(json.dumps(recetas, indent=4, sort_keys=True, ensure_ascii=False).encode('utf8').decode())
    return recetas


if __name__ == "__main__":
    get_datos()
