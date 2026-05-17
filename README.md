# Docstribe Patient Intelligence Dashboard

## Objective
A healthcare analytics dashboard built to provide clinical, operational, and financial insights from patient data.

---

## Features
- Patient risk analytics
- Revenue opportunity tracking
- Pending task monitoring
- Call status analytics
- Natural Language Query Interface
- Scalable architecture for 10,000+ patients

---

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- JSON

---

## Project Structure
- app.py → Main dashboard
- utils.py → Data loading and preprocessing
- requirements.txt → Dependencies
- patients_export.xlsx → Dataset

---

## Setup Instructions

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run app
```bash
python -m streamlit run app.py
```

---

## Assumptions Made
- Input file is Excel
- Required sheets:
  - Patients
  - Visits
  - Visit Actions
  - Call History
- Clinical Summary contains valid JSON

---

## Known Limitations
- NLQ is rule-based
- Not connected to live database
- Limited to predefined query patterns

---

## Scalability
Tested successfully on:
- 200 patients
- 10,000+ patients