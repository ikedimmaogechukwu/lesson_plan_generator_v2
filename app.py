# from flask import Flask, render_template, request, send_file, redirect, url_for
# from io import BytesIO

# from pdf.generator import generate_lesson_plan_pdf

# app = Flask(__name__)

# VERBS = [
#     "Define", "Describe", "Identify", "List", "State", "Explain",
#     "Summarise", "Discuss", "Demonstrate", "Illustrate", "Apply",
#     "Calculate", "Use", "Execute", "Perform", "Compare", "Differentiate",
#     "Classify", "Analyse", "Examine", "Interpret", "Evaluate", "Assess",
#     "Justify", "Critique", "Recommend", "Design", "Develop"
# ]

# METHODOLOGIES = [
#     "Lecture", "Discussion", "Practical Demonstration", "Brain Storming",
#     "Question & Answer", "Group Discussion", "Case Study",
#     "Activity Based Learning", "Demonstration", "Other"
# ]

# TEACHING_AIDS = [
#     "Computer", "White Board", "Laser Pointer", "Power Point Presentation",
#     "Video", "Handout", "Model", "Chart", "Demonstration Equipment", "Other"
# ]

# def empty_data():
#     return {
#         "unit": "", "faculty": "", "branch": "", "course": "", "syllabus": "",
#         "subject": "", "duration": "", "lesson": "", "date": "",
#         "training_objective": {"verb": "", "statement": ""},
#         "learning_objectives": [{"verb": "", "statement": ""} for _ in range(10)],
#         "training_aids": [], "other_training_aid": "",
#         "bibliography": ["" for _ in range(5)],
#         "previous_lesson_tie_up": "",
#         "methodologies": [], "other_methodology": "",
#         "flight_safety_slogan_enabled": False,
#         "flight_safety_slogan": "",
#         "introduction": "", "introduction_time": "", "introduction_progress": "",
#         "lesson_coverage": "",
#         "must_know": "", "must_know_time": "", "must_know_progress": "",
#         "should_know": "", "should_know_time": "", "should_know_progress": "",
#         "could_know": "", "could_know_time": "", "could_know_progress": "",
#         "summary": "", "summary_time": "", "summary_progress": "",
#         "questions_to_class": "", "questions_by_class": "",
#         "home_assignment": "", "prepared_name": "", "prepared_rank": ""
#     }

# def collect_form_data(form):
#     objectives = []
#     for i in range(1, 11):
#         verb = form.get(f"objective_verb_{i}", "").strip()
#         statement = form.get(f"objective_{i}", "").strip()
#         objectives.append({"verb": verb, "statement": statement})

#     bibliography = [x.strip() for x in form.getlist("bibliography")]
#     bibliography += [""] * (5 - len(bibliography))
#     bibliography = bibliography[:5]

#     data = empty_data()
#     data.update({
#         "unit": form.get("unit", "").strip(),
#         "faculty": form.get("faculty", "").strip(),
#         "branch": form.get("branch", "").strip(),
#         "course": form.get("course", "").strip(),
#         "syllabus": form.get("syllabus", "").strip(),
#         "subject": form.get("subject", "").strip(),
#         "duration": form.get("duration", "").strip(),
#         "lesson": form.get("lesson", "").strip(),
#         "date": form.get("date", "").strip(),
#         "training_objective": {
#             "verb": form.get("training_verb", "").strip(),
#             "statement": form.get("training_objective", "").strip()
#         },
#         "learning_objectives": objectives,
#         "training_aids": form.getlist("training_aids"),
#         "other_training_aid": form.get("other_training_aid", "").strip(),
#         "bibliography": bibliography,
#         "previous_lesson_tie_up": form.get("previous_lesson_tie_up", "").strip(),
#         "methodologies": form.getlist("methodologies"),
#         "other_methodology": form.get("other_methodology", "").strip(),
#         "flight_safety_slogan_enabled": form.get("flight_safety_slogan_enabled") == "on",
#         "flight_safety_slogan": form.get("flight_safety_slogan", "").strip(),
#         "introduction": form.get("introduction", "").strip(),
#         "introduction_time": form.get("introduction_time", "").strip(),
#         "introduction_progress": form.get("introduction_progress", "").strip(),
#         "lesson_coverage": form.get("lesson_coverage", "").strip(),
#         "must_know": form.get("must_know", "").strip(),
#         "must_know_time": form.get("must_know_time", "").strip(),
#         "must_know_progress": form.get("must_know_progress", "").strip(),
#         "should_know": form.get("should_know", "").strip(),
#         "should_know_time": form.get("should_know_time", "").strip(),
#         "should_know_progress": form.get("should_know_progress", "").strip(),
#         "could_know": form.get("could_know", "").strip(),
#         "could_know_time": form.get("could_know_time", "").strip(),
#         "could_know_progress": form.get("could_know_progress", "").strip(),
#         "summary": form.get("summary", "").strip(),
#         "summary_time": form.get("summary_time", "").strip(),
#         "summary_progress": form.get("summary_progress", "").strip(),
#         "questions_to_class": form.get("questions_to_class", "").strip(),
#         "questions_by_class": form.get("questions_by_class", "").strip(),
#         "home_assignment": form.get("home_assignment", "").strip(),
#         "prepared_name": form.get("prepared_name", "").strip(),
#         "prepared_rank": form.get("prepared_rank", "").strip(),
#     })
#     return data

# def form_kwargs(data):
#     return dict(
#         data=data, verbs=VERBS, methodologies=METHODOLOGIES,
#         teaching_aids=TEACHING_AIDS
#     )

# @app.get("/")
# def landing():
#     return render_template("landing.html")

# @app.route("/create", methods=["GET", "POST"])
# def index():
#     data = collect_form_data(request.form) if request.method == "POST" else empty_data()
#     return render_template("index.html", **form_kwargs(data))

# @app.post("/preview")
# def preview():
#     data = collect_form_data(request.form)
#     return render_template("preview.html", data=data)

# @app.post("/edit")
# def edit():
#     # POST is intentional: it preserves every repeated field and checkbox.
#     data = collect_form_data(request.form)
#     return render_template("index.html", **form_kwargs(data))

# @app.post("/download")
# def download():
#     data = collect_form_data(request.form)
#     pdf_buffer = BytesIO()
#     generate_lesson_plan_pdf(pdf_buffer, data)
#     pdf_buffer.seek(0)

#     topic = data.get("lesson") or data.get("subject") or "Lesson_Plan"
#     safe_topic = "".join(
#         c if c.isalnum() or c in (" ", "-", "_") else "_"
#         for c in topic
#     ).strip().replace(" ", "_")

#     return send_file(
#         pdf_buffer,
#         mimetype="application/pdf",
#         as_attachment=True,
#         download_name=f"Lesson_Plan_{safe_topic or 'Lesson'}.pdf"
#     )

# if __name__ == "__main__":
#     app.run(debug=True)

from datetime import datetime
from io import BytesIO

from flask import Flask, render_template, request, send_file

from docx_generator import generate_lesson_plan_docx

from pdf.generator import (
    calculate_progressive_times,
    generate_lesson_plan_pdf,
    training_objective_text,
)

app = Flask(__name__)

VERBS = [
    "Define", "Describe", "Identify", "List", "State", "Explain",
    "Summarise", "Discuss", "Demonstrate", "Illustrate", "Apply",
    "Calculate", "Use", "Execute", "Perform", "Compare", "Differentiate",
    "Classify", "Analyse", "Examine", "Interpret", "Evaluate", "Assess",
    "Justify", "Critique", "Recommend", "Design", "Develop",
]

# "Other" is handled by the separate "Other ..." text boxes on the form.
METHODOLOGIES = [
    "Lecture", "Discussion", "Practical Demonstration", "Brain Storming",
    "Question & Answer", "Group Discussion", "Case Study",
    "Activity Based Learning", "Demonstration",
]

TEACHING_AIDS = [
    "Computer", "White Board", "Laser Pointer", "Power Point Presentation",
    "Video", "Handout", "Model", "Chart", "Demonstration Equipment",
]

TRAINING_PERSONS = ["Officer", "Cadet", "Student", "Warrant Officer", "Trainee"]

NUM_LEARNING_OBJECTIVES = 10
MIN_BIBLIOGRAPHY_ROWS = 5
MAX_BIBLIOGRAPHY_ROWS = 15

# Plain single-value text fields (everything except lists / checkboxes).
TEXT_FIELDS = [
    "unit", "faculty", "branch", "course", "syllabus", "subject", "duration",
    "lesson", "date", "training_objective", "training_aids", "teaching_aids", "other_training_aid",
    "previous_lesson_tie_up", "other_methodology", "flight_safety_slogan",
    "flight_safety_instruction",
    "introduction", "introduction_time",
    "lesson_coverage", "lesson_coverage_time",
    "must_know", "should_know", "could_know",
    "summary", "summary_time",
    "questions_to_class", "questions_to_class_time",
    "questions_by_class", "questions_by_class_time",
    "home_assignment", "home_assignment_time",
    "prepared_name", "prepared_rank",
]


def empty_data():
    data = {field: "" for field in TEXT_FIELDS}
    data.update({
        "training_person": TRAINING_PERSONS[0],
        "learning_objectives": [
            {"verb": "", "statement": ""} for _ in range(NUM_LEARNING_OBJECTIVES)
        ],
        "training_aids": [],
        "teaching_aids": [],
        "logo_data": "",
        "methodologies": [],
        "bibliography": [],
        "flight_safety_slogan_enabled": False,
    })
    data.update(derived_fields(data))
    return data


def clean_list(values, allowed=None):
    """Strip entries, drop blanks and the literal 'Other', optionally whitelist."""
    out = []
    for v in values:
        v = v.strip()
        if not v or v.lower() == "other":
            continue
        if allowed is not None and v not in allowed:
            continue
        out.append(v)
    return out


def derived_fields(data):
    """Values calculated from the form: progressive time, display date, etc."""
    date_display = data.get("date", "")
    try:
        date_display = datetime.strptime(date_display, "%Y-%m-%d").strftime("%d-%m-%Y")
    except ValueError:
        pass
    derived = {
        "date_display": date_display,
        "training_text": training_objective_text(data),
    }
    derived.update(calculate_progressive_times(data))
    return derived


def split_entries(value):
    """Split free-text aid/methodology fields by commas or newlines."""
    if isinstance(value, list):
        value = "\n".join(value)
    return [part.strip() for line in str(value or "").splitlines() for part in line.split(",") if part.strip()]


def collect_form_data(form):
    """Turn the submitted form into one clean dict used by form, preview, PDF."""
    data = empty_data()

    for field in TEXT_FIELDS:
        data[field] = form.get(field, "").strip()

    person = form.get("training_person", "").strip()
    data["training_person"] = person if person in TRAINING_PERSONS else TRAINING_PERSONS[0]

    data["learning_objectives"] = [
        {
            "verb": form.get(f"objective_verb_{i}", "").strip(),
            "statement": form.get(f"objective_{i}", "").strip(),
        }
        for i in range(1, NUM_LEARNING_OBJECTIVES + 1)
    ]

    data["training_aids"] = split_entries(form.get("training_aids", ""))
    data["teaching_aids"] = split_entries(form.get("teaching_aids", ""))
    data["logo_data"] = form.get("logo_data", "").strip()
    data["methodologies"] = split_entries(form.get("methodologies", ""))
    data["bibliography"] = clean_list(form.getlist("bibliography"))[:MAX_BIBLIOGRAPHY_ROWS]
    data["flight_safety_slogan_enabled"] = form.get("flight_safety_slogan_enabled") == "on"

    data.update(derived_fields(data))
    return data


def form_kwargs(data, error=None):
    rows = max(MIN_BIBLIOGRAPHY_ROWS, len(data["bibliography"]))
    bibliography = data["bibliography"] + [""] * (rows - len(data["bibliography"]))
    return dict(
        data=data,
        verbs=VERBS,
        methodologies=METHODOLOGIES,
        teaching_aids=TEACHING_AIDS,
        training_persons=TRAINING_PERSONS,
        bibliography_rows=bibliography,
        max_bibliography=MAX_BIBLIOGRAPHY_ROWS,
        error=error,
    )


def has_learning_objective(data):
    return any(o["statement"] for o in data["learning_objectives"])


# ----------------------------------------------------------------- routes ---
@app.get("/")
def landing():
    return render_template("landing.html")


@app.route("/create", methods=["GET", "POST"])
def index():
    data = collect_form_data(request.form) if request.method == "POST" else empty_data()
    return render_template("index.html", **form_kwargs(data))


@app.post("/preview")
def preview():
    data = collect_form_data(request.form)
    if not has_learning_objective(data):   # server-side check (JS can be bypassed)
        return render_template(
            "index.html",
            **form_kwargs(data, error="Please enter at least one learning objective."),
        )
    return render_template("preview.html", data=data)


@app.post("/edit")
def edit():
    # POST (not GET) so every repeated field and checkbox is preserved.
    return render_template("index.html", **form_kwargs(collect_form_data(request.form)))


@app.post("/download")
def download():
    data = collect_form_data(request.form)

    pdf_buffer = BytesIO()
    generate_lesson_plan_pdf(pdf_buffer, data)
    pdf_buffer.seek(0)

    topic = data["lesson"] or data["subject"] or "Lesson_Plan"
    safe_topic = "".join(
        c if c.isalnum() or c in (" ", "-", "_") else "_" for c in topic
    ).strip().replace(" ", "_")

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"Lesson_Plan_{safe_topic or 'Lesson'}.pdf",
    )


@app.post("/download-word")
def download_word():
    data = collect_form_data(request.form)
    word_buffer = BytesIO()
    generate_lesson_plan_docx(word_buffer, data)
    word_buffer.seek(0)
    topic = data["lesson"] or data["subject"] or "Lesson_Plan"
    safe_topic = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in topic).strip().replace(" ", "_")
    return send_file(word_buffer, mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document", as_attachment=True, download_name=f"Lesson_Plan_{safe_topic or 'Lesson'}.docx")


if __name__ == "__main__":
    app.run()