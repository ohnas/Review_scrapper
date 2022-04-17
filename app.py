import plotly.express as px
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from review_scrapper import page_control
from review_scrapper import make_month_df


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Review Analysis"),
        dcc.Input(
            id="url-input",
            placeholder="분석할 url를 넣어주세요",
            type="url",
            style={"width": 600},
        ),
        html.Div(children=dcc.Graph(id="month-line-graph")),
    ]
)


@app.callback(Output("month-line-graph", "figure"), Input("url-input", "value"))
def graph(value):
    if value is not None:
        review_list = page_control(value)
        df = make_month_df(review_list)
    else:
        raise PreventUpdate
    fig = px.line(
        df,
        x="created",
        y="content",
        title="월별 리뷰 갯수",
        labels={"created": "월별", "content": "리뷰갯수"},
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
