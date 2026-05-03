import pandas as pd
import numpy as np

# =========================
# 1. PARAMÈTRES
# =========================

CSV_FILE = "ScoreEntry.csv"

CRITERIA_COLUMNS = [
    "Accuracy",
    "Coherence",
    "Impressiveness",
    "Originality",
    "Real_uses",
    "French",
    "Notes",
    "Distribution",
    "Prononciation",
    "Oral Presence",
    "Quality of the medium",
    "Time",
    "Interaction",
    "Questions"
]

NAME_COLUMN = "nom_equipe"
MIDDLE_SCHOOL_COLUMN = "Middle-schoolers"

# =========================
# 2. POIDS
# =========================

weights = {
    "Overall":                [1]*14,
    "Eureka prize":           [3,2,2,2,0,2,1,1,0,1,1,1,4,2],
    "Best experience":        [0,1,5,3,0,1,0,1,0,1,0,1,1,0],
    "Best theoretical":       [5,4,0,1,1,2,2,1,0,1,2,1,0,3],
    "MDL prize":              [1,1,3,4,1,1,1,1,2,2,3,1,1,1],
    "Best English":           [1,2,0,0,0,5,4,2,3,2,0,1,0,3],
    "Best experiment (Middle school)": [1,1,3,3,2,1,0,1,0,1,0,1,1,0],
    "Eureka prize (Middle School)":  [3,2,2,2,0,2,1,1,0,1,1,1,4,2],
}

CATEGORY_ORDER = [
    "Overall",
    "Eureka prize",
    "Best experience",
    "Best theoretical",
    "MDL prize",
    "Best English",
]

# =========================
# 3. LECTURE
# =========================

df = pd.read_csv(CSV_FILE)
df.columns = df.columns.str.strip()
df = df.replace({True: 1, False: 0})

df[CRITERIA_COLUMNS] = df[CRITERIA_COLUMNS] \
    .apply(pd.to_numeric, errors='coerce') \
    .fillna(0)

# =========================
# 4. PROMETHEE II
# =========================

def preference_function(d):
    return 1 if d > 0 else 0

def promethee_ranking(data, criteria, w):
    n = len(data)

    if n <= 1:
        return np.zeros(n)

    weights = np.array(w)
    weights = weights / weights.sum()

    phi_plus = np.zeros(n)
    phi_minus = np.zeros(n)

    values = data[criteria].values

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            preference_sum = 0

            for k in range(len(criteria)):
                d = values[i][k] - values[j][k]
                p = preference_function(d)
                preference_sum += weights[k] * p

            phi_plus[i] += preference_sum
            phi_minus[j] += preference_sum

    phi_plus /= (n - 1)
    phi_minus /= (n - 1)

    phi = phi_plus - phi_minus

    return phi

# =========================
# 5. CLASSEMENT PRINCIPAL
# =========================

already_awarded = set()
results = {}

for category in CATEGORY_ORDER:

    eligible_df = df[
        (~df[NAME_COLUMN].isin(already_awarded)) &
        (df[MIDDLE_SCHOOL_COLUMN] == 0)
    ].copy()

    if len(eligible_df) == 0:
        continue

    phi = promethee_ranking(eligible_df, CRITERIA_COLUMNS, weights[category])
    eligible_df["PROMETHEE_score"] = phi

    eligible_df = eligible_df.sort_values(by="PROMETHEE_score", ascending=False)

    top3 = eligible_df.head(3)

    equality = False
    if len(top3) >= 2:
        if np.isclose(top3.iloc[0]["PROMETHEE_score"],
                      top3.iloc[1]["PROMETHEE_score"]):
            equality = True

    results[category] = {
        "top3": top3[[NAME_COLUMN, "PROMETHEE_score"]],
        "equality": equality
    }

    if len(top3) > 0:
        already_awarded.add(top3.iloc[0][NAME_COLUMN])

# =========================
# 6. PODIUM COLLÉGIENS (TOP 5)
# =========================

middle_df = df[df[MIDDLE_SCHOOL_COLUMN] == 1].copy()

if len(middle_df) > 0:
    phi_middle = promethee_ranking(middle_df, CRITERIA_COLUMNS, weights["Overall"])
    middle_df["PROMETHEE_score"] = phi_middle
    middle_df = middle_df.sort_values(by="PROMETHEE_score", ascending=False)

    middle_top5 = middle_df.head(5)

    middle_equality = False
    if len(middle_top5) >= 2:
        if np.isclose(middle_top5.iloc[0]["PROMETHEE_score"],
                      middle_top5.iloc[1]["PROMETHEE_score"]):
            middle_equality = True
else:
    middle_top5 = pd.DataFrame()
    middle_equality = False

# =========================
# 6B. BEST EXPERIMENT COLLÉGIENS
# =========================

middle_exp_df = df[df[MIDDLE_SCHOOL_COLUMN] == 1].copy()

if len(middle_exp_df) > 0:
    phi_middle_exp = promethee_ranking(
        middle_exp_df,
        CRITERIA_COLUMNS,
        weights["Best experiment (Middle school)"]
    )

    middle_exp_df["PROMETHEE_score"] = phi_middle_exp
    middle_exp_df = middle_exp_df.sort_values(by="PROMETHEE_score", ascending=False)

    middle_exp_top3 = middle_exp_df.head(3)

    middle_exp_equality = False
    if len(middle_exp_top3) >= 2:
        if np.isclose(middle_exp_top3.iloc[0]["PROMETHEE_score"],
                      middle_exp_top3.iloc[1]["PROMETHEE_score"]):
            middle_exp_equality = True
else:
    middle_exp_top3 = pd.DataFrame()
    middle_exp_equality = False


# =========================
# 6C. EUREKA PRIZE COLLÉGIENS
# =========================

middle_eureka_df = df[df[MIDDLE_SCHOOL_COLUMN] == 1].copy()

if len(middle_eureka_df) > 0:
    phi_middle_eureka = promethee_ranking(
        middle_eureka_df,
        CRITERIA_COLUMNS,
        weights["Eureka prize (Middle School)"]
    )

    middle_eureka_df["PROMETHEE_score"] = phi_middle_eureka
    middle_eureka_df = middle_eureka_df.sort_values(by="PROMETHEE_score", ascending=False)

    middle_eureka_top3 = middle_eureka_df.head(3)

    middle_eureka_equality = False
    if len(middle_eureka_top3) >= 2:
        if np.isclose(middle_eureka_top3.iloc[0]["PROMETHEE_score"],
                      middle_eureka_top3.iloc[1]["PROMETHEE_score"]):
            middle_eureka_equality = True
else:
    middle_eureka_top3 = pd.DataFrame()
    middle_eureka_equality = False

# =========================
# 7. AFFICHAGE
# =========================

for category, data in results.items():
    print("\n==============================")
    print(f"🏆 {category}")
    print("==============================")
    print(data["top3"].to_string(index=False))
    if data["equality"]:
        print("⚠️ Égalité détectée pour la première place")

print("\n==============================")
print("🏆 Podium Collégiens (Top 5)")
print("==============================")

if not middle_top5.empty:
    print(middle_top5[[NAME_COLUMN, "PROMETHEE_score"]].to_string(index=False))
    if middle_equality:
        print("⚠️ Égalité détectée pour la première place")
else:
    print("Aucun collégien trouvé.")

print("\n==============================")
print("🏆 Eureka Prize (Collégiens)")
print("==============================")

if not middle_eureka_top3.empty:
    print(middle_eureka_top3[[NAME_COLUMN, "PROMETHEE_score"]].to_string(index=False))
    if middle_eureka_equality:
        print("⚠️ Égalité détectée pour la première place")
else:
    print("Aucun collégien trouvé.")
    
print("\n==============================")
print("🏆 Best Experiment (Collégiens)")
print("==============================")

if not middle_exp_top3.empty:
    print(middle_exp_top3[[NAME_COLUMN, "PROMETHEE_score"]].to_string(index=False))
    if middle_exp_equality:
        print("⚠️ Égalité détectée pour la première place")
else:
    print("Aucun collégien trouvé.")
