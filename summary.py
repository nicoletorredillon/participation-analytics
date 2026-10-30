import csv

input_file = "output/participation_clean.csv"

rows = []

with open(input_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        rows.append(row)

print("Rows loaded:", len(rows))

members = {}

for row in rows:
    commander = row["commander"]

    if commander not in members:
        members[commander] = []

    members[commander].append(row)

print("Members found:", len(members))

print("\nMEMBER TOTALS:")

for commander, observations in members.items():
    total_points = 0

    for observation in observations:
        total_points += int(observation["points"])

    print(commander, total_points)

print("\nBUILDING MEMBER SUMMARY:")

day_map = {
    "mon.csv": "Mon",
    "tue.csv": "Tue",
    "wed.csv": "Wed",
    "thur.csv": "Thu",
    "fri.csv": "Fri"
}

summary_rows = []

for commander, observations in members.items():

    daily_points = {
        "Mon": None,
        "Tue": None,
        "Wed": None,
        "Thu": None,
        "Fri": None
    }

    for observation in observations:
        day = day_map[observation["day"]]
        points = int(observation["points"])

        daily_points[day] = points

    observed_points = []

    for points in daily_points.values():
        if points is not None:
            observed_points.append(points)

    total_points = sum(observed_points)

    observed_days = len(observed_points)

    participating_days = 0
    zero_days = 0

    for points in observed_points:
        if points > 0:
            participating_days += 1

        if points == 0:
            zero_days += 1

    missing_days = 5 - observed_days

    if observed_days == 5 and total_points == 0:
        status = "No participation Mon-Fri"

    elif total_points > 0:
        status = "Participated"

    else:
        status = "Incomplete - review"

    summary_row = {
        "Commander": commander,
        "Mon": daily_points["Mon"],
        "Tue": daily_points["Tue"],
        "Wed": daily_points["Wed"],
        "Thu": daily_points["Thu"],
        "Fri": daily_points["Fri"],
        "TotalPoints": total_points,
        "ObservedDays": observed_days,
        "ParticipatingDays": participating_days,
        "ZeroDays": zero_days,
        "MissingDays": missing_days,
        "Status": status
    }

    summary_rows.append(summary_row)

print("Summary rows:", len(summary_rows))

print("\nSUMMARY CHECK:")

for row in summary_rows:
    if row["Commander"] in [
        "eunice outlaw",
        "ucrybabies",
        "chav e 5"
    ]:
        print(row)

print("\nEXPORTING MEMBER SUMMARY:")

output_file = "output/participation_summary.csv"

fieldnames = [
    "Commander",
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "TotalPoints",
    "ObservedDays",
    "ParticipatingDays",
    "ZeroDays",
    "MissingDays",
    "Status"
]

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for row in summary_rows:
        export_row = row.copy()

        for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            if export_row[day] is None:
                export_row[day] = ""

        writer.writerow(export_row)

print("Saved", len(summary_rows), "rows to", output_file)