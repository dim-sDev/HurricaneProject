import pandas as pd
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import numpy as np

def getNumberOfHurricane(data: pd.DataFrame):
    ouragans = getSeparedHurricane(data)
    return len(ouragans)
    # # Afficher les données de chaque ouragan
    # for i, ouragan_data in enumerate(ouragans):
    #     print(f"\n Ouragans {ouragan_data['NAME'].values[0]} "
    #           f"de {ouragan_data['Hurricane_Date'].min()} "
    #           f"a {ouragan_data['Hurricane_Date'].max()} ")

def getSeparedHurricane(data: pd.DataFrame):
    grouped = data.groupby('SID')
    list_of_dataframes = []
    for group_name, group_data in grouped:
        # Crée un nouveau DataFrame pour chaque groupe
        grouped_df = pd.DataFrame(group_data)

        # Ajoute le DataFrame à la liste
        list_of_dataframes.append(grouped_df)

    return list_of_dataframes

def getSeparedHurricaneByName(data: pd.DataFrame):
    grouped = data.groupby(['NAME','year'])
    list_of_dataframes = []
    for group_name, group_data in grouped:
        # Crée un nouveau DataFrame pour chaque groupe
        grouped_df = pd.DataFrame(group_data)

        # Ajoute le DataFrame à la liste
        list_of_dataframes.append(grouped_df)

    return list_of_dataframes

def getOcurrenceDataframe(dataframes):
    # Dictionnaire pour stocker le nombre d'occurrences de lignes de chaque DataFrame
    occurrences = {}

    # Parcours de la liste de DataFrames
    for df in dataframes:
        num_rows = df.shape[0] # Récupère le nombre de lignes du DataFrame
        if num_rows in occurrences:
            occurrences[num_rows] += 1  # Incrémente le compteur d'occurrences pour ce nombre de lignes
        else:
            occurrences[num_rows] = 1  # Initialise le compteur d'occurrences pour ce nombre de lignes

    # Trouve le maximum d'occurrences de lignes
    max_occurrences = max(occurrences.values())
    key_max_occurrences = max(occurrences, key=occurrences.get)
    if key_max_occurrences < 2 :
        valeurs_triees = sorted(occurrences.values(), reverse=True)
        print(f"""
        Le nombre d'occurrence maximum étant : {max_occurrences} avec {key_max_occurrences} ligne par dataframe 
        nous récupèrerons la seconde valeur la plus haute
        """)
        max_occurrences = valeurs_triees[1]
        for cle, valeur in occurrences.items():
            if valeur == max_occurrences:
                key_max_occurrences = cle
                break
        print(f"""Le nombre d'occurrence max est maintenant : 
        {max_occurrences} avec {key_max_occurrences} ligne par dataframe""")

    # Liste des DataFrames ayant le maximum d'occurrences de lignes
    dataframes_with_max_occurrences = []

    for df in dataframes:
        if df.shape[0] == key_max_occurrences:
            dataframes_with_max_occurrences.append(df)

    # Affichage des résultats
    print(f"Maximum d'occurrences de lignes : {max_occurrences}")
    print(f"Clés correspondant à la valeur maximale : {key_max_occurrences}")
    print(f"{occurrences[key_max_occurrences]}")
    print("DataFrames ayant le maximum d'occurrences de lignes :")

    return dataframes_with_max_occurrences

def getMeanHurricane(liste_dataframes):
    def extraire_lat_long(dataframe):
        latitude = dataframe['LAT']
        longitude = dataframe['LON']
        return latitude, longitude

    latitudes_totales = []
    longitudes_totales = []

    for dataframe in liste_dataframes:
        lat, lon = extraire_lat_long(dataframe)
        latitudes_totales.append(lat)
        longitudes_totales.append(lon)


    for df in latitudes_totales:
        df.reset_index(drop=True, inplace=True)

    for df in longitudes_totales:
        df.reset_index(drop=True, inplace=True)

    moyenne_latitude = pd.concat(latitudes_totales,axis=1).mean(axis=0)
    moyenne_longitude = pd.concat(longitudes_totales, axis=1).mean(axis=0)
    moyenne_longitude_trees = sorted(moyenne_longitude)
    moyenne_latitude_trees = sorted(moyenne_latitude)

    # Trier les points en fonction de la longitude
    points_tries = sorted(zip(moyenne_latitude, moyenne_longitude), key=lambda x: x[1])
    latitudes_triees, longitudes_triees = zip(*points_tries)

    min_lat = moyenne_latitude.min()
    max_lat = moyenne_latitude.max()
    min_lon = moyenne_longitude.min()
    max_lon = moyenne_longitude.max()
    print(f"""
    La latitude moyenne est de {moyenne_latitude.mean()}
    La latitude min est de {min_lat}
    La latitude max est de {max_lat}
    
    La longitude moyenne est de {moyenne_longitude.mean()}
    La longitude min est de {min_lon}
    La longitude max est de {max_lon}
    """)
    # Calculer une marge pour étendre légèrement l'étendue de la carte
    margin = 1.0

    extent = [min_lon - margin, max_lon + margin, min_lat - margin, max_lat + margin]

    # Créer une nouvelle figure pour l'ouragan courant
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Tracer la courbe de trajectoire pour l'ouragan courant
    ax.plot(longitudes_triees, latitudes_triees, marker='o')
    # Ajouter des fonctionnalités cartographiques
    ax.coastlines()
    ax.gridlines()
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    # Titre du graphique
    plt.title(f"Trajectoire de l'ouragan type")

    # Afficher le graphique
    plt.show()

    fig.savefig('ouragan_type.png')

if __name__ == '__main__':
    data = pd.read_csv("../data/hurricanes_Past_In_Caribbean.csv")
    data_caribean = getSeparedHurricaneByName(data)
    liste = getOcurrenceDataframe(data_caribean)
    getMeanHurricane(liste)

