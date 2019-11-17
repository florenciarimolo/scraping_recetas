# coding=utf-8
from bs4 import BeautifulSoup
import requests
import requests_cache
from idna import unicode

# Guardaremos las peticiones en cache, para no tener que hacerlas cada vez que se ejecuta el script
from rest_framework.utils import json

requests_cache.install_cache('cache', backend='sqlite', expire_after=360000)


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
    categorias_resultset = html_inicio_soup.find("div", {"class": "lista_menu"}).find("div", {"class": "clear"})
    links_categorias = categorias_resultset("a")
    recetas = {}
    for link in links_categorias:
        print('Obteniendo datos de la categoría ' + link.text)
        html_recetas = requests.get(link.get("href"))  # La pagina principal de la categoria
        html_recetas_soup = BeautifulSoup(html_recetas.text, features="html.parser")

        recetas_resultset = html_recetas_soup.findAll("a", {
            "class": "titulo titulo--resultado"})  # Guardamos los links de cada receta de la primera pagina

        paginador = html_recetas_soup.find("div", {"class": "paginator"}).findAll("a", {"class": "ga"})
        paginador.pop()  # Quitamos el ultimo link del paginador ya que es la pagina actual

        for index, p in enumerate(paginador):
            html_recetas = requests.get(p.get("href"))
            html_recetas_soup = BeautifulSoup(html_recetas.text, features="html.parser")
            recetas_resultset.extend(
                html_recetas_soup.findAll("a", {
                    "class": "titulo titulo--resultado"}))  # Guardamos los links de todas las recetas de las primeras
            # 5 paginas (el paginador solo llega a 5 en la pagina inicial)

        recetas_info = []  # Aqui guardaremos la informacion parseada de las recetas de la categoria actual

        for receta in recetas_resultset:
            # Visitamos cada receta guardada de la categoria actual
            html_receta = requests.get(receta.get("href"))
            html_receta_soup = BeautifulSoup(unicode(html_receta.content, 'utf-8'),
                                             features="html.parser")

            # Intro
            intro_resultset = html_receta_soup.find("div", {"class": "intro"})("p")
            intro = ""
            for p in intro_resultset:
                intro += p.text.strip() + "\n"

            # Titulo
            titulo = html_receta_soup.find("h1", {"class": "titulo titulo--articulo"}).text.strip()
            if not titulo.startswith('Receta de'):
                continue

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

        recetas[link.text] = recetas_info
    print(json.dumps(recetas, indent=4, sort_keys=True, ensure_ascii=False).encode('utf8').decode())
    return recetas


if __name__ == "__main__":
    get_datos()
