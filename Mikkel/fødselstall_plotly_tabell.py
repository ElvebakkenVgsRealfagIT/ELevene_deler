import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Les CSV korrekt
file_name_csv = "Datasett_fodselstall_komma.csv"
df = pd.read_csv(file_name_csv, sep=',', encoding='utf-8-sig')
df.columns = [col.strip().replace('"', '') for col in df.columns]
df['År'] = pd.to_datetime(df['År'], format='%Y')
df['Nettoinnflytting'] = df['Innflyttinger'] - df['Utflyttinger']

dataserier = ['Levendefødte i alt', 'Innflyttinger', 'Utflyttinger', 'Nettoinnflytting']

# Lag subplot: tabell øverst, linjegraf under
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=False,
    vertical_spacing=0.1,
    specs=[[{"type": "table"}],
           [{"type": "scatter"}]]
)

# Legg til tabell (row 1)
fig.add_trace(
    go.Table(
        header=dict(
            values=['År'] + dataserier,
            font=dict(size=11),
            align="left"
        ),
        cells=dict(
            values=[df['År'].dt.year.tolist()] + [df[col].tolist() for col in dataserier],
            align="left")
    ),
    row=1, col=1
)

# Legg til første graf som utgangspunkt (row 2)
scatter_trace = go.Scatter(x=df['År'], y=df[dataserier[0]], mode='lines', name=dataserier[0])
fig.add_trace(scatter_trace, row=2, col=1)

# Oppdater layout med dropdown
fig.update_layout(
    height=800,
    title="Statistikk over tid",
    xaxis2=dict(  # NB: xaxis2, siden rad 2
        title='År',
        type='date',
        rangeslider=dict(visible=True)
    ),
    yaxis2=dict(title=dataserier[0]),  # NB: yaxis2, også rad 2
    updatemenus=[
        dict(
            buttons=[
                dict(
                    args=[
                        {"y": [df[col]], "name": col, "type": "scatter"},
                        {"yaxis2.title": col}
                    ],
                    label=col,
                    method="update"
                ) for col in dataserier
            ],
            direction="down",
            showactive=True,
            x=0.01,
            xanchor="left",
            y=0.525,
            yanchor="top"
        )
    ]
)

fig.show()
