from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__)


# ---------------------------------
# YOUR FUNCTIONS
# ---------------------------------

SKILLS = [
    "python",
    "sql",
    "tableau",
    "power bi",
    "excel",
    "machine learning",
    "deep learning",
    "tensorflow",
    "keras",
    "pandas",
    "numpy",
    "scikit-learn",
    "nlp",
    "rag",
    "transformers",
    "aws",
    "azure",
    "docker",
    "git",
    "flask"
]


def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        if skill in text:

            found.append(skill)

    return found


def recruiter_feedback(score):

    if score >= 85:
        return "Excellent Match"

    elif score >= 70:
        return "Good Match"

    elif score >= 50:
        return "Moderate Match"

    else:
        return "Low Match"


# TEMPORARY SCORE FUNCTION
# Replace with your transformer score

def calculate_similarity(resume_text, jd_text):

    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        jd_text
    )

    if len(jd_skills) == 0:
        return 0

    score = (
        len(
            set(resume_skills)
            .intersection(jd_skills)
        )
        /
        len(jd_skills)
    ) * 100

    return round(score,2)


# ---------------------------------
# HOME
# ---------------------------------

@app.route("/", methods=["GET","POST"])

def home():

    result = None

    if request.method == "POST":

        uploaded_file = request.files[
            "resume_file"
        ]

        jd_text = request.form[
            "jd_text"
        ]

        resume_text = ""

        with pdfplumber.open(
            uploaded_file
        ) as pdf:

            for page in pdf.pages:

                page_text = (
                    page.extract_text()
                )

                if page_text:

                    resume_text += (
                        page_text + "\n"
                    )

        resume_skills = extract_skills(
            resume_text
        )

        jd_skills = extract_skills(
            jd_text
        )

        score = calculate_similarity(
            resume_text,
            jd_text
        )

        matched_skills = list(
            set(resume_skills)
            .intersection(jd_skills)
        )

        missing_skills = list(
            set(jd_skills)
            .difference(resume_skills)
        )

        result = {

            "score": score,

            "recommendation":
                recruiter_feedback(score),

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills,

            "filename":
                uploaded_file.filename
        }

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":

    app.run(
        debug=False,
        use_reloader=False
    )