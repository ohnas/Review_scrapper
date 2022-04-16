from dash import Dash, html, dcc
import plotly.express as px

from review_scrapper import review_scrap

app = Dash(__name__)

fig = px.bar(review_scrap())

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        html.Div(
            children="""
        Dash: A web application framework for your data.
    """
        ),
        dcc.Graph(id="example-graph", figure=fig),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
