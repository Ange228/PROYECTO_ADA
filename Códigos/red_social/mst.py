import time
import os
import polars as pl
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import random
import math
import plotly.graph_objects as go
import plotly.express as px



##AQUI EL ARBOL DE EXPANSION

class MinimumSpanningTree:
    def __init__(self, grafo, ubicaciones):
        self.grafo = grafo
        self.ubicaciones = ubicaciones
        self.padre = {}
        self.rango = {}

    def calcular_distancia_haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    def encontrar(self, nodo):
        if self.padre[nodo] != nodo:
            self.padre[nodo] = self.encontrar(self.padre[nodo])
        return self.padre[nodo]

    def unir(self, nodo1, nodo2):
        raiz1 = self.encontrar(nodo1)
        raiz2 = self.encontrar(nodo2)
        if raiz1 != raiz2:
            if self.rango[raiz1] < self.rango[raiz2]:
                raiz1, raiz2 = raiz2, raiz1
            self.padre[raiz2] = raiz1
            if self.rango[raiz1] == self.rango[raiz2]:
                self.rango[raiz1] += 1

    def kruskal(self):
        print(f"\n{'='*60}")
        print("CALCULANDO ÁRBOL DE EXPANSIÓN MÍNIMA (KRUSKAL)".center(60))
        print(f"{'='*60}")
        inicio = time.time()

        for nodo in self.grafo:
            self.padre[nodo] = nodo
            self.rango[nodo] = 0

        aristas = []
        for nodo1 in self.grafo:
            if nodo1 in self.ubicaciones:
                lat1, lon1 = self.ubicaciones[nodo1]
                for nodo2 in self.grafo[nodo1]:
                    if nodo2 > nodo1 and nodo2 in self.ubicaciones:
                        lat2, lon2 = self.ubicaciones[nodo2]
                        peso = self.calcular_distancia_haversine(lat1, lon1, lat2, lon2)
                        aristas.append((peso, nodo1, nodo2))

        aristas.sort()

        mst = []
        total_peso = 0
        for peso, nodo1, nodo2 in aristas:
            if self.encontrar(nodo1) != self.encontrar(nodo2):
                self.unir(nodo1, nodo2)
                mst.append((nodo1, nodo2, peso))
                total_peso += peso

        tiempo_total = time.time() - inicio
        print(f"MST calculado en {tiempo_total:.2f}s")
        print(f"Aristas en MST: {len(mst):,}")
        print(f"Peso total (km): {total_peso:.2f}")
        return mst

def generar_estadisticas_mst(mst_aristas, subgrafo):
    """
    Genera estadísticas detalladas del MST
    """
    if not mst_aristas:
        print("No hay aristas en el MST")
        return
    
    print(f"\n{'='*50}")
    print("ANÁLISIS DETALLADO DEL MST".center(50))
    print(f"{'='*50}")
    
    # Calcular grados en el MST
    grados_mst = {}
    for nodo1, nodo2, _ in mst_aristas:
        grados_mst[nodo1] = grados_mst.get(nodo1, 0) + 1
        grados_mst[nodo2] = grados_mst.get(nodo2, 0) + 1
    
    # Estadísticas de grados
    grados = list(grados_mst.values())
    print(f"📈 GRADOS EN EL MST:")
    print(f"   • Grado máximo: {max(grados)}")
    print(f"   • Grado mínimo: {min(grados)}")
    print(f"   • Grado promedio: {sum(grados)/len(grados):.2f}")
    
    # Nodos hoja (grado 1)
    hojas = [nodo for nodo, grado in grados_mst.items() if grado == 1]
    print(f"   • Nodos hoja (grado 1): {len(hojas)}")
    
    # Nodos hub (grado alto)
    grado_alto = [nodo for nodo, grado in grados_mst.items() if grado >= 5]
    print(f"   • Nodos hub (grado ≥5): {len(grado_alto)}")
    if grado_alto:
        print(f"     Ejemplos: {grado_alto[:5]}")
    
    # Comparar con grafo original
    print(f"\n🔄 COMPARACIÓN CON GRAFO ORIGINAL:")
    total_aristas_orig = sum(len(vecinos) for vecinos in subgrafo.values()) // 2
    print(f"   • Aristas originales: {total_aristas_orig:,}")
    print(f"   • Aristas en MST: {len(mst_aristas):,}")
    print(f"   • Reducción: {100*(1 - len(mst_aristas)/total_aristas_orig):.1f}%")


