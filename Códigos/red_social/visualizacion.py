import plotly.graph_objects as go
import plotly.express as px


def visualizar_comunidades(subgrafo, ubicaciones, comunidades, algoritmo=""):
    """
    Visualiza las comunidades detectadas usando Plotly con colores diferentes
    """
    print(f"\n{'='*60}")
    print(f"GENERANDO VISUALIZACIÓN DE COMUNIDADES - {algoritmo}".center(60))
    print(f"{'='*60}")

    try:
        colores = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel + px.colors.qualitative.Dark24

        nodo_a_comunidad = {}
        for i, comunidad in enumerate(comunidades):
            for nodo in comunidad:
                nodo_a_comunidad[nodo] = i

        datos_comunidades = {}
        for i, comunidad in enumerate(comunidades):
            datos_comunidades[i] = {
                'x': [], 'y': [], 'textos': [],
                'color': colores[i % len(colores)],
                'tamaño': len(comunidad)
            }

        for nodo in subgrafo:
            if nodo in ubicaciones and nodo in nodo_a_comunidad:
                lat, lon = ubicaciones[nodo]
                com_id = nodo_a_comunidad[nodo]

                datos_comunidades[com_id]['x'].append(lon)
                datos_comunidades[com_id]['y'].append(lat)
                datos_comunidades[com_id]['textos'].append(
                    f"<b>Usuario: {nodo}</b><br>"
                    f"Comunidad: {com_id + 1}<br>"
                    f"Tamaño comunidad: {datos_comunidades[com_id]['tamaño']}<br>"
                    f"Lat: {lat:.4f}, Lon: {lon:.4f}<br>"
                    f"Conexiones: {len(subgrafo.get(nodo, []))}"
                )

        aristas_internas_x, aristas_internas_y = [], []
        aristas_externas_x, aristas_externas_y = [], []

        for nodo in subgrafo:
            if nodo in ubicaciones and nodo in nodo_a_comunidad:
                lat1, lon1 = ubicaciones[nodo]
                com1 = nodo_a_comunidad[nodo]

                for vecino in subgrafo[nodo]:
                    if vecino > nodo and vecino in ubicaciones and vecino in nodo_a_comunidad:
                        lat2, lon2 = ubicaciones[vecino]
                        com2 = nodo_a_comunidad[vecino]

                        if com1 == com2:
                            aristas_internas_x.extend([lon1, lon2, None])
                            aristas_internas_y.extend([lat1, lat2, None])
                        else:
                            aristas_externas_x.extend([lon1, lon2, None])
                            aristas_externas_y.extend([lat1, lat2, None])

        fig = go.Figure()

        if aristas_externas_x:
            fig.add_trace(go.Scatter(
                x=aristas_externas_x, y=aristas_externas_y,
                mode='lines', line=dict(width=0.5, color='lightgray'),
                hoverinfo='none', name='Conexiones inter-comunidad', opacity=0.3
            ))

        if aristas_internas_x:
            fig.add_trace(go.Scatter(
                x=aristas_internas_x, y=aristas_internas_y,
                mode='lines', line=dict(width=0.8, color='gray'),
                hoverinfo='none', name='Conexiones intra-comunidad', opacity=0.6
            ))

        for com_id, datos in datos_comunidades.items():
            if datos['x']:
                tamaño_marcador = min(12, max(4, 8 + datos['tamaño'] // 10))
                fig.add_trace(go.Scatter(
                    x=datos['x'], y=datos['y'],
                    mode='markers', text=datos['textos'], hoverinfo='text',
                    marker=dict(size=tamaño_marcador, color=datos['color'], opacity=0.8, line=dict(width=1, color='white')),
                    name=f'Comunidad {com_id + 1} ({datos["tamaño"]} nodos)'
                ))

        total_nodos = sum(len(c) for c in comunidades)
        total_aristas_int = len([x for x in aristas_internas_x if x is not None]) // 3
        total_aristas_ext = len([x for x in aristas_externas_x if x is not None]) // 3

        fig.update_layout(
            title={
                'text': f'<b>Detección de Comunidades - {algoritmo}</b><br>'
                        f'<span style="font-size:14px">{len(comunidades)} comunidades | '
                        f'{total_nodos} nodos | '
                        f'{total_aristas_int} aristas internas | '
                        f'{total_aristas_ext} aristas externas</span>',
                'x': 0.5, 'xanchor': 'center'
            },
            showlegend=True,
            hovermode='closest',
            xaxis=dict(title='Longitud', showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
            yaxis=dict(title='Latitud', showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
            plot_bgcolor='white', width=1200, height=800,
            margin=dict(b=50, l=50, r=50, t=100),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.01)
        )

        fig.show()
        return fig

    except Exception as e:
        print(f"Error generando visualización: {e}")
        return None


def visualizar_red_general(subgrafo, ubicaciones):
    """
    Visualiza la red completa sin dividir por comunidades
    """
    try:
        nodos_x, nodos_y, textos = [], [], []
        for nodo in subgrafo:
            if nodo in ubicaciones:
                lat, lon = ubicaciones[nodo]
                nodos_x.append(lon)
                nodos_y.append(lat)
                textos.append(f"Usuario: {nodo}<br>Lat: {lat:.4f}, Lon: {lon:.4f}")

        aristas_x, aristas_y = [], []
        for nodo in subgrafo:
            if nodo in ubicaciones:
                lat1, lon1 = ubicaciones[nodo]
                for vecino in subgrafo[nodo]:
                    if vecino > nodo and vecino in ubicaciones:
                        lat2, lon2 = ubicaciones[vecino]
                        aristas_x.extend([lon1, lon2, None])
                        aristas_y.extend([lat1, lat2, None])

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=aristas_x, y=aristas_y, mode='lines',
            line=dict(width=0.5, color='gray'), hoverinfo='none', name='Conexiones'
        ))

        fig.add_trace(go.Scatter(
            x=nodos_x, y=nodos_y, mode='markers', text=textos,
            hoverinfo='text', marker=dict(size=6, color='blue', opacity=0.8, line=dict(width=0.5, color='white')),
            name='Usuarios'
        ))

        fig.update_layout(
            title='Red Social (Visualización por Coordenadas)',
            showlegend=True,
            hovermode='closest',
            xaxis=dict(title='Longitud'),
            yaxis=dict(title='Latitud'),
            margin=dict(b=20, l=5, r=5, t=40),
        )

        fig.show()
        return fig

    except Exception as e:
        print(f"Error generando visualización general: {e}")
        return None
