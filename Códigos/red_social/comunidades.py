import time
import os
import polars as pl
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import random
import math
import plotly.graph_objects as go
import plotly.express as px


class DeteccionPorPropagacion:
    """
    Label Propagation Algorithm - Muy rápido O(n)
    Ideal para grafos muy grandes
    """
    
    def __init__(self, grafo):
        self.grafo = grafo
        # Inicializar: cada nodo tiene su propio label
        self.labels = {nodo: nodo for nodo in grafo}
    
    def ejecutar_propagacion(self, max_iteraciones=50):
        """Ejecuta Label Propagation"""
        print(f"\n{'='*60}")
        print("EJECUTANDO LABEL PROPAGATION".center(60))
        print(f"{'='*60}")
        
        inicio = time.time()
        
        for iteracion in range(max_iteraciones):
            cambios = 0
            nodos = list(self.grafo.keys())
            random.shuffle(nodos)  # Orden aleatorio
            
            for nodo in nodos:
                if not self.grafo.get(nodo):  # Nodo aislado
                    continue
                
                # Contar labels de los vecinos
                conteo_labels = defaultdict(int)
                for vecino in self.grafo[nodo]:
                    conteo_labels[self.labels[vecino]] += 1
                
                # Seleccionar el label más común (desempate aleatorio)
                if conteo_labels:
                    max_count = max(conteo_labels.values())
                    labels_candidatos = [label for label, count in conteo_labels.items() if count == max_count]
                    nuevo_label = random.choice(labels_candidatos)
                    
                    if nuevo_label != self.labels[nodo]:
                        self.labels[nodo] = nuevo_label
                        cambios += 1
            
            print(f"Iteración {iteracion + 1}: {cambios} cambios")
            
            if cambios == 0:  # Convergencia
                break
        
        tiempo_total = time.time() - inicio
        print(f"\nLabel Propagation completado en {tiempo_total:.2f}s")
        print(f"Iteraciones: {iteracion + 1}")
        
        return self.obtener_comunidades()
    
    def obtener_comunidades(self):
        """Convierte labels a comunidades"""
        comunidades_dict = defaultdict(set)
        for nodo, label in self.labels.items():
            comunidades_dict[label].add(nodo)
        
        return list(comunidades_dict.values())



def generar_estadisticas_comunidades(comunidades, subgrafo, algoritmo=""):
    """
    Genera estadísticas detalladas de las comunidades detectadas
    """
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DETALLADO DE COMUNIDADES - {algoritmo}".center(60))
    print(f"{'='*60}")
    
    if not comunidades:
        print("No se detectaron comunidades")
        return
    
    # Crear mapeo nodo -> comunidad
    nodo_a_comunidad = {}
    for i, comunidad in enumerate(comunidades):
        for nodo in comunidad:
            nodo_a_comunidad[nodo] = i
    
    # Calcular métricas
    tamaños = [len(c) for c in comunidades]
    total_nodos = sum(tamaños)
    
    # Conexiones internas vs externas
    conexiones_internas = 0
    conexiones_externas = 0
    
    for nodo in subgrafo:
        if nodo in nodo_a_comunidad:
            com_nodo = nodo_a_comunidad[nodo]
            for vecino in subgrafo[nodo]:
                if vecino in nodo_a_comunidad:
                    com_vecino = nodo_a_comunidad[vecino]
                    if com_nodo == com_vecino:
                        conexiones_internas += 1
                    else:
                        conexiones_externas += 1
    
    conexiones_internas //= 2  # Cada arista se cuenta dos veces
    conexiones_externas //= 2
    
    print(f"🔢 MÉTRICAS GENERALES:")
    print(f"   • Total comunidades: {len(comunidades)}")
    print(f"   • Nodos analizados: {total_nodos:,}")
    print(f"   • Tamaño promedio: {sum(tamaños)/len(tamaños):.1f} nodos")
    print(f"   • Comunidad más grande: {max(tamaños):,} nodos")
    print(f"   • Comunidad más pequeña: {min(tamaños):,} nodos")
    print(f"   • Mediana de tamaño: {sorted(tamaños)[len(tamaños)//2]:,} nodos")
    
    print(f"\n🔗 CONECTIVIDAD:")
    print(f"   • Conexiones internas: {conexiones_internas:,}")
    print(f"   • Conexiones externas: {conexiones_externas:,}")
    total_conexiones = conexiones_internas + conexiones_externas
    if total_conexiones > 0:
        cohesion = conexiones_internas / total_conexiones
        print(f"   • Cohesión (% internas): {cohesion:.1%}")
        print(f"   • Modularidad aproximada: {cohesion:.3f}")
    
    # Distribución de tamaños
    print(f"\n📈 DISTRIBUCIÓN DE TAMAÑOS:")
    rangos = [(1, 5), (6, 20), (21, 100), (101, 500), (501, float('inf'))]
    for min_tam, max_tam in rangos:
        if max_tam == float('inf'):
            count = sum(1 for t in tamaños if t >= min_tam)
            print(f"   • {min_tam}+ nodos: {count} comunidades")
        else:
            count = sum(1 for t in tamaños if min_tam <= t <= max_tam)
            print(f"   • {min_tam}-{max_tam} nodos: {count} comunidades")
    
    return {
        'total_comunidades': len(comunidades),
        'total_nodos': total_nodos,
        'conexiones_internas': conexiones_internas,
        'conexiones_externas': conexiones_externas,
        'cohesion': cohesion if total_conexiones > 0 else 0,
        'tamaños': tamaños
    }

###visualizzar comunidades

def mostrar_resultados_comunidades(comunidades, algoritmo=""):
    """Muestra resultados de cualquier algoritmo de detección"""
    print(f"\n{'='*60}")
    print(f"RESULTADOS - {algoritmo}".center(60))
    print(f"{'='*60}")
    
    print(f"\n● Total comunidades: {len(comunidades)}")
    print(f"● Nodos totales: {sum(len(c) for c in comunidades):,}")
    
    # Ordenar por tamaño
    comunidades_ordenadas = sorted(comunidades, key=len, reverse=True)
    
    print(f"\nTOP 10 COMUNIDADES MÁS GRANDES:")
    for i, comunidad in enumerate(comunidades_ordenadas[:10], 1):
        print(f"  {i:2d}. {len(comunidad):,} nodos")
        if len(comunidad) <= 5:
            print(f"      Nodos: {sorted(list(comunidad))}")
    
    # Estadísticas
    tamaños = [len(c) for c in comunidades]
    print(f"\nESTADÍSTICAS:")
    print(f"  Comunidad más grande: {max(tamaños):,} nodos")
    print(f"  Comunidad más pequeña: {min(tamaños):,} nodos")
    print(f"  Tamaño promedio: {sum(tamaños)/len(tamaños):.1f} nodos")
    print(f"  Mediana: {sorted(tamaños)[len(tamaños)//2]:,} nodos")

