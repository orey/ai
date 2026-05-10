#!/usr/bin/env python3
"""
Projecteur Sémantique — semantic_projector.py
==============================================
Projette un texte français sur des dimensions sémantiques configurables.

Dépendances :
    pip install spacy snowballstemmer scikit-learn matplotlib

Usage :
    python3 semantic_projector.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import json
import re
import os
import sys
import collections
import threading

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from snowballstemmer import stemmer as Stemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─────────────────────────────────────────────────────────────────────────────
# LEXIQUES PRÉDÉFINIS (français)
# Chaque dimension = liste de mots représentatifs.
# La correspondance peut être "exact" (racine Snowball) ou "similarity" (cosine TF-IDF).
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_DIMENSIONS = {
    "Émotions positives": {
        "method": "exact",
        "color": "#2ecc71",
        "words": [
            "joie", "bonheur", "amour", "espoir", "confiance", "gratitude",
            "enthousiasme", "fierté", "sérénité", "plaisir", "optimisme",
            "contentement", "satisfaction", "tendresse", "affection", "gaieté",
            "allégresse", "euphorie", "ravissement", "émerveillement", "réconfort",
            "bienveillance", "douceur", "charme", "félicité", "épanouissement",
        ],
    },
    "Émotions négatives": {
        "method": "exact",
        "color": "#e74c3c",
        "words": [
            "peur", "tristesse", "colère", "anxiété", "honte", "culpabilité",
            "désespoir", "angoisse", "rancœur", "haine", "jalousie", "regret",
            "mélancolie", "souffrance", "douleur", "détresse", "inquiétude",
            "frustration", "déception", "mépris", "humiliation", "terreur",
            "rage", "solitude", "abattement", "amertume", "affliction",
        ],
    },
    "Registre formel": {
        "method": "exact",
        "color": "#2980b9",
        "words": [
            "néanmoins", "toutefois", "cependant", "par conséquent", "ainsi",
            "afin", "conformément", "notamment", "préalablement", "susmentionné",
            "ledit", "ladite", "ci-joint", "en vertu", "au regard de",
            "il convient", "il est à noter", "dans le cadre de", "en l'espèce",
            "à cet égard", "audit", "précité", "par ailleurs", "en outre",
        ],
    },
    "Registre familier": {
        "method": "exact",
        "color": "#e67e22",
        "words": [
            "super", "truc", "machin", "sympa", "cool", "vachement", "carrément",
            "franchement", "bizarre", "zarbi", "chelou", "relou", "kiffer",
            "péter", "bouffer", "flipper", "galérer", "se barrer", "kiffer",
            "grave", "trop", "énorme", "ouf", "bof", "mouais", "dingue",
        ],
    },
    "Temporalité passé": {
        "method": "exact",
        "color": "#8e44ad",
        "words": [
            "hier", "autrefois", "jadis", "naguère", "anciennement", "passé",
            "antan", "auparavant", "précédemment", "antérieurement", "révolu",
            "ancien", "historique", "tradition", "mémoire", "souvenir",
            "autrefois", "remontait", "fondé", "héritage", "origine",
        ],
    },
    "Temporalité futur": {
        "method": "exact",
        "color": "#27ae60",
        "words": [
            "demain", "bientôt", "prochainement", "futur", "avenir", "ultérieurement",
            "prévision", "perspective", "anticipation", "projection", "objectif",
            "promesse", "ambition", "espoir", "tendance", "innovation", "progrès",
            "développement", "croissance", "évolution", "transformation",
        ],
    },
    "Valeurs morales": {
        "method": "similarity",
        "color": "#16a085",
        "words": [
            "honnêteté", "justice", "loyauté", "intégrité", "courage", "respect",
            "dignité", "solidarité", "équité", "compassion", "responsabilité",
            "générosité", "humilité", "tolérance", "vertu", "éthique", "morale",
            "droiture", "bienveillance", "fraternité",
        ],
    },
    "Champ lexical technique": {
        "method": "similarity",
        "color": "#7f8c8d",
        "words": [
            "système", "processus", "protocole", "interface", "algorithme",
            "données", "paramètre", "configuration", "infrastructure", "module",
            "composant", "architecture", "déploiement", "intégration", "requête",
            "serveur", "réseau", "base de données", "framework", "API",
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# MOTEUR D'ANALYSE SÉMANTIQUE
# ─────────────────────────────────────────────────────────────────────────────

class SemanticEngine:
    """Analyse un texte et projette ses mots sur des dimensions sémantiques."""

    STOPWORDS_FR = {
        "le", "la", "les", "un", "une", "des", "de", "du", "et", "en", "au",
        "aux", "ce", "se", "sa", "son", "ses", "mon", "ma", "mes", "ton",
        "ta", "tes", "notre", "votre", "leur", "nous", "vous", "ils", "elles",
        "je", "tu", "il", "elle", "on", "que", "qui", "quoi", "dont", "où",
        "par", "pour", "sur", "sous", "dans", "avec", "sans", "entre", "vers",
        "très", "plus", "moins", "bien", "aussi", "même", "tout", "tous",
        "est", "sont", "était", "être", "avoir", "été", "fait", "faire",
        "a", "y", "en", "si", "ne", "pas", "ni", "car", "mais", "ou",
    }

    def __init__(self):
        self.fr_stemmer = Stemmer("french")

    def stem(self, word: str) -> str:
        return self.fr_stemmer.stemWord(word.lower())

    def tokenize(self, text: str) -> list[str]:
        """Tokenise le texte, retire la ponctuation et les stopwords."""
        tokens = re.findall(r"\b[a-zàâçéèêëîïôùûüÿæœ'-]+\b", text.lower())
        return [t for t in tokens if t not in self.STOPWORDS_FR and len(t) > 2]

    def build_stem_index(self, words: list[str]) -> dict[str, str]:
        """{ racine → mot_original } pour un lexique."""
        return {self.stem(w): w for w in words}

    def analyze(self, text: str, dimensions: dict) -> dict:
        """
        Retourne pour chaque dimension :
            {
              "matches": [(mot_texte, mot_lexique, occurrences), ...],
              "score": float,      # score total pondéré
              "method": str,
            }
        """
        tokens = self.tokenize(text)
        if not tokens:
            return {}

        # Comptage des occurrences des tokens bruts
        token_counts = collections.Counter(tokens)

        results = {}
        for dim_name, dim_cfg in dimensions.items():
            method = dim_cfg.get("method", "exact")
            lex_words = dim_cfg["words"]

            if method == "exact":
                matches = self._exact_match(token_counts, lex_words)
            else:
                matches = self._similarity_match(token_counts, tokens, lex_words)

            score = sum(occ for _, _, occ in matches)
            results[dim_name] = {
                "matches": sorted(matches, key=lambda x: x[2], reverse=True),
                "score": score,
                "method": method,
                "color": dim_cfg.get("color", "#888888"),
            }

        return results

    def _exact_match(self, token_counts: dict, lex_words: list) -> list:
        """Correspondance par radical Snowball."""
        stem_index = self.build_stem_index(lex_words)
        matches = []
        for token, count in token_counts.items():
            token_stem = self.stem(token)
            if token_stem in stem_index:
                matches.append((token, stem_index[token_stem], count))
        return matches

    def _similarity_match(
        self, token_counts: dict, tokens: list, lex_words: list, threshold: float = 0.35
    ) -> list:
        """
        Correspondance par similarité cosine TF-IDF.
        Chaque token du texte est comparé au lexique de la dimension.
        """
        # D'abord exact pour les correspondances directes
        stem_index = self.build_stem_index(lex_words)
        exact_hits = set()
        matches = []

        for token, count in token_counts.items():
            token_stem = self.stem(token)
            if token_stem in stem_index:
                matches.append((token, stem_index[token_stem], count))
                exact_hits.add(token)

        # Ensuite TF-IDF pour les tokens non capturés
        remaining = [t for t in token_counts if t not in exact_hits]
        if remaining and len(lex_words) >= 2:
            try:
                corpus = lex_words + remaining
                vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
                tfidf = vec.fit_transform(corpus)
                lex_matrix = tfidf[: len(lex_words)]
                tok_matrix = tfidf[len(lex_words) :]
                sims = cosine_similarity(tok_matrix, lex_matrix)  # (n_tokens, n_lex)

                for i, token in enumerate(remaining):
                    best_idx = np.argmax(sims[i])
                    best_score = sims[i, best_idx]
                    if best_score >= threshold:
                        matches.append(
                            (token, lex_words[best_idx], token_counts[token])
                        )
            except Exception:
                pass  # TF-IDF peut échouer sur corpus très court

        return matches


# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE GRAPHIQUE
# ─────────────────────────────────────────────────────────────────────────────

APP_TITLE = "Projecteur Sémantique"
BG = "#f5f6fa"
PANEL_BG = "#ffffff"
ACCENT = "#3d5a80"
ACCENT_LIGHT = "#e0eaf4"
TEXT_FG = "#2c3e50"
MUTED = "#7f8c8d"
BORDER = "#dce1e7"

FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_MONO  = ("Consolas", 10)
FONT_SMALL = ("Segoe UI", 9)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1200x760")
        self.configure(bg=BG)
        self.resizable(True, True)

        self.engine = SemanticEngine()
        self.dimensions = {k: dict(v) for k, v in DEFAULT_DIMENSIONS.items()}
        self.analysis_results = {}

        self._build_ui()
        self._refresh_dim_list()

    # ── Construction de l'UI ─────────────────────────────────────────────────

    def _build_ui(self):
        # ── Barre d'outils ──
        toolbar = tk.Frame(self, bg=ACCENT, height=44)
        toolbar.pack(fill="x", side="top")
        toolbar.pack_propagate(False)

        tk.Label(toolbar, text="⬡  " + APP_TITLE, bg=ACCENT, fg="white",
                 font=("Segoe UI", 11, "bold")).pack(side="left", padx=16, pady=10)

        for label, cmd in [
            ("📂 Ouvrir texte", self._load_file),
            ("💾 Exporter JSON", self._export_json),
            ("📊 Exporter graphique", self._export_chart),
        ]:
            tk.Button(toolbar, text=label, bg=ACCENT, fg="white",
                      activebackground="#2c4a6e", activeforeground="white",
                      relief="flat", padx=10, font=FONT_SMALL, cursor="hand2",
                      command=cmd).pack(side="left", padx=2, pady=6)

        # ── Corps principal ──
        paned = tk.PanedWindow(self, orient="horizontal", bg=BG, sashwidth=6,
                               sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=8, pady=8)

        # Panneau gauche : texte + dimensions
        left = tk.Frame(paned, bg=BG)
        paned.add(left, minsize=340)
        self._build_left(left)

        # Panneau droit : résultats
        right = tk.Frame(paned, bg=BG)
        paned.add(right, minsize=560)
        self._build_right(right)

    def _build_left(self, parent):
        # ── Saisie du texte ──
        text_frame = self._card(parent, "Texte à analyser")
        text_frame.pack(fill="both", expand=True, pady=(0, 6))

        self.text_input = scrolledtext.ScrolledText(
            text_frame, wrap="word", font=FONT_LABEL, bg=PANEL_BG, fg=TEXT_FG,
            relief="flat", borderwidth=0, insertbackground=ACCENT, height=12
        )
        self.text_input.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        btn_bar = tk.Frame(text_frame, bg=PANEL_BG)
        btn_bar.pack(fill="x", padx=8, pady=(0, 8))
        self._btn(btn_bar, "⚡ Analyser", self._run_analysis, primary=True).pack(
            side="left", padx=(0, 6))
        self._btn(btn_bar, "✕ Effacer", self._clear_text).pack(side="left")

        # ── Dimensions ──
        dim_frame = self._card(parent, "Dimensions sémantiques")
        dim_frame.pack(fill="both", expand=True)

        toolbar_dim = tk.Frame(dim_frame, bg=PANEL_BG)
        toolbar_dim.pack(fill="x", padx=8, pady=(0, 4))
        self._btn(toolbar_dim, "+ Nouvelle", self._add_dimension).pack(side="left", padx=(0, 4))
        self._btn(toolbar_dim, "✎ Éditer",   self._edit_dimension).pack(side="left", padx=(0, 4))
        self._btn(toolbar_dim, "✕ Supprimer",self._delete_dimension).pack(side="left")

        # Liste des dimensions avec checkboxes
        list_outer = tk.Frame(dim_frame, bg=PANEL_BG, relief="flat",
                              highlightbackground=BORDER, highlightthickness=1)
        list_outer.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.dim_canvas = tk.Canvas(list_outer, bg=PANEL_BG, highlightthickness=0)
        dim_scroll = ttk.Scrollbar(list_outer, orient="vertical",
                                   command=self.dim_canvas.yview)
        self.dim_canvas.configure(yscrollcommand=dim_scroll.set)
        dim_scroll.pack(side="right", fill="y")
        self.dim_canvas.pack(side="left", fill="both", expand=True)

        self.dim_list_frame = tk.Frame(self.dim_canvas, bg=PANEL_BG)
        self.dim_canvas.create_window((0, 0), window=self.dim_list_frame, anchor="nw")
        self.dim_list_frame.bind(
            "<Configure>",
            lambda e: self.dim_canvas.configure(
                scrollregion=self.dim_canvas.bbox("all"))
        )

        # Variables pour les checkboxes des dimensions
        self.dim_vars = {}   # dim_name -> BooleanVar
        self.dim_selected = tk.StringVar()  # dimension sélectionnée pour édition

    def _build_right(self, parent):
        # Notebook : Graphique / Détail / Classement global
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=[12, 6], font=FONT_LABEL)

        # Tab 1 : Graphique
        tab_chart = tk.Frame(nb, bg=PANEL_BG)
        nb.add(tab_chart, text="📊  Graphique")
        self._build_chart_tab(tab_chart)

        # Tab 2 : Détail par dimension
        tab_detail = tk.Frame(nb, bg=PANEL_BG)
        nb.add(tab_detail, text="🔍  Détail")
        self._build_detail_tab(tab_detail)

        # Tab 3 : Classement global des mots
        tab_rank = tk.Frame(nb, bg=PANEL_BG)
        nb.add(tab_rank, text="📋  Classement")
        self._build_rank_tab(tab_rank)

        self.notebook = nb

    def _build_chart_tab(self, parent):
        self.fig = Figure(figsize=(7, 5), dpi=96, facecolor=PANEL_BG)
        self.ax = self.fig.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
        self._draw_empty_chart()

    def _build_detail_tab(self, parent):
        # Sélecteur de dimension
        sel_bar = tk.Frame(parent, bg=PANEL_BG)
        sel_bar.pack(fill="x", padx=8, pady=(8, 4))
        tk.Label(sel_bar, text="Dimension :", bg=PANEL_BG, fg=TEXT_FG,
                 font=FONT_LABEL).pack(side="left")
        self.detail_dim_var = tk.StringVar()
        self.detail_dim_combo = ttk.Combobox(sel_bar, textvariable=self.detail_dim_var,
                                             state="readonly", width=30, font=FONT_LABEL)
        self.detail_dim_combo.pack(side="left", padx=6)
        self.detail_dim_combo.bind("<<ComboboxSelected>>", lambda e: self._show_detail())

        # Tableau de détail
        cols = ("Mot du texte", "Correspondance lexique", "Occurrences", "Méthode")
        self.detail_tree = ttk.Treeview(parent, columns=cols, show="headings",
                                        height=18)
        for col in cols:
            self.detail_tree.heading(col, text=col)
            self.detail_tree.column(col, anchor="center", width=140)
        self.detail_tree.pack(fill="both", expand=True, padx=8, pady=4)

        detail_scroll = ttk.Scrollbar(parent, orient="vertical",
                                      command=self.detail_tree.yview)
        self.detail_tree.configure(yscrollcommand=detail_scroll.set)

    def _build_rank_tab(self, parent):
        # Tableau global : mot → dimensions qui l'ont capturé
        cols = ("Mot", "Occurrences", "Dimensions")
        self.rank_tree = ttk.Treeview(parent, columns=cols, show="headings", height=22)
        for col, w in zip(cols, [160, 100, 400]):
            self.rank_tree.heading(col, text=col)
            self.rank_tree.column(col, anchor="w", width=w)
        scrollbar = ttk.Scrollbar(parent, orient="vertical",
                                  command=self.rank_tree.yview)
        self.rank_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)
        self.rank_tree.pack(fill="both", expand=True, padx=8, pady=8)

    # ── Helpers UI ───────────────────────────────────────────────────────────

    def _card(self, parent, title: str) -> tk.Frame:
        """Crée un panneau carte avec titre."""
        outer = tk.Frame(parent, bg=BG)
        tk.Label(outer, text=title, bg=BG, fg=ACCENT,
                 font=FONT_TITLE).pack(anchor="w", padx=2, pady=(4, 2))
        inner = tk.Frame(outer, bg=PANEL_BG, relief="flat",
                         highlightbackground=BORDER, highlightthickness=1)
        inner.pack(fill="both", expand=True)
        return inner

    def _btn(self, parent, text: str, cmd, primary=False) -> tk.Button:
        bg = ACCENT if primary else "#ecf0f1"
        fg = "white" if primary else TEXT_FG
        abg = "#2c4a6e" if primary else "#d5dbdb"
        return tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                         activebackground=abg, activeforeground=fg,
                         relief="flat", font=FONT_SMALL, padx=10, pady=4,
                         cursor="hand2", borderwidth=0)

    # ── Gestion des dimensions ────────────────────────────────────────────────

    def _refresh_dim_list(self):
        """Reconstruit la liste des dimensions avec checkboxes."""
        for w in self.dim_list_frame.winfo_children():
            w.destroy()

        # Conserve les variables existantes
        old_vars = {k: v.get() for k, v in self.dim_vars.items()}
        self.dim_vars = {}

        for dim_name in self.dimensions:
            var = tk.BooleanVar(value=old_vars.get(dim_name, True))
            self.dim_vars[dim_name] = var

            row = tk.Frame(self.dim_list_frame, bg=PANEL_BG)
            row.pack(fill="x", padx=4, pady=1)

            color = self.dimensions[dim_name].get("color", "#888")
            method = self.dimensions[dim_name].get("method", "exact")
            method_icon = "≈" if method == "similarity" else "="

            # Carré de couleur
            tk.Label(row, bg=color, width=2, relief="flat").pack(side="left", padx=(4, 6))

            cb = tk.Checkbutton(row, text=dim_name, variable=var,
                                bg=PANEL_BG, fg=TEXT_FG, font=FONT_LABEL,
                                activebackground=PANEL_BG, selectcolor=PANEL_BG,
                                anchor="w", cursor="hand2",
                                command=lambda n=dim_name: self._select_dim(n))
            cb.pack(side="left", fill="x", expand=True)

            tk.Label(row, text=f"[{method_icon}]", bg=PANEL_BG, fg=MUTED,
                     font=FONT_SMALL).pack(side="right", padx=4)

    def _select_dim(self, name: str):
        self.dim_selected.set(name)

    def _add_dimension(self):
        DimensionEditor(self, title="Nouvelle dimension", on_save=self._save_new_dim)

    def _edit_dimension(self):
        sel = self.dim_selected.get()
        if not sel or sel not in self.dimensions:
            messagebox.showinfo("Édition", "Sélectionnez d'abord une dimension.")
            return
        DimensionEditor(self, title=f"Éditer : {sel}",
                        initial=self.dimensions[sel],
                        initial_name=sel,
                        on_save=lambda name, cfg: self._save_edit_dim(sel, name, cfg))

    def _delete_dimension(self):
        sel = self.dim_selected.get()
        if not sel or sel not in self.dimensions:
            messagebox.showinfo("Suppression", "Sélectionnez d'abord une dimension.")
            return
        if messagebox.askyesno("Supprimer", f"Supprimer « {sel} » ?"):
            del self.dimensions[sel]
            self.dim_selected.set("")
            self._refresh_dim_list()

    def _save_new_dim(self, name: str, cfg: dict):
        if name in self.dimensions:
            messagebox.showerror("Erreur", f"La dimension « {name} » existe déjà.")
            return
        self.dimensions[name] = cfg
        self._refresh_dim_list()

    def _save_edit_dim(self, old_name: str, new_name: str, cfg: dict):
        if new_name != old_name and new_name in self.dimensions:
            messagebox.showerror("Erreur", f"Le nom « {new_name} » est déjà utilisé.")
            return
        del self.dimensions[old_name]
        self.dimensions[new_name] = cfg
        self.dim_selected.set(new_name)
        self._refresh_dim_list()

    # ── Analyse ───────────────────────────────────────────────────────────────

    def _run_analysis(self):
        text = self.text_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Texte vide", "Saisissez ou chargez un texte.")
            return

        # Filtre les dimensions activées
        active_dims = {
            k: v for k, v in self.dimensions.items()
            if self.dim_vars.get(k, tk.BooleanVar(value=True)).get()
        }

        if not active_dims:
            messagebox.showwarning("Aucune dimension", "Activez au moins une dimension.")
            return

        self.analysis_results = self.engine.analyze(text, active_dims)
        self._update_chart()
        self._update_detail_tab()
        self._update_rank_tab()
        self.notebook.select(0)

    def _clear_text(self):
        self.text_input.delete("1.0", "end")

    # ── Visualisation ─────────────────────────────────────────────────────────

    def _draw_empty_chart(self):
        self.ax.clear()
        self.ax.set_facecolor(PANEL_BG)
        self.fig.patch.set_facecolor(PANEL_BG)
        self.ax.text(0.5, 0.5, "Analysez un texte pour voir les résultats",
                     ha="center", va="center", color=MUTED,
                     fontsize=12, transform=self.ax.transAxes)
        self.ax.axis("off")
        self.chart_canvas.draw()

    def _update_chart(self):
        self.ax.clear()
        self.ax.set_facecolor(PANEL_BG)
        self.fig.patch.set_facecolor(PANEL_BG)

        if not self.analysis_results:
            self._draw_empty_chart()
            return

        # Trier par score décroissant
        sorted_dims = sorted(
            self.analysis_results.items(), key=lambda x: x[1]["score"], reverse=True
        )
        sorted_dims = [(n, d) for n, d in sorted_dims if d["score"] > 0]

        if not sorted_dims:
            self.ax.text(0.5, 0.5, "Aucune correspondance trouvée",
                         ha="center", va="center", color=MUTED,
                         fontsize=12, transform=self.ax.transAxes)
            self.ax.axis("off")
            self.chart_canvas.draw()
            return

        names  = [n for n, _ in sorted_dims]
        scores = [d["score"] for _, d in sorted_dims]
        colors = [d["color"] for _, d in sorted_dims]

        # Barres horizontales
        y_pos = range(len(names))
        bars = self.ax.barh(y_pos, scores, color=colors, height=0.6,
                            edgecolor="white", linewidth=0.8)

        # Valeurs au bout des barres
        for bar, score in zip(bars, scores):
            self.ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                         str(int(score)), va="center", ha="left",
                         fontsize=9, color=TEXT_FG)

        self.ax.set_yticks(list(y_pos))
        self.ax.set_yticklabels(names, fontsize=10, color=TEXT_FG)
        self.ax.set_xlabel("Score (occurrences projetées)", color=MUTED, fontsize=9)
        self.ax.set_title("Projection par dimension sémantique",
                          fontsize=11, color=ACCENT, pad=10)
        self.ax.tick_params(colors=MUTED)
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color(BORDER)
        self.ax.spines["bottom"].set_color(BORDER)
        self.ax.set_xlim(0, max(scores) * 1.15)

        self.fig.tight_layout()
        self.chart_canvas.draw()

    def _update_detail_tab(self):
        dims = list(self.analysis_results.keys())
        self.detail_dim_combo["values"] = dims
        if dims:
            self.detail_dim_var.set(dims[0])
            self._show_detail()

    def _show_detail(self):
        dim_name = self.detail_dim_var.get()
        for item in self.detail_tree.get_children():
            self.detail_tree.delete(item)

        if dim_name not in self.analysis_results:
            return

        data = self.analysis_results[dim_name]
        for i, (token, lex_word, count) in enumerate(data["matches"]):
            tag = "even" if i % 2 == 0 else "odd"
            self.detail_tree.insert("", "end",
                                    values=(token, lex_word, count, data["method"]),
                                    tags=(tag,))

        self.detail_tree.tag_configure("even", background="#f8fafb")
        self.detail_tree.tag_configure("odd",  background=PANEL_BG)

    def _update_rank_tab(self):
        for item in self.rank_tree.get_children():
            self.rank_tree.delete(item)

        # Agrège mot → {dim: count}
        word_dim_map = collections.defaultdict(lambda: {"count": 0, "dims": []})
        for dim_name, data in self.analysis_results.items():
            for token, _, count in data["matches"]:
                word_dim_map[token]["count"] = max(word_dim_map[token]["count"], count)
                word_dim_map[token]["dims"].append(dim_name)

        sorted_words = sorted(word_dim_map.items(),
                              key=lambda x: x[1]["count"], reverse=True)

        for i, (word, info) in enumerate(sorted_words):
            tag = "even" if i % 2 == 0 else "odd"
            dims_str = " | ".join(info["dims"])
            self.rank_tree.insert("", "end",
                                  values=(word, info["count"], dims_str),
                                  tags=(tag,))

        self.rank_tree.tag_configure("even", background="#f8fafb")
        self.rank_tree.tag_configure("odd",  background=PANEL_BG)

    # ── Actions fichier ───────────────────────────────────────────────────────

    def _load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Fichiers texte", "*.txt"), ("Tous", "*.*")]
        )
        if not path:
            return
        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", content)

    def _export_json(self):
        if not self.analysis_results:
            messagebox.showinfo("Export", "Lancez d'abord une analyse.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")]
        )
        if not path:
            return
        export = {}
        for dim, data in self.analysis_results.items():
            export[dim] = {
                "score": data["score"],
                "method": data["method"],
                "matches": [
                    {"mot": t, "lexique": l, "occurrences": c}
                    for t, l, c in data["matches"]
                ],
            }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(export, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Export", f"Résultats exportés vers :\n{path}")

    def _export_chart(self):
        if not self.analysis_results:
            messagebox.showinfo("Export", "Lancez d'abord une analyse.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")]
        )
        if not path:
            return
        self.fig.savefig(path, dpi=150, bbox_inches="tight",
                         facecolor=self.fig.get_facecolor())
        messagebox.showinfo("Export", f"Graphique enregistré :\n{path}")


# ─────────────────────────────────────────────────────────────────────────────
# ÉDITEUR DE DIMENSION
# ─────────────────────────────────────────────────────────────────────────────

class DimensionEditor(tk.Toplevel):
    """Fenêtre modale pour créer ou modifier une dimension sémantique."""

    COLORS = [
        "#2ecc71", "#e74c3c", "#3498db", "#e67e22", "#9b59b6",
        "#1abc9c", "#f39c12", "#e91e63", "#00bcd4", "#607d8b",
    ]

    def __init__(self, parent, title: str, on_save, initial: dict = None,
                 initial_name: str = ""):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()

        self.on_save = on_save
        self.selected_color = (initial or {}).get("color", self.COLORS[0])

        # ── Nom ──
        tk.Label(self, text="Nom de la dimension", bg=BG, fg=TEXT_FG,
                 font=FONT_LABEL).pack(anchor="w", padx=16, pady=(16, 2))
        self.name_var = tk.StringVar(value=initial_name)
        tk.Entry(self, textvariable=self.name_var, font=FONT_LABEL, width=42,
                 relief="flat", highlightthickness=1,
                 highlightbackground=BORDER).pack(padx=16, pady=(0, 8))

        # ── Méthode ──
        tk.Label(self, text="Méthode de correspondance", bg=BG, fg=TEXT_FG,
                 font=FONT_LABEL).pack(anchor="w", padx=16, pady=(4, 2))
        self.method_var = tk.StringVar(
            value=(initial or {}).get("method", "exact")
        )
        method_frame = tk.Frame(self, bg=BG)
        method_frame.pack(anchor="w", padx=16, pady=(0, 8))
        for val, label in [("exact", "Exacte (racine Snowball)"),
                           ("similarity", "Similarité (cosine TF-IDF)")]:
            tk.Radiobutton(method_frame, text=label, variable=self.method_var,
                           value=val, bg=BG, fg=TEXT_FG, font=FONT_LABEL,
                           activebackground=BG, selectcolor=BG).pack(side="left", padx=8)

        # ── Couleur ──
        tk.Label(self, text="Couleur", bg=BG, fg=TEXT_FG,
                 font=FONT_LABEL).pack(anchor="w", padx=16, pady=(4, 2))
        color_frame = tk.Frame(self, bg=BG)
        color_frame.pack(anchor="w", padx=16, pady=(0, 8))
        self.color_buttons = []
        for color in self.COLORS:
            btn = tk.Button(color_frame, bg=color, width=3, relief="flat",
                            cursor="hand2",
                            command=lambda c=color: self._pick_color(c))
            btn.pack(side="left", padx=2)
            self.color_buttons.append((color, btn))
        self._pick_color(self.selected_color)

        # ── Mots du lexique ──
        tk.Label(self, text="Mots du lexique (un par ligne)",
                 bg=BG, fg=TEXT_FG, font=FONT_LABEL).pack(anchor="w", padx=16, pady=(4, 2))
        self.words_text = scrolledtext.ScrolledText(
            self, font=FONT_MONO, width=46, height=14, bg=PANEL_BG, fg=TEXT_FG,
            relief="flat", borderwidth=1
        )
        self.words_text.pack(padx=16, pady=(0, 8))

        if initial:
            self.words_text.insert("1.0", "\n".join(initial.get("words", [])))

        # ── Boutons ──
        btn_bar = tk.Frame(self, bg=BG)
        btn_bar.pack(fill="x", padx=16, pady=(4, 16))
        tk.Button(btn_bar, text="Enregistrer", bg=ACCENT, fg="white",
                  activebackground="#2c4a6e", relief="flat", font=FONT_LABEL,
                  padx=14, pady=6, cursor="hand2",
                  command=self._save).pack(side="right", padx=(6, 0))
        tk.Button(btn_bar, text="Annuler", bg="#ecf0f1", fg=TEXT_FG,
                  relief="flat", font=FONT_LABEL, padx=14, pady=6, cursor="hand2",
                  command=self.destroy).pack(side="right")

        self.update_idletasks()
        self._center()

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = self.master.winfo_rootx() + (self.master.winfo_width() - w) // 2
        y = self.master.winfo_rooty() + (self.master.winfo_height() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _pick_color(self, color: str):
        self.selected_color = color
        for c, btn in self.color_buttons:
            btn.config(relief="sunken" if c == color else "flat",
                       highlightthickness=2 if c == color else 0,
                       highlightbackground="black" if c == color else BG)

    def _save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Le nom ne peut pas être vide.", parent=self)
            return
        raw_words = self.words_text.get("1.0", "end").strip()
        words = [w.strip() for w in raw_words.splitlines() if w.strip()]
        if not words:
            messagebox.showerror("Erreur", "Le lexique ne peut pas être vide.", parent=self)
            return
        cfg = {
            "method": self.method_var.get(),
            "color": self.selected_color,
            "words": words,
        }
        self.on_save(name, cfg)
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
