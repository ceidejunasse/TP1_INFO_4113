import pandas as pd
import dash
from dash import dcc, html
import dash_table
import plotly.express as px
import webbrowser

# Charger les données
df = pd.read_excel("data_kpi.xlsx")

# Convertir 'Montant_Transaction' en type numérique
df["Montant_Transaction"] = pd.to_numeric(df["Montant_Transaction"], errors='coerce')

# Calcul des KPI
moyenne_montant = df["Montant_Transaction"].mean()
repartition_categories = df.groupby("Categorie_Produit")["Montant_Transaction"].sum()
repartition_pct = repartition_categories / repartition_categories.sum() * 100

clients_fideles = df.groupby("ID_Client")["ID_Client"].count()[df.groupby("ID_Client")["ID_Client"].count() > 1].count()
taux_recurrence = clients_fideles / df["ID_Client"].nunique() * 100

mode_paiement_pct = df.groupby("Mode_Paiement")["ID_Client"].count() / df["ID_Client"].count() * 100

# Calcul du CLV et de la catégorie la plus rentable
clv_data = df.groupby("ID_Client")["Montant_Transaction"].sum()
clv_moyenne = clv_data.mean()

best_categorie = repartition_categories.idxmax()
best_categorie_valeur = repartition_categories.max()

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Ajouter le CSS de Bootstrap
app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"})

# Mise en page de l'application
app.layout = html.Div(className='container', children=[
    html.H1("EXERCICE 1 : Analyse des KPI", className='text-center my-4'),

    # Informations personnelles
    html.Div([
        html.H6("Nom : Paho Wandji", className='text-center'),
        html.H6("Matricule : 19I2780", className='text-center'),
        html.H6("Superviseur : Dr Tekouabo", className='text-center'),
        html.H6("Matière : INFO_4113", className='text-center'),
    ], className='mb-4'),

    html.Div(className='row', children=[
        html.Div(className='col-md-6 mb-4', children=[
            html.H2("1) Moyenne des montants"),
            html.P(f"Moyenne des montants : {moyenne_montant:.2f} €", className='lead')
        ]),
        
        html.Div(className='col-md-6 mb-4', children=[
            html.H2("2) Taux de récurrence des clients"),
            html.P(f"Taux de récurrence des clients : {taux_recurrence:.2f} %", className='lead')
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='col-md-6 mb-4', children=[
            html.H2("3) Répartition des catégories"),
            dcc.Graph(
                figure=px.pie(repartition_pct,
                               names=repartition_pct.index,
                               values=repartition_pct.values,
                               title="Répartition des catégories"))
        ]),

        html.Div(className='col-md-6 mb-4', children=[
            html.H2("4) Répartition des modes de paiement"),
            dcc.Graph(
                figure=px.pie(mode_paiement_pct,
                               names=mode_paiement_pct.index,
                               values=mode_paiement_pct.values,
                               title="Répartition des modes de paiement"))
        ])
    ]),

    html.Div(className='row', children=[
        html.Div(className='col-md-6 mb-4', children=[
            html.H2("5) CLV (Customer Lifetime Value)"),
            html.P(f"CLV moyenne : {clv_moyenne:.2f} €", className='lead')
        ]),

        html.Div(className='col-md-6 mb-4', children=[
            html.H2("6) Catégorie la plus rentable"),
            html.P(f"Catégorie la plus rentable : {best_categorie}, Montant généré : {best_categorie_valeur:.2f} €", className='lead')
        ])
    ]),

    # Tableau des données étudiées
    html.Div(className='row', children=[
        html.Div(className='col-12', children=[
            html.H2("Données étudiées", className='text-center'),
            dash_table.DataTable(
                id='table-donnees',
                columns=[
                    {"name": col, "id": col} for col in df.columns
                ],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                page_size=10,  # Nombre de lignes par page
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                },
                style_header={
                    'backgroundColor': 'rgba(0, 123, 255, 0.1)',
                    'fontWeight': 'bold',
                }
            )
        ])
    ])
])

# Ouvrir le navigateur
if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:8050/')  # Ouvrir dans le navigateur
    app.run(debug=True)  # Utilisation de app.run