import pandas as pd
import plotly.graph_objects as go

# Les inn data
file_name_csv = "Datasett_fodselstall_komma.csv"
df = pd.read_csv(file_name_csv, sep=',', encoding='utf-8-sig')
df.columns = [col.strip() for col in df.columns]  # Fjern ekstra mellomrom
print(df.columns)  # Sjekk at 'År' nå vises riktig
df['År'] = pd.to_datetime(df['År'], format='%Y')
# Lag graf med range slider og selectors
fig = go.Figure()
fig.add_trace(
    go.Scatter(x=df['År'], y=df['Levendefødte i alt'], mode='lines', name='Levendefødte')
)
fig.update_layout(
    title_text="Levendefødte i Norge over tid",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                #dict(count=10, label="10 år", step="year", stepmode="backward"),
                #dict(count=20, label="20 år", step="year", stepmode="backward"),
                #dict(step="all", label="Alle")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date",
        title='År'
    ),
    yaxis_title='Antall levendefødte'
)
fig.show()
