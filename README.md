# Lesson Plan Generator

A Flask app for preparing a lesson plan and exporting it to PDF and Word.

## Features
- Separate Training Aids and Teaching Aids inputs.
- Preserves repeated bibliography inputs from form through preview and both downloads.
- Hierarchical numbering for objectives, methodology/teaching aids, bibliography, and assessment questions.
- Optional centered logo above the document title.
- Flight-safety slogan in matching bordered, centered quotations at the top and after Home Assignment.
- Word downloads are converted from the generated PDF to keep their page layout consistent.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Logo files are converted in the browser to a data URL and limited to 1 MB. Do not upload sensitive images.
Word export uses PDF-to-DOCX layout conversion. This better matches the PDF than
rebuilding the document separately, but PDF conversion may not preserve every
layout detail identically in all Word versions.

## Build a Windows executable

On Windows, install Python and run `build_windows.bat` from the project folder.
The script installs the app and packaging dependencies, then creates
`dist\LessonPlanGenerator.exe`. Launch the executable to start the local app and
open it in your default browser at http://127.0.0.1:5000. Keep the console open
while using the app; closing it stops the local server. If port 5000 is already
in use, set the `LESSON_PLAN_PORT` environment variable before launching the
executable and use the corresponding port in the browser.
