import pandas as pd
import json


def load_data():
    file = "patients_export.xlsx"

    patients = pd.read_excel(file, sheet_name="Patients")
    visits = pd.read_excel(file, sheet_name="Visits")
    actions = pd.read_excel(file, sheet_name="Visit Actions")
    calls = pd.read_excel(file, sheet_name="Call History")

    # standardize column names
    patients.columns = patients.columns.str.strip()
    visits.columns = visits.columns.str.strip()
    actions.columns = actions.columns.str.strip()
    calls.columns = calls.columns.str.strip()

    return patients, visits, actions, calls


def parse_clinical_summary(df):
    def extract_json(x):
        try:
            return json.loads(x) if isinstance(x, str) else {}
        except:
            return {}

    if "Clinical Summary" not in df.columns:
        df["risk"] = "Unknown"
        df["revenue"] = 0
        df["next_follow_up"] = None
        return df

    df["parsed"] = df["Clinical Summary"].apply(extract_json)

    df["risk"] = df["parsed"].apply(
        lambda x: x.get("risk_stratification", {}).get(
            "risk_category",
            "Unknown"
        )
    )

    df["revenue"] = df["parsed"].apply(
        lambda x: x.get("operational_snapshot", {})
        .get("revenue_potential", {})
        .get("total_indian_rupees", 0)
    )

    df["next_follow_up"] = df["parsed"].apply(
        lambda x: x.get("next_follow_up", {}).get(
            "scheduled_date",
            None
        )
    )

    return df