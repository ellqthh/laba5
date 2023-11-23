from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import base64
import io

app = Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow only single file upload
    ),
    html.Div(id='output-data-upload'),
    html.Div(children='Показатели'),
    html.Hr(),
    dcc.RadioItems(options=[
        {'label': 'Возраст', 'value': 'Возраст'},
        {'label': 'Давление', 'value': 'Давление'}
    ], value='Возраст', id='controls-and-radio-item'),
    dash_table.DataTable(data=[], page_size=10, id='data-table'),
    dcc.Graph(figure={}, id='controls-and-graph'),
    dcc.Graph(figure={}, id='histogram-chart'),
    dcc.Graph(figure={}, id='line-chart'),
])

@app.callback(
    [Output(component_id='data-table', component_property='data'),
     Output(component_id='controls-and-graph', component_property='figure'),
     Output(component_id='histogram-chart', component_property='figure'),
     Output(component_id='line-chart', component_property='figure')],
    [Input(component_id='upload-data', component_property='contents'),
     Input(component_id='upload-data', component_property='filename'),
     Input(component_id='controls-and-radio-item', component_property='value')]
)
def update_data_and_graph(contents, filename, col_chosen):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        fig_hist = px.histogram(df, x='Дата', y=col_chosen, histfunc='avg')
        fig_pie = px.pie(df, values='Пациент',  names='Пациент')
        fig_bar = px.bar(df, x='Дата', y='Пациент')

        return df.to_dict('records'), fig_pie, fig_hist, fig_bar
    else:
        return [], {}, {}, {}

if __name__ == '__main__':
    app.run_server(debug=True)