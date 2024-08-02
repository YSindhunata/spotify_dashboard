import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# Pastikan path ke file CSV benar
# Ganti path ini dengan path yang benar ke file CSV Anda
csv_file_path = 'D:/SINAU/spotify_dashboard/spotify_dashboard/Spotify_2010_2019.csv'

# Membaca data
df = pd.read_csv(csv_file_path)

# Data preprocessing
df_cleaned = df.drop(index=[1000, 1001, 1002])
df_cleaned.drop_duplicates(inplace=True)

# Membuat Histogram untuk feature musik
fig_histograms = make_subplots(rows=3, cols=3, subplot_titles=('<i>popularity', '<i>danceability', '<i>energy', '<i>loudness', '<i>speechiness', '<i>acousticness', '<i>liveness', '<i>valence', '<i>tempo'))
fig_histograms.add_trace(go.Histogram(x=df['pop'], name='popularity'), row=1, col=1)
fig_histograms.add_trace(go.Histogram(x=df['dnce'], name='danceability'), row=1, col=2)
fig_histograms.add_trace(go.Histogram(x=df['nrgy'], name='energy'), row=1, col=3)
fig_histograms.add_trace(go.Histogram(x=df['dB'], name='loudness'), row=2, col=1)
fig_histograms.add_trace(go.Histogram(x=df['spch'], name='speechiness'), row=2, col=2)
fig_histograms.add_trace(go.Histogram(x=df['acous'], name='acousticness'), row=2, col=3)
fig_histograms.add_trace(go.Histogram(x=df['live'], name='liveness'), row=3, col=1)
fig_histograms.add_trace(go.Histogram(x=df['val'], name='valence'), row=3, col=2)
fig_histograms.add_trace(go.Histogram(x=df['bpm'], name='tempo'), row=3, col=3)
fig_histograms.update_layout(height=900, width=900, title_text='<b>Feature Distribution')
fig_histograms.update_layout(template='plotly_dark', title_x=0.5)

# Menampilkan jumlah lagu berdasarkan genre
fig_genres = px.histogram(df.groupby('top genre', as_index=False).count().sort_values(by='title', ascending=False), x='top genre', y='title', color_discrete_sequence=['green'], template='plotly_dark', marginal='box', title='<b>Total songs based on genres</b>')
fig_genres.update_layout(xaxis_title='Genres', yaxis_title='Songs', title_x=0.5)

# Menampilkan 20 penyanyi yang populer
fig_singers = px.bar(df.groupby('artist', as_index=False).sum().sort_values(by='pop', ascending=False).head(20), x='artist', y='pop', color_discrete_sequence=['lightgreen'], template='plotly_dark', text='pop', title='<b>Top 20 Popular Singers')
fig_singers.update_layout(xaxis_title='Singer', yaxis_title='Popularity (pop)', title_font_size=20, title_x=0.5)

# Menampilkan lagu yang populer di Spotify
fig_songs = px.line(df.sort_values(by='pop', ascending=False).head(20), x='title', y='pop', hover_data=['artist'], color_discrete_sequence=['green'], markers=True, title='<b>Top 20 songs in Spotify')
fig_songs.update_layout(xaxis_title='Title of Song', yaxis_title='Popularity (pop)', title_font_size=20, title_x=0.5)

# Inisialisasi Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    html.H1(children='Spotify Data Dashboard'),
    html.Div(children='''Dashboard yang menampilkan visualisasi data Spotify 2010-2019.'''),
    
    dcc.Graph(
        id='feature-distribution',
        figure=fig_histograms
    ),
    dcc.Graph(
        id='total-songs-genres',
        figure=fig_genres
    ),
    dcc.Graph(
        id='top-20-singers',
        figure=fig_singers
    ),
    dcc.Graph(
        id='top-20-songs',
        figure=fig_songs
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
