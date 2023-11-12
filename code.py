# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/ellqthh/laba5/main/анализ%20данных%20о%20здоровье%20и%20мед%20показаниях%20.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='Возраст', y='Давление', histfunc='avg'))
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)