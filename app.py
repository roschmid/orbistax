import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd

#Opening variables

external_stylesheets = ["https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/minty/bootstrap.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = "Orbis Tax Admin"

server = app.server

data = "jurisprudencia.csv"

df = pd.read_csv(data, sep=",")
filtered_df = df[["pubResumen", "pubNumOficio", "pubFechaPubli"]]

PAGE_SIZE = 25

#Table

def get_stock_table():
    
    return html.Div([
    html.H2("Orbis Tax Admin"),
    dcc.Markdown("""---""", style={"width": "50%"}),
    html.Div([
        html.Br(),
        dcc.Input(value='', id='filter-input', placeholder='Busca Texto...', debounce=False),
        dcc.Input(value="", id="filter-oficio", placeholder="Busca oficio...", debounce=False),
        dash_table.DataTable(
        id='datatable-paging',
        columns=[
            {"name": i, "id": i} for i in df.columns  # sorted(df.columns)
        ],
        style_cell={"textAlign": "left", "fontSize": "13px",
                    "whiteSpace": "normal", "height": "auto",
                    "maxWidth": "1300px"},
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom',

        sort_action='custom',
        sort_mode='single',
        sort_by=[],
        css=[
            {
        'selector': 'table',
        'rule': 'width: 90%;'
        }
            ],)
        ], style={"padding": "0px 0px 0px 30px"})
    ], style={"width": "60%"})

#Layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    get_stock_table()
], style={"width": "80%"})

#Callbacks

@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', 'page_current'),
     Input('datatable-paging', 'page_size'),
     Input('datatable-paging', 'sort_by'),
     Input("filter-input", "value"),
     Input("filter-oficio", "value")])
def update_table(page_current, page_size, sort_by, filter_string, filter_oficio):

    # Filter

    final_df = filtered_df.loc[filtered_df["pubResumen"].str.contains(filter_string, case=False)]
    clean_df = final_df.loc[final_df["pubNumOficio"].str.contains(filter_oficio, case=False)]

    # Sort if necessary
    if len(sort_by):
        clean_df = clean_df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )

    return clean_df.iloc[
           page_current * page_size:(page_current + 1) * page_size
           ].to_dict('records')

#Main

if __name__ == '__main__':
    app.run_server(debug=True)
