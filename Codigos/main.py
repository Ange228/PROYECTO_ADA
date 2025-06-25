import os
import time
from red_social.cargador import CargadorRedSocial
from red_social.comunidades import DeteccionPorPropagacion, mostrar_resultados_comunidades, generar_estadisticas_comunidades
from red_social.analisis import analisis_camino_promedio
from red_social.mst import MinimumSpanningTree, generar_estadisticas_mst
from red_social.visualizacion import visualizar_comunidades, visualizar_red_general

def main():
    cargador = CargadorRedSocial()

    archivos = {
        'ubicaciones': "10_million_location.txt",
        'conexiones': "10_million_user.txt"
    }

    for tipo, archivo in archivos.items():
        if not os.path.exists(archivo):
            print(f"ERROR: No se encuentra {archivo}")
            return

    tiempos = {}

    print("\n" + "="*50)
    print("CARGA DE DATOS PARA DETECCIÓN DE COMUNIDADES".center(50))
    print("="*50)

    inicio = time.time()
    cargador.cargar_ubicaciones(archivos['ubicaciones'])
    tiempos['Carga Ubicaciones'] = time.time() - inicio

    inicio = time.time()
    cargador.cargar_conexiones(archivos['conexiones'])
    tiempos['Carga Conexiones'] = time.time() - inicio

    tamaño_subgrafo = 10000000#Tamaño del subgrafo para análisis y detección de comunidades
    inicio = time.time()
    
    subgrafo = cargador.obtener_subgrafo(tamaño=tamaño_subgrafo) #con la funcion obgterner subgrafo solo agarramos  nodos seleccionados que son mutuas (bidireccionales).
    tiempos['Extracción Subgrafo'] = time.time() - inicio

    print("\n" + "="*50)
    print("DETECCIÓN DE COMUNIDADES (Label Propagation)".center(50))
    print("="*50)

    inicio = time.time()
    lp = DeteccionPorPropagacion(subgrafo)
    comunidades = lp.ejecutar_propagacion()
    tiempos['Detección Comunidades'] = time.time() - inicio

    mostrar_resultados_comunidades(comunidades, algoritmo="Label Propagation")

    print("\n" + "="*60)
    print("VISUALIZACIÓN DE COMUNIDADES".center(60))
    print("="*60)
    inicio = time.time()
    visualizar_comunidades(subgrafo, cargador.ubicaciones, comunidades, "Label Propagation")
    generar_estadisticas_comunidades(comunidades, subgrafo, "Label Propagation")
    tiempos['Visualización Comunidades'] = time.time() - inicio

    print("\n" + "="*50)
    print("ANÁLISIS DE CAMINOS MÁS CORTOS".center(50))
    print("="*50)
    analisis_camino_promedio(subgrafo, sample_size=1000)

    print("\n" + "="*50)
    print("VISUALIZACIÓN INTERACTIVA DE LA RED".center(50))
    print("="*50)
    visualizar_red_general(subgrafo, cargador.ubicaciones)

    print("\n" + "="*80)
    print("ÁRBOL DE EXPANSIÓN MÍNIMA (KRUSKAL)".center(80))
    print("="*80)
    inicio = time.time()
    mst = MinimumSpanningTree(subgrafo, cargador.ubicaciones).kruskal()
    tiempos['Cálculo MST'] = time.time() - inicio

    print("\n" + "="*60)
    print("VISUALIZACIÓN DEL ÁRBOL DE EXPANSIÓN MÍNIMA".center(60))
    print("="*60)
    inicio = time.time()
    generar_estadisticas_mst(mst, subgrafo)
    tiempos['Visualización MST'] = time.time() - inicio

    print("\n" + "="*50)
    print("RESUMEN DE TIEMPOS".center(50))
    print("="*50)
    for nombre, duracion in tiempos.items():
        print(f"{nombre:<25}: {duracion:.2f} segundos")

    print("\n✔ Análisis completo.")

if __name__ == "__main__":
    main()
