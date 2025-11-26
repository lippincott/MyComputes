# MyComputes

MyComputes is a Django-based prototype for AI-assisted review of alcohol product labels.

It lets you upload front/back label images, have an AI model read the label, and then compare the AI-extracted data against user-entered data side-by-side. The goal is to make it fast and auditable to verify label details like brand, product name, type, ABV, and volume.

---

## Features

- **Label uploads**
  - Upload front (and optionally back) images of alcohol product labels.
- **AI-powered extraction**
  - Sends label images to an AI model and returns a normalized JSON payload with:
    - Brand  
    - Product name  
    - Product type (e.g., “Beer - IPA”, “Wine - Merlot”, “Whiskey”)  
    - ABV (%)  
    - Volume (mL / fl oz, including liter → mL conversions)  
    - Presence and text of warning labels  
- **Side-by-side comparison**
  - Stores both **user-entered** and **AI-extracted** values.
  - Renders a clean UI where humans can visually compare values and confirm/correct them.
- **Match scoring & notes**
  - Utility functions compute match scores (e.g., string similarity, numeric tolerance) between user and AI fields.
  - Designed to support future “pass/fail” or “needs review” workflows.
- **PostgreSQL-backed Django app**
  - Uses Postgres as the primary datastore.
- **Bootstrap-based UI**
  - Uses Bootstrap 5 and project-specific CSS/JS for a clean, responsive interface.

---

## Architecture & Approach

### High-level design

The project is structured as a standard Django project:

- `myTTB/` – Django project configuration:
  - `settings.py`, `urls.py`, `wsgi.py`, etc.
- `reporter/` – Core application:
  - `models.py` – `Report` model (user vs. AI data, images, metadata).
  - `views.py` – List/detail/create views for reports.
  - `forms.py` – Forms for capturing user input and file uploads.
  - `utils/ai_extraction.py` – Integration with the AI model to extract fields from images.
  - `utils/report_matching.py` – Logic to compute match scores between user and AI values.
  - `templates/reporter/` – Templates for list, detail, and form pages.
- `static/` – CSS/JS/Images (including admin assets and custom UI).
- `templates/` – Base templates (`base.html`, `index.html`, etc.).

### Data model & separation of concerns

The core concept is a **Report**, representing a single product label review. Each report keeps:

- **User-entered fields**  
  These are the authoritative human inputs:
  - `brand`
  - `product_name`
  - `product_type`
  - `abv`
  - `milliliters`
  - `fl_oz`
  - `warning_label`
  - `warning_text`
  - Product images (front/back)

- **AI-extracted fields**  
  Parallel fields populated from the AI model:
  - `ai_brand`
  - `ai_product_name`
  - `ai_product_type`
  - `ai_abv`
  - `ai_milliliters`
  - `ai_fl_oz`
  - `ai_warning_label`
  - `ai_warning_text`
  - `ai_payload` – full raw JSON payload from the AI call (for auditing/debugging).

This **strict separation** between user and AI data makes it easy to:

- Show clear differences between what the label “should” say vs. what the AI thinks it says.
- Audit AI performance over time.
- Avoid overwriting human-entered values automatically.

### AI extraction flow

The extraction logic lives in `reporter/utils/ai_extraction.py`:

1. **Input images**  
   The function receives filesystem paths or file objects for:
   - `front_image`
   - `back_image` (optional)

2. **Prompt construction**  
   It sends a natural language instruction to the AI model explaining that:
   - The images contain alcohol product labels.
   - The model must return **only** a JSON object with a fixed set of keys (e.g., `ai_brand`, `ai_abv`, etc.).
   - Values should be normalized:
     - ABV as an integer (e.g., `13` for 13%).
     - Volume as integer mL (with conversion from liters if needed).
     - Optional fields as `null` if unknown.

3. **AI call & JSON parsing**  
   The helper:
   - Calls the OpenAI (or compatible) API with images + prompt.
   - Parses the model response to JSON.
   - Returns a Python dictionary with the expected keys.

4. **Model update**  
   The view or service layer:
   - Stores the full JSON in `ai_payload`.
   - Maps fields into individual `ai_*` columns on the `Report` model.
   - Saves the report.

### Match scoring & review

`reporter/utils/report_matching.py` handles comparison logic between user and AI values:

- For each relevant field:
  - Computes a **match score** (e.g., 0–100).
  - Handles numeric tolerance (e.g., ABV differences within a small range).
  - Handles string normalization (case, whitespace, simple punctuation).
- Results are attached to the `Report` and displayed in templates so reviewers can quickly see:
  - Which fields match confidently.
  - Which fields need manual attention.

This approach keeps **business rules** (matching logic, thresholds) centralized and easy to refine over time.

---

## Tech Stack

- **Language:** Python 3.x (see `requirements.txt` for specifics)
- **Framework:** Django (4.x)
- **Database:** PostgreSQL
- **Frontend:**
  - HTML templates with Bootstrap 5
  - Custom CSS/JS under `static/MASTER`
- **AI Integration:** OpenAI-compatible API for image+text (vision) models

### Assumptions
+ You have python, pip, django, pillow, and OpenAI packages installed. 
---

## Getting Started (Local Development)

### 1. Prerequisites

You’ll need:

- Python 3.10+  
- Git  
- PostgreSQL 13+  
- A working OpenAI (or compatible) API key

On Ubuntu, a rough setup might look like:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git postgresql postgresql-contrib

### 2. Clone the Repo
```
git clone git@github.com:lippincott/MyComputes.git
cd MyComputes
```

### 3. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate

```

### 4. Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt

pip install Pillow OpenAI
```

Keep in mind you will need to update all environment variables with your own Django Secret KEY and OpenAI API Key. 


### 5. Database Note
This uses postgres, but for simplicity use the default sqllite deployment. You will also need to update the settings.


### 6. Deploy Migrations
```
python manage.py migrate
python manage.py makemigrations
```


### 7. Test on Server
```
python manage.py runserver
```

By default, the site will be available at:

http://127.0.0.1:8000/

## Running Tests
If/when tests are added, you can run them with:
```
python manage.py test

```

## Test Images
There are sample images available for testing!

## Liceense

If you want, I can tweak this to exactly match your `urls.py` (e.g., whatever the landing path for the reporter UI is) or add a short “Quick Demo Flow” section once you settle on the main user flow.
::contentReference[oaicite:0]{index=0}

