import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import requests

# --- KORAK 1: Priprema i čišćenje podataka ---

df_lokacije = pd.read_csv('moji_mars_podaci/mars_lokacije.csv', sep=';', decimal=',')
df_uzorci = pd.read_csv('moji_mars_podaci/mars_uzorci.csv', sep=';', decimal=',')

# Spajanje tablica
df = pd.merge(df_lokacije, df_uzorci, on='ID_Uzorka')

# Filtriranje anomalija
indeksi_za_brisanje = df[(df['Temp_Tla_C'] > 100) | (df['pH_Vrijednost'] < 0)].index
df_cisto = df.drop(indeksi_za_brisanje) # Cista tablica

# Definiranje Kandidata:
df_kandidati = df_cisto[
    (df_cisto['Metan_Senzor'] == 'Pozitivno') &
    (df_cisto['Organske_Molekule'] == 'Da')
]

# Vizualizacija i Satelitska mapa
def kreiraj_grafove(data, kandidati):
    sns.set_theme(style="whitegrid")

    # 1. Odnos temperature i vlage
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='Temp_Tla_C', y='H2O_Postotak', hue='Metan_Senzor', palette='coolwarm')
    plt.title('Odnos temperature i vlage uz detekciju metana')
    plt.savefig('graph1_temp_h2o.png') # Ažurirano ime datoteke[cite: 3]
    plt.close()

    # 2. Geografska karta dubine bušenja
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='GPS_LONG', y='GPS_LAT', hue='Dubina_Busenja_cm', palette='YlOrBr')
    plt.title('Prostorna raspodjela dubine bušenja')
    plt.savefig('graph2_heatmap_depth.png')
    plt.close()

    # 3. Karta detekcije metana
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='GPS_LONG', y='GPS_LAT', hue='Metan_Senzor',
                    palette={'Negativno': 'blue', 'Pozitivno': 'red'})
    plt.title('Lokacije pozitivne detekcije metana')
    plt.savefig('graph3_methane_scatter.png')
    plt.close()

    # 4. Identifikacija kandidata za život
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='GPS_LONG', y='GPS_LAT', hue='H2O_Postotak', palette='viridis', alpha=0.4)
    plt.scatter(kandidati['GPS_LONG'], kandidati['GPS_LAT'], color='red', marker='*', s=250, label='Kandidati za život')
    plt.title('Identifikacija kandidata za život')
    plt.legend()
    plt.savefig('scatter_plot.png')
    plt.close()

    # 5. NOVO:
    try:
        slika_kratera = plt.imread('jezero_crater_satellite_map.jpg')

        # Izračunavanje granica u usporedbi s mojim cistim podacima
        extent_koordinate = [
            data['GPS_LONG'].min(), data['GPS_LONG'].max(),
            data['GPS_LAT'].min(), data['GPS_LAT'].max()
        ]

        plt.figure(figsize=(12, 8))
        # Prikaz slike
        plt.imshow(slika_kratera, extent=extent_koordinate, aspect='auto', alpha=0.7)

        # Crtanje točaka
        sns.scatterplot(data=data, x='GPS_LONG', y='GPS_LAT', color='teal', s=15, alpha=0.5)
        plt.scatter(kandidati['GPS_LONG'], kandidati['GPS_LAT'], color='yellow', marker='*', s=300,
        edgecolor='black', label='Ciljevi bušenja')

        plt.title('Završna mapa misije - Satelitski prikaz (Jezero Crater)')
        plt.legend()
        plt.savefig('jezero_missija_map.png')
        plt.close()
    except Exception as e:
        print(f"Greška")

kreiraj_grafove(df_cisto, df_kandidati)

# JSON
lista_naloga = []

# Korištenje iterrows()
for _, redak in df_kandidati.iterrows():
    # NAVIGACIJA
    lista_naloga.append({
        "akcija": "NAVIGACIJA",
        "cilj_id": int(redak['ID_Uzorka']),
        "koordinate": {"lat": float(redak['GPS_LAT']), "lon": float(redak['GPS_LONG'])}
    })
    # SONDIRANJE
    lista_naloga.append({
        "akcija": "SONDIRANJE",
        "dubina": int(redak['Dubina_Busenja_cm'] * 10)
    })
    # SLANJE_PODATAKA
    lista_naloga.append({
        "akcija": "SLANJE_PODATAKA",
        "podaci": {
            "lat": float(redak['GPS_LAT']), "lon": float(redak['GPS_LONG']),
            "dubina_busenja_cm": float(redak['Dubina_Busenja_cm']),
            "Temp_Tla_C": float(redak['Temp_Tla_C']),
            "pH_Vrijednost": float(redak['pH_Vrijednost']),
            "H2O_Postotak": float(redak['H2O_Postotak']),
            "Metan_Senzor": redak['Metan_Senzor'],
            "Organske_Molekule": redak['Organske_Molekule']
        }
    })

def kreiraj_finalni_paket(nalozi):
    return {
        "misija": "NEXUS_Zavrsetak",
        "ucenik": "Ivan Jurcan",
        "nalog": nalozi
    }

moj_paket = kreiraj_finalni_paket(lista_naloga)

# Spremanje i slanje
with open("Zavrsni_5.json", 'w') as f:
    json.dump(moj_paket, f, indent=4)
print("JSON paket je spremljen.")

# server_url = "https://test3e4.centar-pozitron.hr/index.php"
# posalji_na_server(server_url, moj_paket)