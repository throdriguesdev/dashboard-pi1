import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import os

# Leia os dados dos CSVs
df1 = pd.read_csv("dataset-1.csv")
df2 = pd.read_csv("dataset-2.csv")
df3 = pd.read_csv("dataset-3.csv")
df4 = pd.read_csv("dataset-4.csv")
df5 = pd.read_csv("dataset-5.csv")

# Dicionário de mapeamento de regiões e estados
region_map = {
    'Sudeste': ['Minas Gerais', 'São Paulo', 'Rio de Janeiro', 'Espírito Santo'],
    'Nordeste': ['Bahia', 'Pernambuco', 'Ceará', 'Maranhão', 'Paraíba', 'Rio Grande do Norte', 'Alagoas', 'Piauí', 'Sergipe'],
    'Sul': ['Paraná', 'Rio Grande do Sul', 'Santa Catarina'],
    'Centro-Oeste': ['Goiás', 'Mato Grosso', 'Mato Grosso do Sul', 'Distrito Federal'],
    'Norte': ['Pará', 'Amazonas', 'Rondônia', 'Tocantins', 'Acre', 'Roraima', 'Amapá']
}

# Crie a aplicação Dash
app = dash.Dash(__name__)

# Adicionar folha de estilo CSS
app.css.append_css({"external_url": "/assets/styles.css"})

app.layout = html.Div(className='container', children=[
    html.H1("Dashboard de Escolas"),
    html.Div([
        dcc.Dropdown(
            id='visualization-dropdown',
            options=[
                {'label': 'Escolas Públicas', 'value': 'public'},
                {'label': 'Escolas Particulares', 'value': 'private'},
                {'label': 'Ambas', 'value': 'both'}
            ],
            value='both',
            className='dccDropdown'
        ),
    ]),
    dcc.Graph(id='school-graph'),
    dcc.Graph(id='libraries-pie'),
    dcc.Graph(id='schools-by-state')
])

@app.callback(
    Output('school-graph', 'figure'),
    [Input('visualization-dropdown', 'value')]
)
def update_graph(selected_option):
    fig = go.Figure()

    if selected_option in ['public', 'both']:
        for region, states in region_map.items():
            fig.add_trace(go.Bar(
                name=f'Escolas Públicas - {region}',
                x=states,
                y=[df1[df1['NO_UF'] == state]['Escolas_Publicas_Com_Biblioteca'].iloc[0] if not df1[df1['NO_UF'] == state].empty else 0 for state in states]
            ))

    if selected_option in ['private', 'both']:
        for region, states in region_map.items():
            fig.add_trace(go.Bar(
                name=f'Escolas Particulares - {region}',
                x=states,
                y=[df2[df2['NO_UF'] == state]['Escolas_Particulares_Com_Biblioteca'].iloc[0] if not df2[df2['NO_UF'] == state].empty else 0 for state in states]
            ))

    fig.update_layout(
        title='Escolas Públicas e Particulares com Biblioteca por Região',
        xaxis_title='Estado',
        yaxis_title='Número de Escolas',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

@app.callback(
    Output('libraries-pie', 'figure'),
    [Input('visualization-dropdown', 'value')]
)
def update_pie(selected_option):
    fig = go.Figure()

    fig.add_trace(go.Pie(labels=df5['Categoria'], values=df5['Total']))

    fig.update_layout(
        title='Quantidade de Bibliotecas Totais no Brasil',
    )

    return fig

@app.callback(
    Output('schools-by-state', 'figure'),
    [Input('visualization-dropdown', 'value')]
)
def update_schools_by_state(selected_option):
    fig = go.Figure()

    fig.add_trace(go.Bar(name='Escolas Públicas', x=df1['NO_UF'], y=df1['Escolas_Publicas_Com_Biblioteca']))
    fig.add_trace(go.Bar(name='Escolas Particulares', x=df2['NO_UF'], y=df2['Escolas_Particulares_Com_Biblioteca']))

    fig.update_layout(
        title='Escolas Públicas e Particulares por Estado',
        xaxis_title='Estado',
        yaxis_title='Número de Escolas',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
