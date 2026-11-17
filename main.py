"""
Moduł Główny: Eksploracyjna Analiza Danych (EDA) oraz Data Wrangling
Projekt Zespołowy - Analiza Danych w Pythonie
Autorzy: Piotr Czarnecki, Mikołaj Grubba, Błażej Kujawski
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfiguracja estetyki wykresów
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (11, 7)

def wczytaj_i_oczyscz_dane(sciezka_pliku: str) -> pd.DataFrame:
    """
    Wczytuje surowy zbiór danych, przeprowadza proces data wranglingu,
    obsługuje braki danych, usuwa duplikaty oraz standaryzuje typy zmiennych.
    """
    print("[INFO] Wczytywanie surowego zbioru danych...")
    df = pd.read_csv(sciezka_pliku)
    
    print(f"Wymiary początkowe ramki danych: {df.shape}")
    
    # 1. Standaryzacja nazw kolumn (małe litery, usunięcie spacji)
    df.columns = df.columns.str.strip().str.lower()
    
    # 2. Identyfikacja i obsługa braków danych (imputacja medianą dla zmiennych numerycznych)
    kolumny_numeryczne = df.select_dtypes(include=[np.number]).columns
    for col in kolumny_numeryczne:
        if df[col].isnull().sum() > 0:
            mediana_val = df[col].median()
            df[col] = df[col].fillna(mediana_val)
            print(f"[CLEANING] Imputowano braki w kolumnie '{col}' medianą: {mediana_val}")
            
    # 3. Usuwanie duplikatów
    poczatkowa_l_wierszy = len(df)
    df = df.drop_duplicates(subset=['track_id'], keep='first')
    usunięto = poczatkowa_l_wierszy - len(df)
    print(f"[CLEANING] Usunięto zduplikowane rekordy: {usunięto}")
    
    # 4. Konwersja typów logicznych / kategorycznych
    if 'explicit' in df.columns:
        df['explicit'] = df['explicit'].astype(bool)
        
    return df

def wyznacz_statystyki_opisowe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generuje kompleksowe statystyki opisowe dla kluczowych wskaźników akustycznych
    i miar popularności.
    """
    print("\n--- ANALIZA OPISOWA: Miary tendencji centralnej i rozproszenia ---")
    zmienne_kluczowe = ['popularity', 'danceability', 'energy', 'tempo', 'loudness', 'acousticness']
    
    # Wyznaczenie podstawowych miar statystycznych
    staty = df[zmienne_kluczowe].describe().T[['count', 'mean', 'std', 'min', '50%', 'max']]
    staty = staty.rename(columns={'50%': 'median'})
    
    # Dodanie miary rozstępu ćwiartkowego (IQR) dla oceny leptokurtyczności i asymetrii rozkładów
    q25 = df[zmienne_kluczowe].quantile(0.25)
    q75 = df[zmienne_kluczowe].quantile(0.75)
    staty['iqr'] = q75 - q25
    
    return staty

def przeprowadz_agregacje(df: pd.DataFrame) -> pd.DataFrame:
    """
    Przeprowadza wielowymiarową agregację danych (.groupby) w przekroju gatunków muzycznych.
    """
    if 'track_genre' in df.columns:
        print("\n--- AGREGACJA W PRZEKROJU GATUNKÓW MUZYCZNYCH ---")
        agregacja = (
            df.groupby('track_genre', observed=True)
            .agg(
                liczba_utworow=('track_id', 'size'),
                srednia_popularnosc=('popularity', 'mean'),
                mediana_energii=('energy', 'median'),
                mediana_tanecznosci=('danceability', 'median')
            )
            .sort_values(by='srednia_popularnosc', ascending=False)
        )
        return agregacja
    return pd.DataFrame()

def generuj_wizualizacje(df: pd.DataFrame):
    """
    Tworzy profesjonalne wizualizacje analityczne (macierz korelacji oraz rozkład cech).
    """
    print("\n[INFO] Generowanie wizualizacji danych...")
    
    # Wykres 1: Macierz korelacji Pearsona dla cech akustycznych
    plt.figure(figsize=(10, 8))
    cechy_korelacji = ['popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo']
    matrix_corr = df[cechy_korelacji].corr()
    
    sns.heatmap(matrix_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.6, cbar_kws={'label': 'Współczynnik korelacji'})
    plt.title("Macierz Korelacji Cech Akustycznych i Popularności Utworów", fontsize=14, pad=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig('korelacje_akustyczne.png', dpi=300)
    plt.show()

# --- GŁÓWNA PROCEDURA WYKONAWCZA ---
if __name__ == "__main__":
    # Ścieżka do pliku CSV w repozytorium (dostosuj nazwę pliku do pobranego zbioru)
    PLIK_DANYCH = "dataset.csv" 
    
    try:
        # 1. Wrangling i Czyszczenie
        df_clean = wczytaj_i_oczyscz_dane(PLIK_DANYCH)
        
        # 2. Analiza Opisowa
        tabela_statystyk = wyznacz_statystyki_opisowe(df_clean)
        display(tabela_statystyk) if 'display' in globals() else print(tabela_statystyk)
        
        # 3. Agregacja
        tabela_agregacji = przeprowadz_agregacje(df_clean)
        display(tabela_agregacji) if 'display' in globals() else print(tabela_agregacji)
        
        # 4. Wizualizacja
        generuj_wizualizacje(df_clean)
        
        print("\n[SUKCES] Proces analizy danych zakończył się pomyślnie. Raport i wykresy są gotowe.")
        
    except FileNotFoundError:
        print(f"[BŁĄD] Nie znaleziono pliku '{PLIK_DANYCH}'. Umieść plik CSV w katalogu roboczym projektu.")