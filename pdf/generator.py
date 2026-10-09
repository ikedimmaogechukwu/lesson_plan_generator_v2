# TOP = BOTTOM = 10 * mm

# def clean(text):
#     if text is None:
#         return ""
#     return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# def P(text, style):
#     return Paragraph(clean(text or " ").replace("\n", "<br/>"), style)

# def styles():
#     return {
#         "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=12, leading=14, alignment=TA_CENTER, spaceAfter=4),
#         "section": ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=7.8, leading=9),
#         "body": ParagraphStyle("body", fontName="Helvetica", fontSize=7, leading=8.4),
#         "small": ParagraphStyle("small", fontName="Helvetica", fontSize=6.5, leading=7.6),
#         "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=7, leading=8.2),
#         "slogan": ParagraphStyle("slogan", fontName="Helvetica-Bold", fontSize=8, leading=10, alignment=TA_CENTER),
#     }

# def table(rows, widths, style=None):
#     t = Table(rows, colWidths=widths, repeatRows=0)
#     base = [
#         ("GRID", (0,0), (-1,-1), .45, colors.black),
#         ("VALIGN", (0,0), (-1,-1), "TOP"),
#         ("LEFTPADDING", (0,0), (-1,-1), 3),
#         ("RIGHTPADDING", (0,0), (-1,-1), 3),
#         ("TOPPADDING", (0,0), (-1,-1), 2),
#         ("BOTTOMPADDING", (0,0), (-1,-1), 2),
#     ]
#     if style: base += style
#     t.setStyle(TableStyle(base))
#     return t

# def section(number, title, content, s):
#     return table([[P(f"{number}. {title}", s["section"])], [P(content, s["body"])]],
#                  [PAGE_W-LEFT-RIGHT])

# def timing_section(number, title, content, allotted, progress, s):
#     return table([
#         [P(f"{number}. {title}", s["section"]), "", ""],
#         [P("<b>Content</b>", s["label"]), P("<b>Time Allotted</b>", s["label"]), P("<b>Progress Time</b>", s["label"])],
#         [P(content, s["body"]), P(allotted, s["body"]), P(progress, s["body"])]
#     ], [112*mm, 33*mm, 33*mm], [("SPAN",(0,0),(-1,0))])

# def coverage_table(data, s):
#     rows = [
#         [P("<b>7. LESSON COVERAGE.</b>", s["section"]), "", "", ""],
#         [P(data["lesson_coverage"], s["body"]), "", "", ""],
#         [P("<b>Must Know</b>", s["label"]), P(data["must_know"], s["body"]), P(data["must_know_time"], s["body"]), P(data["must_know_progress"], s["body"])],
#         [P("<b>Should Know</b>", s["label"]), P(data["should_know"], s["body"]), P(data["should_know_time"], s["body"]), P(data["should_know_progress"], s["body"])],
#         [P("<b>Could Know</b>", s["label"]), P(data["could_know"], s["body"]), P(data["could_know_time"], s["body"]), P(data["could_know_progress"], s["body"])],
#     ]
#     return table(rows, [30*mm, 102*mm, 23*mm, 23*mm], [("SPAN",(0,0),(-1,0)), ("SPAN",(0,1),(-1,1))])

# def generate_lesson_plan_pdf(buffer, data):
#     s = styles()
#     doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=RIGHT, leftMargin=LEFT,
#                             topMargin=TOP, bottomMargin=BOTTOM, title="Lesson Plan",
#                             author=data.get("prepared_name",""))
#     story = [P("LESSON PLAN", s["title"])]
#     if data.get("flight_safety_slogan_enabled") and data.get("flight_safety_slogan"):
#         story += [table([[P("“" + data["flight_safety_slogan"] + "”", s["slogan"])]], [PAGE_W-LEFT-RIGHT]), Spacer(1,2)]

#     detail = [
#         [P("Unit",s["label"]),P(data["unit"],s["body"]),P("Faculty",s["label"]),P(data["faculty"],s["body"])],
#         [P("Branch",s["label"]),P(data["branch"],s["body"]),P("Course",s["label"]),P(data["course"],s["body"])],
#         [P("Syllabus",s["label"]),P(data["syllabus"],s["body"]),P("Subject",s["label"]),P(data["subject"],s["body"])],
#         [P("Duration",s["label"]),P(data["duration"],s["body"]),P("Date",s["label"]),P(data["date"],s["body"])],
#         [P("Lesson",s["label"]),P(data["lesson"],s["body"]),"",""]
#     ]
#     story += [table(detail,[22*mm,67*mm,22*mm,67*mm]), Spacer(1,2)]

#     train = data["training_objective"]
#     learning = "<br/>".join(f"{i}. {clean(o['verb'])+' ' if o['verb'] else ''}{clean(o['statement'])}" for i,o in enumerate(data["learning_objectives"],1) if o["statement"]) or " "
#     story += [table([
#         [P("<b>1. Objectives.</b>",s["body"]),""],
#         [P("<b>(a) TRAINING.</b>",s["body"]),P(f"{train['verb']} {train['statement']}",s["body"])],
#         [P("<b>(b) LEARNING.</b>",s["body"]),P(learning,s["small"])]
#     ], [38*mm, 140*mm], [("SPAN",(0,0),(1,0))]), Spacer(1,2)]

#     aids = ", ".join(data["training_aids"])
#     if data["other_training_aid"]: aids += (", " if aids else "") + data["other_training_aid"]
#     story += [section("2","Training Aids",aids,s), Spacer(1,2)]

#     refs = "<br/>".join(f"{i}. {clean(x)}" for i,x in enumerate(data["bibliography"],1) if x)
#     story += [section("3","Bibliography",refs,s), Spacer(1,2)]
#     story += [section("4","Previous Lesson Tie Up",data["previous_lesson_tie_up"],s), Spacer(1,2)]

#     methods = "<br/>".join(f"({i}) {clean(x)}" for i,x in enumerate(data["methodologies"],1))
#     if data["other_methodology"]: methods += f"<br/>Other: {clean(data['other_methodology'])}"
#     aids_list = "<br/>".join(f"({i}) {clean(x)}" for i,x in enumerate(data["training_aids"],1))
#     story += [table([[P("<b>5. METHODOLOGY.</b>",s["body"]),P("<b>TEACHING AIDS.</b>",s["body"])],
#                     [P(methods,s["small"]),P(aids_list,s["small"])]],[89*mm,89*mm]), Spacer(1,2)]

#     story += [timing_section("6","INTRODUCTION",data["introduction"],data["introduction_time"],data["introduction_progress"],s), Spacer(1,2)]
#     story += [coverage_table(data,s), Spacer(1,2)]
#     story += [timing_section("8","Summary and Conclusion",data["summary"],data["summary_time"],data["summary_progress"],s), Spacer(1,2)]

#     q1 = "<br/>".join(f"{i}. {clean(x)}" for i,x in enumerate(data["questions_to_class"].splitlines(),1) if x.strip())
#     story += [table([
#         [P("<b>9. Questions to the Class.</b>",s["body"]),P(q1,s["body"])],
#         [P("<b>10. Questions by the Class.</b>",s["body"]),P(data["questions_by_class"],s["body"])],
#         [P("<b>11. Home Assignment.</b>",s["body"]),P(data["home_assignment"],s["body"])]
#     ],[45*mm,133*mm]), Spacer(1,4)]
#     story += [table([[P("<b>12. Prepared by</b>",s["body"]),P("<b>Checked &amp; Approved by</b>",s["body"])],
#                      [P(f"<b>Name:</b> {clean(data['prepared_name'])}<br/><b>Rank:</b> {clean(data['prepared_rank'])}",s["body"]),""]],[89*mm,89*mm])]
#     story += [PageBreak(), P("13. Review:",s["section"])]
#     story += [table([[P("<b>Date</b>",s["body"]),P("<b>Instructor</b>",s["body"]),P("<b>Signature</b>",s["body"]),P("<b>Comments</b>",s["body"])],["","","",""],["","","",""]],[28*mm,45*mm,38*mm,67*mm])]
#     story += [Spacer(1,8), section("14","Remarks by Senior Instructor"," ",s), Spacer(1,8), section("15","Remarks by Head of Faculty/Chief Instructor"," ",s)]
#     doc.build(story)

"""PDF generation for the Lesson Plan.

All user text is escaped exactly once (inside ``P`` / ``html_lines``), section
boxes grow with their content (no fixed heights that make long text overlap),
and progressive time is always calculated from the allotted times.
"""
import os
import re
import base64
from io import BytesIO

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepInFrame,
    Image,
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Use an Arial-compatible font when available; Helvetica is the portable fallback.
try:
    FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "fonts")
    pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONT_DIR, "Arial-compatible.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONT_DIR, "Arial-compatible-Bold.ttf")))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial", boldItalic="Arial-Bold")
    FONT, FONT_BOLD = "Arial", "Arial-Bold"
except Exception:
    FONT, FONT_BOLD = "Helvetica", "Helvetica-Bold"

PAGE_W, PAGE_H = A4
LEFT = RIGHT = 15 * mm
TOP = BOTTOM = 12 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT
MAX_BLOCK_H = PAGE_H - TOP - BOTTOM - 25 * mm   # safety limit for one block

NUM_W = 17 * mm          # width of the "1." / "7.1." number column
TIME_W = 48 * mm         # width of the Time Allotted / Progressive Time box
TIME_GAP = 4 * mm

# Fields whose "Time Allotted" feeds the progressive-time calculation,
# in the order they appear in the document.
TIMED_FIELDS = [
    "introduction_time",
    "lesson_coverage_time",
    "summary_time",
    "questions_to_class_time",
    "questions_by_class_time",
    "home_assignment_time",
]


# ------------------------------------------------------------------ text ---
def clean(text):
    """Escape text for ReportLab's mini-HTML and normalise newlines."""
    if text is None:
        return ""
    return (
        str(text)
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def html_lines(text):
    """Escape text and turn newlines into <br/>. Returns ready-to-use markup."""
    return clean(text).replace("\n", "<br/>")


def numbered_html(items, prefix="", start=1):
    """'1. item' lines, escaped once, joined with <br/>. Returns markup."""
    return "<br/>".join(
        f"&nbsp;&nbsp;&nbsp;{prefix}{i}. {html_lines(item)}"
        for i, item in enumerate(items, start)
    )


def P(text, style, raw=False):
    """Paragraph. ``raw=True`` means text is already-escaped markup."""
    value = (text if raw else html_lines(text)) if text else " "
    return Paragraph(value or " ", style)


def styles():
    def ps(name, font, size, leading, **kw):
        return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading, **kw)

    return {
        "title": ps("title", "Helvetica-Bold", 12, 14, alignment=TA_CENTER, spaceAfter=5),
        "section": ps("section", FONT_BOLD, 12, 14, alignment=TA_LEFT),
        "body": ps("body", FONT, 12, 14),
        "body_bold": ps("body_bold", FONT_BOLD, 12, 14),
        "label": ps("label", FONT_BOLD, 12, 14),
        "slogan": ps("slogan", FONT_BOLD, 12, 14, alignment=TA_CENTER),
        "time": ps("time", FONT, 12, 14, alignment=TA_CENTER),
        "time_header": ps("time_header", FONT_BOLD, 12, 14, alignment=TA_CENTER),
    }


# ----------------------------------------------------------------- tables ---
def plain_style(extra=None, right_pad=0):
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), right_pad),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


def bordered_table(rows, widths, style=None, paddings=3, row_heights=None):
    cmds = [
        ("GRID", (0, 0), (-1, -1), 0.45, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), paddings),
        ("RIGHTPADDING", (0, 0), (-1, -1), paddings),
        ("TOPPADDING", (0, 0), (-1, -1), paddings),
        ("BOTTOMPADDING", (0, 0), (-1, -1), paddings),
    ]
    if style:
        cmds.extend(style)
    table = Table(rows, colWidths=widths, rowHeights=row_heights)
    table.setStyle(TableStyle(cmds))
    return table


def guard(flowable):
    """Shrink a block that is taller than a page instead of crashing."""
    return KeepInFrame(CONTENT_W, MAX_BLOCK_H, [flowable], mode="shrink")


def section_box(number, title, body, s, width=CONTENT_W, min_body_h=15 * mm,
                title_h=6.5 * mm, raw=False):
    """Number + title row, then a body row that is at least ``min_body_h`` tall
    and grows to fit the text. Returns (table, total_height)."""
    body_w = width - NUM_W
    para = P(body, s["body"], raw=raw)
    _, h = para.wrap(body_w, 10_000)
    body_h = max(min_body_h, h + 2 * mm)
    table = Table(
        [[P(number, s["section"]), P(title, s["body_bold"])], ["", para]],
        colWidths=[NUM_W, body_w],
        rowHeights=[title_h, body_h],
    )
    table.setStyle(plain_style())
    return table, title_h + body_h


def open_section(number, title, body, s, min_body_h=10 * mm, raw=False):
    table, _ = section_box(number, title, body, s, min_body_h=min_body_h, raw=raw)
    return guard(table)


def timing_header(s):
    return bordered_table(
        [[P("Time\nAllotted", s["time_header"]), P("Progressive\nTime", s["time_header"])]],
        [23 * mm, 25 * mm],
    )


def right_timing_header(s):
    table = Table([["", timing_header(s)]], colWidths=[CONTENT_W - TIME_W, TIME_W])
    table.setStyle(plain_style())
    return table


def timing_box(allotted, progress, height, s):
    # Fixed-size time cells: independent of the neighbouring content length.
    return bordered_table(
        [[P(allotted, s["time"]), P(progress, s["time"])]],
        [23 * mm, 25 * mm],
        paddings=4,
        row_heights=[18 * mm],
    )


def timed_section(number, title, body, allotted, progress, s,
                  min_body_h=25 * mm, raw=False):
    left_w = CONTENT_W - TIME_W - TIME_GAP
    left, height = section_box(number, title, body, s, width=left_w,
                               min_body_h=min_body_h, raw=raw)
    wrapper = Table(
        [[left, timing_box(allotted, progress, height, s)]],
        colWidths=[CONTENT_W - TIME_W, TIME_W],
    )
    wrapper.setStyle(plain_style())
    return guard(wrapper)


# ------------------------------------------------------------------ time ---
def parse_minutes(value):
    """Turn '5', '5 mins', '1 hour 30 min', '1.5 hours', '01:30' into minutes."""
    if value is None:
        return 0
    text = str(value).strip().lower()
    if not text:
        return 0

    m = re.fullmatch(r"(\d+):(\d{1,2})", text)          # hh:mm
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))

    total, matched = 0.0, False
    for num, unit in re.findall(
        r"(\d+(?:\.\d+)?)\s*(hours?|hrs?|h|minutes?|mins?|m)\b", text
    ):
        matched = True
        total += float(num) * (60 if unit.startswith("h") else 1)
    if matched:
        return int(round(total))

    m = re.search(r"\d+(?:\.\d+)?", text)               # bare number = minutes
    return int(round(float(m.group()))) if m else 0


def format_minutes(minutes):
    minutes = max(0, int(minutes or 0))
    if minutes >= 60:
        return f"{minutes // 60}:{minutes % 60:02d}"
    return str(minutes)


def calculate_progressive_times(data):
    """{'introduction_progress': '5', 'lesson_coverage_progress': '15', ...}"""
    progressive, total = {}, 0
    for field in TIMED_FIELDS:
        minutes = parse_minutes(data.get(field, ""))
        total += minutes
        progressive[field.replace("_time", "_progress")] = (
            format_minutes(total) if minutes else ""
        )
    return progressive


# ------------------------------------------------------ content builders ---
def training_objective_text(data):
    """'By the end of the lesson Cadet will be able to <objective>'.
    Also accepts the legacy dict form {'person','verb','statement'}."""
    training = data.get("training_objective", "")
    person = data.get("training_person", "")
    verb = ""
    if isinstance(training, dict):
        person = training.get("person", person)
        verb = training.get("verb", "")
        training = training.get("statement", "")
    statement = " ".join(x for x in (str(verb).strip(), str(training).strip()) if x)
    if not statement:
        return ""
    person = str(person).strip() or "Officer"
    return f"By the end of the lesson {person} will be able to {statement}"


def learning_objectives_markup(data):
    """Render the selected action verb in bold in the final PDF."""
    rows = []
    for o in data.get("learning_objectives", []):
        statement = (o.get("statement") or "").strip()
        if not statement:
            continue
        verb = (o.get("verb") or "").strip()
        prefix = f"<b>{clean(verb)}</b> " if verb else ""
        rows.append(prefix + html_lines(statement))
    return "<br/>".join(
        f"&nbsp;&nbsp;&nbsp;1.2.{i}. {item}" for i, item in enumerate(rows, 1)
    )


def with_other(items, other):
    items = [i for i in items if i and i.strip() and i.strip().lower() != "other"]
    if other and other.strip():
        items.append(other.strip())
    return items


# --------------------------------------------------------------- blocks ---
def details_block(data, s):
    def row(l1, k1, l2, k2):
        return [P(l1, s["label"]), P(data.get(k1), s["body"]),
                P(l2, s["label"]), P(data.get(k2), s["body"])]

    date = data.get("date_display") or data.get("date")
    rows = [
        row("Unit", "unit", "Faculty", "faculty"),
        row("Branch", "branch", "Course", "course"),
        row("Syllabus", "syllabus", "Subject", "subject"),
        [P("Duration", s["label"]), P(data.get("duration"), s["body"]),
         P("Date", s["label"]), P(date, s["body"])],
        [P("Lesson", s["label"]), P(data.get("lesson"), s["body"]), "", ""],
    ]
    return bordered_table(
        rows, [24 * mm, 61 * mm, 24 * mm, CONTENT_W - 109 * mm],
        style=[("SPAN", (1, 4), (3, 4))],
    )


def objectives_block(data, s):
    train_w = CONTENT_W - NUM_W
    training = P(training_objective_text(data), s["body"])
    learning = P(learning_objectives_markup(data), s["body"], raw=True)
    _, th = training.wrap(train_w, 10_000)
    _, lh = learning.wrap(train_w, 10_000)
    t_h = max(12 * mm, th + 2 * mm)
    l_h = max(24 * mm, lh + 2 * mm)
    table = Table(
        [
            [P("1.1.", s["section"]), P("Training.", s["body_bold"])],
            ["", training],
            [P("1.2.", s["section"]), P("Learning.", s["body_bold"])],
            ["", learning],
        ],
        colWidths=[NUM_W, train_w],
        rowHeights=[6.5 * mm, t_h, 6.5 * mm, l_h],
    )
    table.setStyle(plain_style())
    return guard(table)


def methodology_block(methods, aids, s):
    col_w = (CONTENT_W - NUM_W) / 2
    m_par = P(numbered_html(methods, "5."), s["body"], raw=True)
    a_par = P(numbered_html(aids, "5.", start=len(methods) + 1), s["body"], raw=True)
    h = max(m_par.wrap(col_w - 3, 10_000)[1], a_par.wrap(col_w - 3, 10_000)[1])
    table = Table(
        [
            [P("5.", s["section"]), P("Methodology.", s["body_bold"]),
             P("Teaching Aids.", s["body_bold"])],
            ["", m_par, a_par],
        ],
        colWidths=[NUM_W, col_w, col_w],
        rowHeights=[6.5 * mm, max(22 * mm, h + 2 * mm)],
    )
    table.setStyle(plain_style(right_pad=3))
    return guard(table)


def coverage_block(data, s, progress):
    """Section 7: one time box for the whole section, 7.1-7.3 below it."""
    heading = Table(
        [[P("7.", s["section"]), P("Lesson Coverage.", s["body_bold"])]],
        colWidths=[NUM_W, CONTENT_W - NUM_W],
    )
    heading.setStyle(plain_style())

    left_w = CONTENT_W - TIME_W - TIME_GAP
    body_w = left_w - NUM_W
    para = P(data.get("lesson_coverage", ""), s["body"])
    height = max(25 * mm, para.wrap(body_w, 10_000)[1] + 2 * mm)
    left = Table([["", para]], colWidths=[NUM_W, body_w], rowHeights=[height])
    left.setStyle(plain_style())
    main = Table(
        [[left, timing_box(data.get("lesson_coverage_time", ""),
                           progress.get("lesson_coverage_progress", ""), height, s)]],
        colWidths=[CONTENT_W - TIME_W, TIME_W],
    )
    main.setStyle(plain_style())

    blocks = [guard(heading), guard(main), Spacer(1, 3 * mm)]
    for number, title, key in [
        ("7.1.", "Must Know.", "must_know"),
        ("7.2.", "Should Know.", "should_know"),
        ("7.3.", "Could Know.", "could_know"),
    ]:
        blocks.append(open_section(number, title, data.get(key, ""), s,
                                   min_body_h=20 * mm))
        blocks.append(Spacer(1, 3 * mm))
    return blocks


def questions_block(data, s, progress):
    """Sections 9-11, each with its own allotted time + progressive time."""
    q_lines = [x.strip() for x in (data.get("questions_to_class") or "")
               .replace("\r", "").split("\n") if x.strip()]
    items = [
        ("9.", "Questions to the Class.", numbered_html(q_lines, "9."), True,
         "questions_to_class"),
        ("10.", "Questions by the Class.",
         numbered_html([x.strip() for x in (data.get("questions_by_class") or "").splitlines() if x.strip()], "10."), True,
         "questions_by_class"),
        ("11.", "Home Assignment.",
         numbered_html([x.strip() for x in (data.get("home_assignment") or "").splitlines() if x.strip()], "11."), True,
         "home_assignment"),
    ]
    blocks = []
    for number, title, body, raw, key in items:
        blocks.append(timed_section(
            number, title, body,
            data.get(f"{key}_time", ""), progress.get(f"{key}_progress", ""),
            s, min_body_h=20 * mm, raw=raw,
        ))
        blocks.append(Spacer(1, 3 * mm))
    return blocks


def signature_block(data, s):
    col_w = (CONTENT_W - NUM_W) / 3
    prepared = f"{html_lines(data.get('prepared_name'))}<br/>" \
               f"{html_lines(data.get('prepared_rank'))}"
    table = Table(
        [
            [P("12.", s["section"]), P("Prepared by", s["body_bold"]),
             P("Checked by", s["body_bold"]), P("Approved by", s["body_bold"])],
            ["", P(prepared, s["body"], raw=True), "", ""],
        ],
        colWidths=[NUM_W, col_w, col_w, col_w],
        rowHeights=[7 * mm, 24 * mm],
    )
    table.setStyle(plain_style(extra=[
        ("BOX", (1, 1), (1, 1), 0.45, colors.black),
        ("BOX", (2, 1), (2, 1), 0.45, colors.black),
        ("BOX", (3, 1), (3, 1), 0.45, colors.black),
        ("LEFTPADDING", (1, 1), (-1, 1), 3),
        ("TOPPADDING", (1, 1), (-1, 1), 3),
    ]))
    return table


# ------------------------------------------------------------------ main ---
def generate_lesson_plan_pdf(buffer, data):
    """Write the lesson plan PDF for ``data`` (see app.collect_form_data)."""
    progress = calculate_progressive_times(data)
    s = styles()

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=RIGHT, leftMargin=LEFT, topMargin=TOP, bottomMargin=BOTTOM,
        title="Lesson Plan", author=data.get("prepared_name", "") or "",
    )
    story = []

    # ---- Page 1: header and sections 1-5 --------------------------------
    logo_data = data.get("logo_data", "")
    if logo_data.startswith("data:image/") and "," in logo_data:
        try:
            raw_logo = base64.b64decode(logo_data.split(",", 1)[1])
            logo = Image(BytesIO(raw_logo), width=18 * mm, height=14 * mm, kind="proportional")
            logo.hAlign = "CENTER"
            story.append(logo)
            story.append(Spacer(1, 1 * mm))
        except Exception:
            pass
    story.append(P("LESSON PLAN", s["title"]))
    story.append(details_block(data, s))
    story.append(Spacer(1, 3 * mm))

    if data.get("flight_safety_slogan_enabled") and data.get("flight_safety_slogan"):
        story.append(bordered_table([[P("“" + data["flight_safety_slogan"] + "”", s["slogan"])]],
                                    [CONTENT_W], paddings=5))
        story.append(Spacer(1, 3 * mm))

    story.append(open_section("1.", "Objectives.", "", s, min_body_h=0))
    story.append(Spacer(1, 1 * mm))
    story.append(objectives_block(data, s))
    story.append(Spacer(1, 3 * mm))

    aids = with_other(list(data.get("training_aids", [])), data.get("other_training_aid"))
    methods = with_other(list(data.get("methodologies", [])), data.get("other_methodology"))
    bibliography = [x for x in data.get("bibliography", []) if x and x.strip()]

    story.append(open_section("2.", "Training Aids.", numbered_html(aids, "2."), s, raw=True))
    story.append(Spacer(1, 3 * mm))
    story.append(open_section("3.", "Bibliography.", numbered_html(bibliography, "3."), s,
                              min_body_h=14 * mm, raw=True))
    story.append(Spacer(1, 3 * mm))
    story.append(open_section("4.", "Previous Lesson Tie-up.",
                              data.get("previous_lesson_tie_up", ""), s,
                              min_body_h=16 * mm))
    story.append(Spacer(1, 3 * mm))
    teaching_aids = with_other(list(data.get("teaching_aids", [])), "") or aids
    story.append(methodology_block(methods, teaching_aids, s))

    # ---- Page 2: sections 6-7 -------------------------------------------
    story.append(PageBreak())
    story.append(right_timing_header(s))
    story.append(Spacer(1, 3 * mm))
    story.append(timed_section(
        "6.", "Introduction.", data.get("introduction", ""),
        data.get("introduction_time", ""), progress["introduction_progress"],
        s, min_body_h=35 * mm,
    ))
    story.append(Spacer(1, 3 * mm))
    story.extend(coverage_block(data, s, progress))

    # ---- Page 3: sections 8-12 ------------------------------------------
    story.append(PageBreak())
    story.append(right_timing_header(s))
    story.append(Spacer(1, 3 * mm))
    story.append(timed_section(
        "8.", "Summary and Conclusion.", data.get("summary", ""),
        data.get("summary_time", ""), progress["summary_progress"],
        s, min_body_h=28 * mm,
    ))
    story.append(Spacer(1, 3 * mm))
    story.extend(questions_block(data, s, progress))
    story.append(HRFlowable(width="100%", thickness=0.7, color=colors.black, spaceBefore=2 * mm, spaceAfter=3 * mm))
    if data.get("flight_safety_slogan_enabled") and data.get("flight_safety_slogan"):
        story.append(bordered_table(
            [[P("“" + data["flight_safety_slogan"] + "”", s["slogan"])]],
            [CONTENT_W], paddings=5,
        ))
        story.append(Spacer(1, 3 * mm))

    if data.get("flight_safety_instruction"):
        story.append(open_section("", "Flight Safety Instruction.",
                                  data["flight_safety_instruction"], s,
                                  min_body_h=10 * mm))
        story.append(Spacer(1, 3 * mm))

    story.append(signature_block(data, s))
    story.append(Spacer(1, 7 * mm))
    story.append(P("Countersigned by", s["body_bold"]))

    doc.build(story)
