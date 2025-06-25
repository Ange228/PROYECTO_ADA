import time
import os
import polars as pl
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import random
import math
import plotly.graph_objects as go
import plotly.express as px



class CargadorRedSocial:
    def __init__(self):
        self.ubicaciones = {}  # {id: (lat, lon)}
        self.conexiones = defaultdict(list)  # {id: [conexiones]}
    
    def cargar_ubicaciones(self, archivo):
        """Carga ubicaciones desde archivo con formato: lat,lon (float negativos)"""
        print(f"\nCargando ubicaciones desde {archivo}...")
        inicio = time.time()
        
        try:
            df = pl.read_csv(
                archivo,
                has_header=False,
                separator=',',
                new_columns=['lat', 'lon'],
                dtypes={'lat': pl.Float64, 'lon': pl.Float64}
            )
            
            self.ubicaciones = {
                idx + 1: (row['lat'], row['lon'])
                for idx, row in enumerate(df.iter_rows(named=True))
            }
            
            print(f"[POLARS] {len(self.ubicaciones):,} ubicaciones cargadas en {time.time() - inicio:.2f}s")
            
        except Exception as e:
            print(f"Error con carga ubi: {e}\n") 
 
    def cargar_conexiones(self, archivo, lote=100000):
        """Carga conexiones desde archivo con formato: id,id1,id2,..."""
        print(f"\nCargando conexiones desde {archivo}...")
        inicio = time.time()
        contador = total_conex = 0
        
        try:
            with open(archivo, 'r') as f:
                for line_num, linea in enumerate(f, 1):
                    try:
                        ids = list(map(int, filter(None, linea.strip().split(','))))
                        if ids:
                            self.conexiones[ids[0]] = ids[1:]
                            contador += 1
                            total_conex += len(ids[1:])
                    except Exception as e:
                        print(f"Línea {line_num}: Error - {e}")
        
        except Exception as e:
            print(f"Error con conexiones: {e}")
        
        print(f"{contador:,} usuarios con {total_conex:,} conexiones cargadas en {time.time() - inicio:.2f}s")
        print(f"Promedio: {total_conex/contador:.1f} conexiones/usuario")

    def obtener_subgrafo(self, tamaño=50000):
        """Extrae subgrafo usando muestreo más inteligente"""
        print(f"\nExtrayendo subgrafo de {tamaño:,} nodos...")
        inicio = time.time()
        
        if not self.conexiones:
            print("No hay conexiones cargadas.")
            return {}
        
        nodos_ordenados = sorted(
            [(nodo, len(vecinos)) for nodo, vecinos in self.conexiones.items()],
            key=lambda x: x[1], reverse=True
        )
        
        total_disponibles = len(nodos_ordenados)
        tamaño = min(tamaño, total_disponibles)

        hubs_count = tamaño // 3
        aleatorios_count = tamaño - hubs_count

        hubs = [nodo for nodo, _ in nodos_ordenados[:hubs_count]]
        resto_nodos = [nodo for nodo, _ in nodos_ordenados[hubs_count:]]

        # Si hay suficientes nodos para muestrear
        if len(resto_nodos) >= aleatorios_count:
            nodos_aleatorios = random.sample(resto_nodos, aleatorios_count)
        else:
            nodos_aleatorios = resto_nodos  # Tomar todos los disponibles

        nodos_seleccionados = set(hubs + nodos_aleatorios)
        
        # Construir subgrafo bidireccional
        subgrafo = defaultdict(list)
        for nodo in nodos_seleccionados:
            if nodo in self.conexiones:
                for vecino in self.conexiones[nodo]:
                    if vecino in nodos_seleccionados:
                        if vecino not in subgrafo[nodo]:
                            subgrafo[nodo].append(vecino)
                        if nodo not in subgrafo[vecino]:
                            subgrafo[vecino].append(nodo)

        print(f"Subgrafo: {len(subgrafo):,} nodos, {sum(len(v) for v in subgrafo.values())//2:,} aristas en {time.time()-inicio:.2f}s")
        return dict(subgrafo)
