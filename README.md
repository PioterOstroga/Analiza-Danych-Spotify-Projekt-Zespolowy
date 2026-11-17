# 🎵 Eksploracyjna Analiza Danych Rynku Muzycznego (Spotify) · Projekt Zespołowy

Projekt realizowany w ramach zajęć **Analiza danych w Pythonie (2026)**. Celem badania jest wielowymiarowa analiza przekrojowa (*cross-sectional*) zbioru utworów muzycznych dostępnych na platformie Spotify, identyfikacja determinant popularności utworów oraz segmentacja gatunkowa na podstawie parametrów akustycznych.

---

## 👥 Zespół Projektowy
* **Piotr Czarnecki** – Lider Projektu / Analiza Opisowa i Modelowanie
* **Mikołaj Grubba** – Inżynieria Danych / Git Workflow i Czyszczenie Danych
* **Błażej Kujawski** – Wizualizacja Danych / Dokumentacja Techniczna

---

## 📊 Charakterystyka Zbioru Danych
Badanie opiera się na zbiorze **Spotify Tracks Dataset** (źródło: Kaggle), obejmującym ponad **114 000 obserwacji** oraz **20 zmiennych** opisujących zarówno metadane rynkowe, jak i strukturę akustyczną nagrań:
* **Zmienne identyfikacyjne i kategoryczne:** `track_id`, `artists`, `album_name`, `track_name`, `track_genre`, `explicit`, `key`, `mode`, `time_signature`.
* **Zmienne ciągłe i wskaźniki akustyczne:** `popularity` (0–100), `duration_ms`, `danceability`, `energy`, `loudness`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`.

---

## 📂 Struktura Repozytorium
