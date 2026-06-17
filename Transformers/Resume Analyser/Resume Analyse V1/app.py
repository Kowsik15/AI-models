from flask import Flask, render_template

app = Flask(__name__)

# -----------------------------
# Dummy Results (replace later)
# -----------------------------

def analyze_resume():

    result = {
        "score": 78.5,
        "recommendation": "Good Match",
        "matched_skills": [
            "Python",
            "SQL",
            "Tableau",
            "Machine Learning",
            "Pandas",
            "NumPy"
        ],
        "missing_skills": [
            "Power BI",
            "Statistics",
            "AWS"
        ]
    }

    return result


# -----------------------------
# Home Page
# -----------------------------

@app.route("/")
def home():

    result = analyze_resume()

    return render_template(
        "index.html",
        result=result
    )


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )