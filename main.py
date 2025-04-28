import pandas as pd
import json
from datetime import datetime

# Load CSV
file_path = r"C:\Users\Maram\OneDrive - Saudi Ground Services\RegistrationStatusCSV.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()
 # for testing purposes, we are just testing things out
 # df.rows= df.rows.str.strip()


# Columns to keep
columns_to_keep = [
    "User ID", "First Name", "Last Name", "Middle Name", "Class ID",
    "Course ID", "Title", "Start Date/Time", "End Date/Time",
    "Venue", "Instructor First Name", "Instructor Last Name"
]
df = df[columns_to_keep]

# Clean timezone text
df["Start Date/Time"] = df["Start Date/Time"].str.replace(r' [A-Za-z]+/[A-Za-z]+$', '', regex=True)
df["End Date/Time"] = df["End Date/Time"].str.replace(r' [A-Za-z]+/[A-Za-z]+$', '', regex=True)

# Convert date
df["Start Date"] = pd.to_datetime(df["Start Date/Time"], format="%m/%d/%Y %H:%M:%S", errors='coerce').dt.date

# Clean NaNs
df = df.fillna("")

# Build final JSON
final_data = {}
initial_data{} # type: ignore #for testing data


for date, date_group in df.groupby("Start Date"):
    date_str = str(date)
    day_name = date.strftime("%A")

    final_data[date_str] = {
        "day": day_name,
        "classes": {}
    }
    
    for class_id, class_group in date_group.groupby("Class ID"):
        class_info = class_group.iloc[0]
        students = class_group[["User ID", "First Name", "Middle Name", "Last Name"]].to_dict(orient="records")
        
        final_data[date_str]["classes"][str(class_id)] = {
            "title": class_info["Title"],
            "start_time": class_info["Start Date/Time"],
            "end_time": class_info["End Date/Time"],
            "venue": class_info["Venue"],
            "instructor": f"{class_info['Instructor First Name']} {class_info['Instructor Last Name']}",
            "students": students,
            "student_count": len(students)
        }
        
# Save as JSON for for easier fetching and pushing
with open("attendance_data.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4)

print("✅ JSON is now successfully updated")