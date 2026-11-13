"""Module de gestion, de nettoyage et d'exploration des données (INF1007 - Projet 2)."""

import os
import matplotlib.pyplot as plt
import pandas as pd


def charger_et_nettoyer_donnees(chemin_fichier: str) -> pd.DataFrame:
    """Charge le jeu de données des jeux vidéo et nettoie les valeurs manquantes.

    Paramètres :
        chemin_fichier (str) : Chemin d'accès vers le fichier CSV.

    Retourne :
        pd.DataFrame : Tableau nettoyé avec les colonnes sélectionnées.

    Lève :
        FileNotFoundError : Si le chemin du fichier n'existe pas.
    """
    if not os.path.exists(chemin_fichier):
        raise FileNotFoundError(f"Le fichier '{chemin_fichier}' est introuvable.")

    # 1. Lecture du fichier CSV
    df = pd.read_csv(chemin_fichier)

    # 2. Conservation des colonnes pertinentes
    colonnes_requises = [
        "Platform",
        "Genre",
        "Critic_Score",
        "User_Score",
        "Global_Sales",
    ]
    df_filtre = df[colonnes_requises].copy()

    # 3. Conversion de User_Score : transforme 'tbd' ou erreurs en NaN
    df_filtre["User_Score"] = pd.to_numeric(
        df_filtre["User_Score"], errors="coerce"
    )

    # 4. Suppression des lignes comportant des cases vides
    df_propre = df_filtre.dropna().reset_index(drop=True)

    return df_propre


def sauvegarder_graphique_exploration(
    df: pd.DataFrame, chemin_sortie: str = "graphique_exploration.png"
) -> None:
    """Génère et sauvegarde un graphique montrant l'impact des notes sur les ventes.

    Paramètres :
        df (pd.DataFrame) : Le tableau de données nettoyé.
        chemin_sortie (str) : Chemin et nom du fichier image à enregistrer.
    """
    plt.figure(figsize=(9, 5))
    plt.scatter(
        df["Critic_Score"],
        df["Global_Sales"],
        alpha=0.4,
        color= "#2b5c8f",
        edgecolors="none",
        vmax=40
    )
    plt.title("Relation entre la note Metacritic et les ventes mondiales")
    plt.xlabel("Score des critiques (sur 100)")
    plt.ylabel("Ventes mondiales (en millions d'exemplaires)")
    plt.grid(True, linestyle="--", alpha=0.5)

    # Sauvegarde de l'image
    plt.savefig(chemin_sortie, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    # Point d'entrée pour tester directement le module
    chemin_donnees = os.path.join("donnees", "jeux_video.csv")
    
    print("Chargement et nettoyage des données...")
    donnees = charger_et_nettoyer_donnees(chemin_donnees)
    
    print(f"\nSuccès : {len(donnees)} observations prêtes pour l'entraînement.")
    print("\nAperçu des 5 premières lignes :")
    print(donnees.head())

    print("\nGénération du graphique d'exploration...")
    sauvegarder_graphique_exploration(donnees)
    print("Graphique sauvegardé sous 'graphique_exploration.png'.")