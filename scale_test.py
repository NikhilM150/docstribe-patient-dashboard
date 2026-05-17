import pandas as pd

file = "patients_export.xlsx"

# Load original sheets
patients = pd.read_excel(file, sheet_name="Patients")
visits = pd.read_excel(file, sheet_name="Visits")
actions = pd.read_excel(file, sheet_name="Visit Actions")
calls = pd.read_excel(file, sheet_name="Call History")

# Repeat data 50 times
patients_big = pd.concat([patients] * 50, ignore_index=True)
visits_big = pd.concat([visits] * 50, ignore_index=True)
actions_big = pd.concat([actions] * 50, ignore_index=True)
calls_big = pd.concat([calls] * 50, ignore_index=True)

# Save bigger file
with pd.ExcelWriter("patients_10000.xlsx", engine="openpyxl") as writer:
    patients_big.to_excel(writer, sheet_name="Patients", index=False)
    visits_big.to_excel(writer, sheet_name="Visits", index=False)
    actions_big.to_excel(writer, sheet_name="Visit Actions", index=False)
    calls_big.to_excel(writer, sheet_name="Call History", index=False)

print("Created patients_10000.xlsx successfully")