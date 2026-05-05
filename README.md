# Misija Nexus: Analitički izvještaj
**Autor:** Ivan Jurcan
**Projekt:** Istraživanje kratera Jezero

## 1. Sažetak
Ovaj projekt obuhvaća obradu senzorskih podataka prikupljenih s površine Marsa, identifikaciju lokacija s visokim potencijalom za život te generiranje strukturiranog JSON naloga za rover.

## 2. Obrada podataka
Podaci su učitani iz dva izvora (lokacije i uzorci) te spojeni u jedinstvenu bazu. Provedeno je strogo filtriranje anomalija (npr. pH vrijednosti izvan 0-14, temperature iznad 100°C) kako bi se osigurala točnost analize.
Kandidati za život definirani su kao lokacije s istovremenom detekcijom metana i prisutnošću organskih molekula.

## 3. Rezultati i interpretacija vizualizacija
U sklopu analize generirano je 5 ključnih vizualizacija:

### A. Odnos temperature i vlage
![Graf 1](assets/graph1_temp_h2o.png)
*Interpretacija: Vidljivo je da se pozitivne detekcije metana grupiraju u specifičnim temperaturnim rasponima...*

### B. Satelitska mapa misije (Jezero Crater)
![Satelitska mapa](assets/jezero_mission_map.png)
*Interpretacija: Korištenjem 'extent' parametra, analitički rezultati su precizno preklopljeni sa satelitskom snimkom. Žute zvjezdice označavaju ciljeve za iduću fazu bušenja.*

*(Ovdje dodaj i ostala 3 grafa na isti način)*

## 4. Inženjerski dnevnik
Tijekom razvoja projekta riješeni su sljedeći tehnički izazovi:
1. **Problem s učitavanjem:** CSV datoteke su koristile ';' kao separator i ',' za decimale. Riješeno parametrom `sep=';'` i `decimal=','`.
2. **Greška pri izradi mape:** Python nije mogao pronaći satelitsku sliku zbog krivog naziva (`jezero_krater.jpg`). Ispravljeno korištenjem punog naziva `jezero_crater_satellite_map.jpg`.
3. **Poravnanje koordinata:** Inicijalno točke nisu odgovarale mapi. Problem je riješen dinamičkim izračunom `extent` parametra na temelju min/max GPS koordinata iz podataka.

## 5. Komunikacijski protokol
Finalni nalog je generiran u JSON formatu i sadrži tri akcije za svaku metu: Navigacija, Sondiranje i Slanje podataka.
