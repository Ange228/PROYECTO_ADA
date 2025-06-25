import time
import os
import polars as pl
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import random
import math
import plotly.graph_objects as go
import plotly.express as px


def bfs_distancia(grafo, origen, destino):
    """Distancia más corta entre dos nodos usando BFS"""
    if origen == destino:
        return 0

    visitado = set([origen])
    cola = deque([(origen, 0)])

    while cola:
        actual, dist = cola.popleft()
        for vecino in grafo.get(actual, []):
            if vecino == destino:
                return dist + 1
            if vecino not in visitado:
                visitado.add(vecino)
                cola.append((vecino, dist + 1))

    return None  # No hay camino


def analisis_camino_promedio(subgrafo, sample_size=1000, mostrar_grafico=True):
    print(f"\nCalculando longitud promedio de caminos más cortos (muestra: {sample_size})")
    inicio = time.time()

    nodos = list(subgrafo.keys())
    total_distancias = []
    errores = 0

    for _ in range(sample_size):
        origen, destino = random.sample(nodos, 2)
        distancia = bfs_distancia(subgrafo, origen, destino)
        if distancia is not None:
            total_distancias.append(distancia)
        else:
            errores += 1

    if not total_distancias:
        print("No se encontraron caminos válidos.")
        return 0

    promedio = sum(total_distancias) / len(total_distancias)
    fin = time.time()
    print(f"✔ Promedio de caminos: {promedio:.2f} (basado en {len(total_distancias)} pares, {errores} fallos)")
    print(f"Tiempo: {fin - inicio:.2f}s")

    if mostrar_grafico:
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 5))
            plt.hist(total_distancias, bins=range(1, max(total_distancias)+2), color='skyblue', edgecolor='black')
            plt.title("Distribución de Caminos Más Cortos")
            plt.xlabel("Longitud del camino")
            plt.ylabel("Frecuencia")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except ImportError:
            print("matplotlib no está instalado. Ejecuta: pip install matplotlib")

    return promedio




