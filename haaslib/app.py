import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from haaslib import api

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize the HaasLib executor
executor = api.RequestsExecutor(host="127.0.0.1", port=8090, state=api.Guest())
executor = executor.authenticate(email="your_email@example.com", password="your_password")

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("HaasBot Management Dashboard"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(html.H5("Select Bot for Performance Analysis"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='bot-dropdown', options=[], placeholder="Select a bot"), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='performance-graph'), className="mb-2")
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='performance-metrics'), className="mb-2")
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    )
])

# Callback to populate the bot dropdown
@app.callback(
    Output('bot-dropdown', 'options'),
    Input('bot-dropdown', 'value')
)
def update_bot_dropdown(value):
    bot_api = api.BotAPI(executor)
    bots = bot_api.get_bots()
    return [{'label': bot.bot_name, 'value': bot.bot_id} for bot in bots]

# Callback to display bot performance
@app.callback(
    [Output('performance-graph', 'figure'),
     Output('performance-metrics', 'children')],
    Input('bot-dropdown', 'value')
)
def display_bot_performance(bot_id):
    if bot_id is None:
        return go.Figure(), ""

    bot_api = api.BotAPI(executor)
    bot_details = bot_api.get_bot(bot_id)

    # Example performance data (replace with actual data)
    performance_data = {
        'time': [1, 2, 3, 4, 5],
        'profit': [100, 150, 130, 170, 190]
    }

    figure = go.Figure(
        data=[go.Scatter(x=performance_data['time'], y=performance_data['profit'], mode='lines+markers')]
    )

    metrics = [
        html.P(f"Bot Name: {bot_details.bot_name}"),
        html.P(f"Total Profit: {sum(performance_data['profit'])}"),
        html.P(f"Number of Trades: {len(performance_data['time'])}")
    ]

    return figure, metrics

# Callback to update market data graph
@app.callback(
    Output('market-data-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_market_data(n_intervals):
    price_api = api.PriceAPI(executor)
    market = "BINANCE_BTC_USDT_SPOT"
    ticks = price_api.last_ticks(market, interval=1)

    figure = go.Figure(
        data=[go.Scatter(x=[tick.timestamp for tick in ticks], y=[tick.price for tick in ticks], mode='lines+markers')]
    )
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)