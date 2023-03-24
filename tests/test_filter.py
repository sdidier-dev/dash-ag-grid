from dash import Dash, html, Input, Output
from dash_ag_grid import AgGrid
import plotly.express as px
import json

from . import utils


df = px.data.election()
default_display_cols = ["district_id", "district", "winner"]


def test_fi001_floating_filter(dash_duo):
    app = Dash()
    app.layout = html.Div([
        AgGrid(
            id="grid",
            rowData=df.to_dict("records"),
            columnDefs=[
                {"headerName": col.capitalize(), "field": col}
                for col in default_display_cols
            ],
            defaultColDef={"filter": True, "floatingFilter": True}
        ),
        html.Div(id='filterModel')
    ])

    @app.callback(
        Output("filterModel", "children"),
        Input("grid", "filterModel"),
    )
    def updateFilterModel(fM):
        return json.dumps(fM)

    dash_duo.start_server(app)

    grid = utils.Grid(dash_duo, "grid")

    grid.wait_for_cell_text(0, 1, "101-Bois-de-Liesse")
    dash_duo.wait_for_text_to_equal("#filterModel", "{}")

    grid.set_filter(0, "12")
    dash_duo.wait_for_text_to_equal("#filterModel", '{"district_id": {"filterType": "text",'
                                                    ' "type": "contains", "filter": "12"}}')

    grid.wait_for_cell_text(0, 1, "112-DeLorimier")
    grid.wait_for_rendered_rows(5)

    grid.set_filter(0, "")
    dash_duo.wait_for_text_to_equal("#filterModel", "{}")
