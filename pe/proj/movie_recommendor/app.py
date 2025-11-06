#!/usr/bin/env python3
"""
movie_recommender_imdb.py
Simple CLI Movie Recommender using your imdb.csv

Expected imdb.csv columns:
id,title,type,genres,averageRating,numVotes,releaseYear

Usage:
    pip install pandas scikit-learn
    python movie_recommender_imdb.py

Features:
- Parse multi-genre strings (comma-separated)
- User rates movies (like/dislike)
- Train DecisionTreeClassifier or RandomForestClassifier on user's ratings
- Recommend unwatched movies by predicted probability of "like"
- Persist ratings in user_ratings.json
"""

import os
import json
import sys
from textwrap import dedent

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

MOVIES_CSV = "imdb.csv"            # change if your file name differs
RATINGS_FILE = "user_ratings.json" # persisted user ratings

# Config
MIN_VOTES = 0  # filter out very obscure titles if you want (set to 0 to disable)
ALLOWED_TYPE = "movie"  # keep only rows where type == 'movie' (if present)
RECOMMEND_TOP_N = 10

def load_movies(csv_path=MOVIES_CSV):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Put imdb.csv in the same directory.")
        sys.exit(1)
    df = pd.read_csv(csv_path, low_memory=False)
    # Normalize column names if needed
    df = df.rename(columns={
        'title': 'title',
        'genres': 'genres',
        'averageRating': 'imdb',
        'numVotes': 'numVotes',
        'releaseYear': 'year',
        'type': 'type'
    })
    # Keep movies only (if type column exists)
    if 'type' in df.columns:
        df = df[df['type'].fillna('').str.lower() == ALLOWED_TYPE]
    # Filter by votes to reduce noise (optional)
    if 'numVotes' in df.columns:
        df = df[df['numVotes'].fillna(0) >= MIN_VOTES]

    
    # Keep necessary columns and drop duplicates
    want_cols = ['title', 'genres', 'imdb', 'numVotes', 'year']
    available = [c for c in want_cols if c in df.columns]
    df = df[available].drop_duplicates(subset=['title']).reset_index(drop=True)
    # Clean fields
    df['title'] = df['title'].astype(str).str.strip()
    df['genres'] = df['genres'].fillna('').astype(str)
    # Normalize imdb to numeric
    if 'imdb' in df.columns:
        df['imdb'] = pd.to_numeric(df['imdb'], errors='coerce').fillna(df['imdb'].mean())
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
    if 'numVotes' in df.columns:
        df['numVotes'] = pd.to_numeric(df['numVotes'], errors='coerce').fillna(0).astype(int)
    if 'numVotes' in df.columns and 'year' in df.columns:
        df['popularity'] = df.groupby('year')['numVotes'].transform(
            lambda x: (x - x.mean()) / (x.std() + 1e-9)
        )
    return df

def search_movie(title_query, df, max_results=100):
    """Return a list of close matches for partial movie titles."""
    title_query = title_query.lower().strip()
    matches = df[df['title'].str.lower().str.contains(title_query, na=False)]
    return matches.head(max_results).reset_index(drop=True)


def select_movie_from_search(df):
    """Interactive helper for fuzzy title search + selection."""
    query = input("Enter (partial) movie title: ").strip()
    matches = search_movie(query, df)

    if matches.empty:
        print("No matches found.")
        return None

    print("\nPossible matches:")
    for i, row in matches.iterrows():
        print(f"{i+1}. {row['title']} ({int(row['year']) if 'year' in row and not pd.isna(row['year']) else 'Unknown'})")

    choice = input("Select number (0 to cancel): ").strip()
    if not choice.isdigit():
        return None
    choice = int(choice)
    if choice <= 0 or choice > len(matches):
        return None

    return matches.iloc[choice - 1]['title']



def parse_genres(df):
    # Genres come like "Action, Adventure" or "Drama" or ""
    lists = df['genres'].apply(lambda s: [g.strip() for g in s.split(',') if g.strip()]) 
    mlb = MultiLabelBinarizer(sparse_output=False)
    genre_mat = mlb.fit_transform(lists)
    genre_df = pd.DataFrame(genre_mat, columns=[f"genre__{g}" for g in mlb.classes_])
    return genre_df, mlb

def build_features(df, mlb=None, scaler=None, fit_scaler=True):
    # returns feature DataFrame and fitted scaler/mlb (if applicable)
    genre_df, mlb_fitted = parse_genres(df) if mlb is None else (pd.DataFrame(mlb.transform(df['genres'].apply(lambda s: [g.strip() for g in s.split(',') if g.strip()])) , columns=[f"genre__{g}" for g in mlb.classes_]), mlb)
    feats = pd.concat([df.reset_index(drop=True), genre_df.reset_index(drop=True)], axis=1)

    numeric_cols = []
    for col in ['imdb', 'year', 'numVotes', 'popularity']:
        if col in feats.columns:
            numeric_cols.append(col)

    scaler_fitted = scaler
    if fit_scaler:
        scaler_fitted = StandardScaler()
        if numeric_cols:
            feats[numeric_cols] = scaler_fitted.fit_transform(feats[numeric_cols])
    else:
        if scaler_fitted and numeric_cols:
            feats[numeric_cols] = scaler_fitted.transform(feats[numeric_cols])
    # drop raw genres column before returning features
    feats = feats.drop(columns=['genres'])
    return feats, mlb_fitted, scaler_fitted

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_ratings(ratings):
    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ratings, f, indent=2, ensure_ascii=False)

def train_model(features_df, ratings_dict, classifier='rf'):
    # Build training X,y from features_df using ratings_dict: title -> 0/1
    rated_rows = features_df[features_df['title'].isin(ratings_dict.keys())].copy()
    if rated_rows.empty:
        return None, None, None
    y = rated_rows['title'].map(ratings_dict).astype(int).values
    X = rated_rows.drop(columns=['title', 'numVotes'] if 'numVotes' in rated_rows.columns else ['title']).values
    # choice of classifier
    if classifier == 'rf':
        clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    else:
        clf = DecisionTreeClassifier(max_depth=6, random_state=42)
    clf.fit(X, y)
    return clf, X, y



import numpy as np

def recommend(df, clf, feats_df, ratings_dict, top_n=RECOMMEND_TOP_N):
    # Determine unwatched movies
    unwatched_mask = ~df['title'].isin(ratings_dict.keys())
    if not unwatched_mask.any():
        return []

    candidates = feats_df[unwatched_mask].copy()
    if candidates.empty:
        return []

    # Prepare feature matrix for candidates (drop non-feature cols)
    drop_cols = ['title']
    if 'numVotes' in candidates.columns:
        drop_cols.append('numVotes')
    X_cand = candidates.drop(columns=drop_cols).values

    # Get probability of "like" (class 1) robustly
    prob_like = None
    if hasattr(clf, 'predict_proba'):
        proba = clf.predict_proba(X_cand)  # shape (n_samples, n_classes)
        classes = getattr(clf, "classes_", None)

        if classes is None:
            # Fallback: if no classes_ attribute, use predict output
            preds = clf.predict(X_cand)
            prob_like = preds.astype(float)
        else:
            # If both classes are present, find column index of class 1
            if 1 in classes:
                idx1 = int(list(classes).index(1))
                # safe indexing
                if proba.shape[1] > idx1:
                    prob_like = proba[:, idx1]
                else:
                    # fallback - should not normally happen, but handle gracefully
                    prob_like = np.zeros(len(X_cand))
            else:
                # single-class (only 0 or only other label) case
                # If classifier was trained only on class 0 -> prob_like = 0
                # If trained only on class something else (e.g., only 1), handle accordingly
                single_class = classes[0]
                if single_class == 1:
                    prob_like = np.ones(len(X_cand))
                else:
                    prob_like = np.zeros(len(X_cand))
    else:
        # classifier doesn't support predict_proba -> fallback to predict
        preds = clf.predict(X_cand)
        prob_like = preds.astype(float)

    # Insert probabilities and sort
    candidates = candidates.reset_index(drop=True)
    candidates['prob_like'] = prob_like
    recs = candidates.sort_values('prob_like', ascending=False).head(top_n)

    out = []
    for _, row in recs.iterrows():
        title = row['title']
        # use original df to get the true values
        orig = df[df['title'] == title].iloc[0]
        out.append({
            'title': title,
            'prob_like': float(row['prob_like']),
            'imdb': round(float(orig['imdb']),2) if 'imdb' in orig else None,
            'year': int(orig['year']) if 'year' in orig else None
        })

    # print(feats_df.describe(include='all'))
    return out


def sample_for_rating(df, k=20):
    # return a small random sample of popular movies for user to rate
    # prefer higher numVotes and recent
    if 'numVotes' in df.columns:
        candidates = df.sort_values(['numVotes', 'imdb'], ascending=[False, False]).head(k*5)
        sample = candidates.sample(n=min(k, len(candidates)), random_state=42)
    else:
        sample = df.sample(n=min(k, len(df)), random_state=42)
    return sample.reset_index(drop=True)

def interactive_menu():
    df = load_movies()
    ratings = load_ratings()

    feats, mlb, scaler = build_features(df, mlb=None, scaler=None, fit_scaler=True)

    menu = dedent("""
    ===== IMDb CLI Recommender =====
    1) Show sample catalog (titles)
    2) Show a small sample to rate
    3) Rate a movie (like/dislike)
    4) Show my ratings
    5) Train & Recommend (RandomForest)
    6) Train & Recommend (DecisionTree)
    7) Export recommendations CSV (after training)
    8) Clear ratings
    9) Exit
    """).strip()

    last_recs = []

    while True:
        print("\n" + menu)
        choice = input("Choose option [1-9]: ").strip()
        if choice == '1':
            print("\nRandom movie titles (sampled):")
            # Shuffle the dataframe rows randomly each time
            shuffled = df.sample(frac=1, random_state=None).reset_index(drop=True)

            # Display first 100 (or fewer)
            for i, t in enumerate(shuffled['title'].head(100), 1):
                tagged = f" (rated: {ratings[t]})" if t in ratings else ''
                print(f"{i:2d}. {t}{tagged}")

        elif choice == '2':
            sample = sample_for_rating(df, k=20)
            print("\nSample to rate (enter exact title to rate from option 3):")
            for i, row in sample.iterrows():
                print(f"{i+1:2d}. {row['title']} — {row.get('imdb', 'N/A')} — {row.get('year', '')}")
        elif choice == '3':
            # title = input("Enter exact movie title to rate: ").strip()
            title = select_movie_from_search(df)
            if not title:
                print("Cancelled or not found.")
                continue
            if title not in df['title'].values:
                print("Title not found (try option 2 to view a sample). Exact match needed.")
                continue
            val = input("Like this movie? (y/n): ").strip().lower()
            if val not in ('y', 'n'):
                print("Use 'y' for like, 'n' for dislike.")
                continue
            ratings[title] = 1 if val == 'y' else 0
            save_ratings(ratings)
            print(f"Saved rating: {title} -> {ratings[title]}")
        elif choice == '4':
            if not ratings:
                print("No ratings yet. Use option 2 or 3 to rate some movies.")
            else:
                print("\nYour ratings:")
                for t, v in ratings.items():
                    print(f"- {t}: {'Liked' if v==1 else 'Disliked'}")
        elif choice in ('5', '6'):
            clf_type = 'rf' if choice == '5' else 'dt'
            # rebuild features with same mlb/scaler objects to avoid mismatch
            feats_df, _, _ = build_features(df, mlb=mlb, scaler=scaler, fit_scaler=False)
            clf, X, y = train_model(feats_df, ratings, classifier='rf' if clf_type == 'rf' else 'dt')
            if clf is None:
                print("No rated movies found. Rate at least a few (5-10) movies first.")
                continue
            recs = recommend(df, clf, feats_df, ratings, top_n=RECOMMEND_TOP_N)
            if not recs:
                print("No recommendations (maybe you rated all sample movies).")
            else:
                print(f"\nTop {len(recs)} recommendations (using {'RandomForest' if clf_type=='rf' else 'DecisionTree'}):")
                for i, r in enumerate(recs, 1):
                    print(f"{i}. {r['title']} — IMDb: {r['imdb']} — Year: {r['year']} — Prob_like: {r['prob_like']:.3f}")
                last_recs = recs
        elif choice == '7':
            if not last_recs:
                print("No cached recommendations. Run option 5 or 6 first.")
            else:
                out_df = pd.DataFrame(last_recs)
                out_df.to_csv("recommendations.csv", index=False)
                print("Wrote recommendations.csv")
        elif choice == '8':
            confirm = input("Clear saved ratings? [y/N]: ").strip().lower()
            if confirm == 'y':
                ratings = {}
                save_ratings(ratings)
                print("Ratings cleared.")
        elif choice == '9':
            print("Goodbye.")
            break
        else:
            print("Invalid option. Choose 1-9.")

if __name__ == "__main__":
    interactive_menu()
