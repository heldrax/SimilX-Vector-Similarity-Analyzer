# SimilX – Vector Similarity Analyzer
Analyseur de similarité vectorielle multi‑dimensionnelle, avec visualisation, comparaison détaillée et interface graphique moderne.

---

## Présentation

SimilX est un outil interactif permettant de comparer deux vecteurs ou listes numériques,  
dimension par dimension, afin de mesurer leur similarité.

Il inclut :

- une interface graphique moderne (Tkinter)
- un système de thèmes clair/sombre
- un mini‑modèle Word2Vec simplifié pour générer des vecteurs
- une comparaison détaillée avec mise en évidence des valeurs proches
- un historique des comparaisons
- une visualisation graphique (matplotlib)
- l’export des résultats en JSON

SimilX est conçu pour être simple, pédagogique et puissant, idéal pour explorer la similarité numérique, tester des vecteurs, ou comprendre la logique des embeddings.

---

## Fonctionnalités

### Comparaison vectorielle
- Analyse dimension par dimension  
- Calcul de similarité numérique  
- Mise en évidence automatique des valeurs proches  

### Génération de vecteurs
- Mini‑modèle Word2Vec intégré  
- Vocabulaire et corpus d’entraînement personnalisables  
- Vecteurs multi‑dimensionnels  

### Interface graphique
- Tkinter moderne  
- Thème clair / sombre  
- Zones de debug, résultats, historique  
- Navigation par onglets  

### Visualisation
- Graphique matplotlib des deux vecteurs  
- Comparaison visuelle claire  

### Export
- Export JSON de l’historique complet  

---

## Installation

Assurez‑vous d’avoir Python 3.10+ installé.

Installation de matplotlib :

```bash
pip install matplotlib
