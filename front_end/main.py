# =======================
#  APP
# =======================
from dash import Output, Input, State, Dash, html, dcc, exceptions
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc
import math as _math

from logica_montecarlo import logica_montecarlo

app = Dash(
    __name__,
    title="TP Montecarlo",
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)

# =======================
# HEADER
# =======================
header = dbc.Container(
    [
        html.H1("📊 Montecarlo — Simulación Instagram",
                className="display-6 fw-bold text-center mt-4 mb-2"),
        html.P(
            "Simulación probabilística con visualización en tiempo real.",
            className="lead text-center text-muted mb-4"
        ),
    ],
    fluid=True
)

# =======================
# FORM
# =======================
form_card = dbc.Card(
    [
        dbc.CardHeader("Parámetros"),
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Número de simulaciones (N)"),
                        dbc.Input(id="input-n", type="number", value=10000)
                    ]),
                    dbc.Col([
                        dbc.Label("Fila desde (j)"),
                        dbc.Input(id="input-desde", type="number", value=1)
                    ]),
                    dbc.Col([
                        dbc.Label("Fila hasta (i)"),
                        dbc.Input(id="input-hasta", type="number", value=200)
                    ]),
                ]),
                dbc.Button("Simular", id="btn", className="mt-3", color="primary")
            ]
        )
    ],
    className="shadow-sm"
)

# =======================
# KPIs
# =======================
kpis = dbc.Row([
    dbc.Col(dbc.Alert(["Promedio: ", html.Span(id="kpi-prom")], color="light")),
    dbc.Col(dbc.Alert(["% Edición+Extra: ", html.Span(id="kpi-prob")], color="light")),
    dbc.Col(dbc.Alert(["Iteraciones: ", html.Span(id="kpi-iter")], color="light")),
])

# =======================
# TABLA
# =======================
tabla = dbc.Card(
    dbc.CardBody(
        DataTable(
            id="tabla",
            page_action="none",  # 🔥 muestra TODO
            fixed_rows={"headers": True},
            style_table={"height": "60vh", "overflowY": "auto"},
            style_cell={"textAlign": "center", "fontSize": 13},
            style_header={"fontWeight": "bold"}
        )
    )
)

# =======================
# LAYOUT
# =======================
app.layout = dbc.Container([
    header,
    form_card,
    html.Br(),
    kpis,
    html.Br(),
    tabla
], fluid=True)


# =======================
# CALLBACK
# =======================
@app.callback(
    Output("tabla", "data"),
    Output("tabla", "columns"),
    Output("kpi-prom", "children"),
    Output("kpi-prob", "children"),
    Output("kpi-iter", "children"),
    Input("btn", "n_clicks"),
    State("input-n", "value"),
    State("input-desde", "value"),
    State("input-hasta", "value"),
    prevent_initial_call=True
)
def run_sim(n_clicks, n, j, i):

    if not n or n <= 0:
        return [], [], "", "", ""

    state = {
        "n": n,
        "i": 0,
        "total_tiempo": 0.0,
        "cont_edicion_y_extra": 0,
        "cont_sin_pausa_sin_extra": 0,
        "max_tiempo": 0.0,
        "min_tiempo": float("inf")
    }

    start = max(1, j or 1)
    end = max(start, i or 200)

    subset = []
    last = None

    for k in range(n):
        state, row = logica_montecarlo.montecarlo_step(state)

        last = row

        if start <= row["Iteración"] <= end:
            subset.append(row)

    # 🔥 siempre agrego la última si no está
    if last and (last["Iteración"] > end):
        subset.append(last)

    if not subset:
        return [], [], "", "", ""

    columns = [{"name": k, "id": k} for k in subset[0].keys()]

    return (
        subset,
        columns,
        f"{(state["total_tiempo"]/state["i"]):.2f}",
        f"{state["cont_edicion_y_extra"]/state["i"]*100:.2f}%",
        f"{state['i']}"
    )


# =======================
# RUN
# =======================
if __name__ == "__main__":
    app.run(debug=True)