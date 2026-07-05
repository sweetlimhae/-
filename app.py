from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

SAMPLE_GAMES = [
    {
        "sport": "soccer",
        "league": "EPL",
        "home": "Manchester City",
        "away": "Chelsea",
        "start_in_minutes": 55,
        "pick": "Manchester City 승",
        "odds": 1.72,
        "score": 88,
        "reason": ["Pinnacle 홈승 하락", "BMBets 시장 평균 대비 괴리", "홈 마핸 흐름 양호"]
    },
    {
        "sport": "soccer",
        "league": "LaLiga",
        "home": "Real Madrid",
        "away": "Valencia",
        "start_in_minutes": 35,
        "pick": "Real Madrid 승",
        "odds": 1.65,
        "score": 84,
        "reason": ["초기배당 대비 하락", "무승부 배당 상승", "Sharp 흐름"]
    },
    {
        "sport": "baseball",
        "league": "KBO",
        "home": "LG",
        "away": "Doosan",
        "start_in_minutes": 58,
        "pick": "LG 승",
        "odds": 1.78,
        "score": 82,
        "reason": ["Pinnacle 홈승 하락", "국내 배당 유지", "마핸 동반 하락"]
    },
    {
        "sport": "baseball",
        "league": "MLB",
        "home": "Dodgers",
        "away": "Padres",
        "start_in_minutes": 28,
        "pick": "Dodgers 승",
        "odds": 1.91,
        "score": 76,
        "reason": ["배당 하락", "시장 평균보다 낮은 sharp odds", "수익성 후보"]
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze")
def analyze():
    sport = request.args.get("sport", "all")
    window = int(request.args.get("window", 60))

    games = [
        g for g in SAMPLE_GAMES
        if g["start_in_minutes"] <= window and (sport == "all" or g["sport"] == sport)
    ]

    sorted_games = sorted(games, key=lambda x: x["score"], reverse=True)

    conservative = sorted_games[:2]
    balanced = sorted(sorted_games, key=lambda x: (x["score"] * x["odds"]), reverse=True)[:2]
    aggressive = sorted(sorted_games, key=lambda x: x["odds"], reverse=True)[:2]

    return jsonify({
        "games": games,
        "recommendations": {
            "신중형": conservative,
            "균형형": balanced,
            "공격형": aggressive
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
