"""
SimilX - Module de chargement du modèle vectoriel
-------------------------------------------------

Ce module fournit :
- un vocabulaire
- un corpus d'entraînement
- un espace vectoriel initialisé
- un entraînement léger basé sur la co‑occurrence
- une description claire du modèle

Il est conçu pour être importé dans SimilX.py.
"""

import random

# ================== INITIALISATION DES VECTEURS ==================

def init_vectors(vocab, dim=8):
    """Crée un vecteur aléatoire pour chaque mot du vocabulaire."""
    return {word: [random.random() for _ in range(dim)] for word in vocab}

# ================== ENTRAÎNEMENT SIMPLIFIÉ ==================

def train_vectors(vectors, corpus, lr=0.01):
    """
    Entraîne légèrement les vecteurs en rapprochant les mots
    qui apparaissent ensemble dans le corpus.
    """
    for sentence in corpus:
        for i, word in enumerate(sentence):
            context = []
            if i > 0:
                context.append(sentence[i - 1])
            if i < len(sentence) - 1:
                context.append(sentence[i + 1])

            for ctx in context:
                for d in range(len(vectors[word])):
                    vectors[word][d] += lr * (vectors[ctx][d] - vectors[word][d])

# ================== CHARGEMENT DU MODELE ==================

def load_model():
    """
    Initialise le vocabulaire, le corpus et les vecteurs,
    puis entraîne le modèle.

    Retourne :
    - vocabulaire
    - vecteurs entraînés
    - corpus
    - description du modèle
    """

    vocab = ["chien", "chat", "mange", "boit"]

    corpus = [
        ["chien", "mange"],
        ["chat", "mange"],
        ["chien", "boit"],
        ["chat", "boit"]
    ]

    vectors = init_vectors(vocab)
    train_vectors(vectors, corpus)

    description = (
        "Modèle SimilX chargé avec succès.\n\n"
        "Ce modèle utilise un mini‑système Word2Vec simplifié basé sur :\n"
        " • Un vocabulaire de 4 mots\n"
        " • Un corpus d'entraînement de 4 phrases\n"
        " • Des vecteurs de 8 dimensions générés aléatoirement\n"
        " • Un apprentissage léger basé sur la co‑occurrence\n\n"
        "Il permet d'analyser la similarité entre deux vecteurs ou listes,\n"
        "dimension par dimension, afin de mesurer leur proximité numérique.\n"
    )

    return vocab, vectors, corpus, description
