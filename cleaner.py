import csv
from difflib import SequenceMatcher

files = ["mon.csv", "tue.csv", "wed.csv", "thur.csv", "fri.csv"]
all_rows = []

for filename in files:
    file_path = f"output/{filename}"

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            all_rows.append({
                "day": filename,
                "commander": row["commander"],
                "points": int(row["points"])
            })

print("Total observations:", len(all_rows))
print("First row:", all_rows[0])

names = []

for row in all_rows:
    if row["commander"] not in names:
        names.append(row["commander"])

print("Unique OCR names:", len(names))
normalized_names = []

for name in names:
    normalized = name.lower().strip()

    if normalized not in normalized_names:
        normalized_names.append(normalized)

print("Unique normalized names:", len(normalized_names))

name_counts = {}

for row in all_rows:
    normalized = row["commander"].lower().strip()

    if normalized not in name_counts:
        name_counts[normalized] = 0

    name_counts[normalized] += 1

for name, count in name_counts.items():
    if count >= 4:
        print(name, count)

for row in all_rows:
    normalized = row["commander"].lower().strip()

    if normalized == "jambah" or normalized == "brittstndsonbiznezz":
        print(row["day"], row["commander"], row["points"])
deduped_rows = {}

for row in all_rows:
    normalized = row["commander"].lower().strip()
    key = (row["day"], normalized)

    if key not in deduped_rows:
        deduped_rows[key] = row

    if row["points"] > deduped_rows[key]["points"]:
        deduped_rows[key] = row

clean_rows = list(deduped_rows.values())

print("After same-day dedupe:", len(clean_rows))
print("Duplicates removed:", len(all_rows) - len(clean_rows))

clean_names = []

for row in clean_rows:
    normalized = row["commander"].lower().strip()

    if normalized not in clean_names:
        clean_names.append(normalized)

name_days = {}

for row in clean_rows:
    normalized = row["commander"].lower().strip()

    if normalized not in name_days:
        name_days[normalized] = []

    if row["day"] not in name_days[normalized]:
        name_days[normalized].append(row["day"])

print("\nHIGH-SIMILARITY MATCHES:")

for i in range(len(clean_names)):
    for j in range(i + 1, len(clean_names)):
        name1 = clean_names[i]
        name2 = clean_names[j]

        score = SequenceMatcher(None, name1, name2).ratio()

        if score >= 0.85:
            print(
                name1, name_days[name1],
                "<->",
                name2, name_days[name2],
                round(score, 2)
            )

alias_map = {
    "dusty1o3": "dusty103",
    "saltylen": "saltyjen",
    "mojosodopez011": "mojosodopezo11",
    "pisacater": "pisaeater",
    "germanyz3": "germany23",
    "steeveelo": "steevee1o",
    "becf man": "beef man",
    "nutcasccarpenter": "nutcasecarpenter",
    "melonsmcdanicls": "melonsmcdaniels",

    "ofolnoah": "ofo noah",
    "ofq noah": "ofo noah",
    "ofoinoah": "ofo noah",

    "nickrod1g": "nickrod",
    "nickrod1z": "nickrod",
    "nickrod1b": "nickrod",

    "thegreatoncz0z4": "thegreatone2024",
    "thegreatone20z4": "thegreatone2024",
    "thegreatonez0z4": "thegreatone2024",
    "thegreatonczoz4": "thegreatone2024",
    # Hellhole family
    "hellholez0z4": "hellhole2024",
    "hellhole20z4": "hellhole2024",
    "hellhole2024": "hellhole2024",

    # Juninho family
    "juninho2024": "juninho2024",
    "juninhozoz4": "juninho2024",
    "juninho20z4": "juninho2024",
    "juninhoz0z4": "juninho2024",

    # Neneuu OCR error
    "meneuu": "neneuu",

    # RKC family
    "rkcz4": "rkc24",
    "rkc24": "rkc24",

    # Polished family
    "polishedo7": "polishedo7",
    "polishedoz": "polishedo7",

    # CHAVES family
    "[have 5": "chav e 5",
    "[aav e 5": "chav e 5",
    "chav e 5": "chav e 5",

    # Five-day stylized/non-Latin family A
    "fel+li": "nonlatin_a",
    "sl+4i": "nonlatin_a",
    "el+4i": "nonlatin_a",
    "94+41": "nonlatin_a",
    "5944i": "nonlatin_a",

    # Five-day stylized/non-Latin family B
    "g25c4": "nonlatin_b",
    "43=ch": "nonlatin_b",
    "g354h": "nonlatin_b",
    "435ch": "nonlatin_b",
    "g3=ch": "nonlatin_b",

    # Five-day stylized/non-Latin family C
    "xize ti?ix}": "nonlatin_c",
    "ti7e ti?ix}": "nonlatin_c",
    "xi7= *i?ix}": "nonlatin_c",
    "tizf ti7ix}": "nonlatin_c",
    # Flying family
    "flying": "flying",
    "bull its flying": "flying",

    # Naay family
    "naay": "naay",
    "nazy": "naay",

    # Kaaaaa family
    "kaaaaa": "kaaaaa",
    "kcaaca": "kaaaaa",

    # Clellz family
    "4#clellz": "pzclellz",
    "pzclellz": "pzclellz",
    "p22clellz": "pzclellz",
    "9zcieiz": "pzclellz",

       # J family
    # Arabic commander - exact Arabic canonical name will be handled separately
    "j": "j",
    "joj": "j",
    "jaj": "j",

    # Korean: 모바일
    # Row-anchored Korean OCR confirmed this identity across multiple days.
    "54/9": "모바일",
    "24/8": "모바일",
    "28/8": "모바일",
    "50/9": "모바일",
    "24/4": "모바일",

    # Korean: 편한세상만세
    # Strong repeated row-anchored reads across multiple days.
    "helxlzntal": "편한세상만세",
    "#etxaptxl": "편한세상만세",
    "metxartll": "편한세상만세",
    "halxla@al": "편한세상만세",
    "dzxla@xl": "편한세상만세",

    # Korean: 징가Z
    # English OCR repeatedly mangled the Korean characters into numeric-looking text.
    "37z": "징가z",
    "3217": "징가z",

    # Korean: 검환장
    # Repeated row-anchored Korean OCR across multiple days.
    "423": "검환장",
    "42g": "검환장",
    "h28": "검환장",

    # Korean: 슬로버
    # Korean OCR varies slightly, but row/points evidence ties these observations together.
    "420": "슬로버",
    "4201": "슬로버",
    "241": "슬로버",
    "224": "슬로버",

    # Korean commander - OCR spelling still varies.
    # Keep one stable canonical identity while preserving original OCR in ocr_name.
    "803": "응이랑",
    "g0a": "응이랑",
    "303": "응이랑",

    # Korean: 희망이 family
    # Strong row-anchored identity match; exact first syllable still needs final visual confirmation.
    "ofel 4g01": "야인 희망이",
    "ofe 2go1": "야인 희망이",
    "otel 4g01": "야인 희망이",
    "ofel ag0": "야인 희망이",

    # Korean: 징가Z
    "327": "징가z",

    # Korean: 희망이 family - Monday zero-point OCR variant
    "of8 2go1": "야인 희망이",

    # Korean: 휘킹발할라
    "43422": "휘킹발할라",
    "93442": "휘킹발할라",
    "434221": "휘킹발할라",
    "434321": "휘킹발할라",
    "43442": "휘킹발할라",
    "43432": "휘킹발할라",

}


for row in clean_rows:
    normalized = row["commander"].lower().strip()

    if normalized in alias_map:
        row["canonical_name"] = alias_map[normalized]
    else:
        row["canonical_name"] = normalized

final_rows = {}

for row in clean_rows:
    key = (row["day"], row["canonical_name"])

    if key not in final_rows:
        final_rows[key] = row

    if row["points"] > final_rows[key]["points"]:
        final_rows[key] = row

clean_rows = list(final_rows.values())

print("\nAfter canonical dedupe:", len(clean_rows))

canonical_names = []

for row in clean_rows:
    if row["canonical_name"] not in canonical_names:
        canonical_names.append(row["canonical_name"])

print("\nCanonical identities:", len(canonical_names))
for canonical_name in canonical_names:
    print(canonical_name)

canonical_counts = {}

for row in clean_rows:
    canonical_name = row["canonical_name"]

    if canonical_name not in canonical_counts:
        canonical_counts[canonical_name] = 0

    canonical_counts[canonical_name] += 1

print("\nIDENTITIES WITH FEWER THAN 5 DAYS:")

for canonical_name, count in canonical_counts.items():
    if count < 5:
        print(canonical_name, count)


print("\n\n========== IDENTITY REVIEW ==========")

# Build a list of observations for each current canonical identity
identity_rows = {}

for row in clean_rows:
    canonical_name = row["canonical_name"]

    if canonical_name not in identity_rows:
        identity_rows[canonical_name] = []

    identity_rows[canonical_name].append(row)


# Show only identities that do NOT currently have exactly 5 observations
for canonical_name, observations in identity_rows.items():

    if len(observations) != 5:

        print("\n---", canonical_name, "---")

        for row in observations:
            print(
                row["day"],
                "| OCR:", row["commander"],
                "| Points:", row["points"]
            )


print("\n\n========== ORDERED DAILY ROSTERS ==========")

days = ["mon.csv", "tue.csv", "wed.csv", "thur.csv", "fri.csv"]

for day in days:

    print("\n\n###", day.upper(), "###")

    position = 1

    for row in clean_rows:

        if row["day"] == day:
            print(
                position,
                "| OCR:", row["commander"],
                "| Canonical:", row["canonical_name"],
                "| Points:", row["points"]
            )

            position += 1

print("\n\n========== MISSING-DAY MATCH CANDIDATES ==========")

days = ["mon.csv", "tue.csv", "wed.csv", "thur.csv", "fri.csv"]

# Build a dictionary showing which days each identity appears
canonical_days = {}

for row in clean_rows:
    name = row["canonical_name"]

    if name not in canonical_days:
        canonical_days[name] = []

    if row["day"] not in canonical_days[name]:
        canonical_days[name].append(row["day"])


# Look only at identities that appear on 2, 3, or 4 days.
# These are especially useful because another OCR fragment may
# perfectly fill their missing day(s).

for name, seen_days in canonical_days.items():

    if len(seen_days) >= 2 and len(seen_days) < 5:

        missing_days = []

        for day in days:
            if day not in seen_days:
                missing_days.append(day)

        print("\n---", name, "---")
        print("Seen:", seen_days)
        print("Missing:", missing_days)

        print("Possible fragments on missing days:")

        for row in clean_rows:

            if row["day"] in missing_days:

                candidate = row["canonical_name"]
                candidate_days = canonical_days[candidate]

                # Only show identities that themselves appear
                # on fewer than 5 days.
                if len(candidate_days) < 5:

                    score = SequenceMatcher(
                        None,
                        name,
                        candidate
                    ).ratio()

                    if score >= 0.30:
                        print(
                            row["day"],
                            "|",
                            candidate,
                            "| OCR:",
                            row["commander"],
                            "| similarity:",
                            round(score, 2),
                            "| points:",
                            row["points"]
                        )

print("\n\n========== EXPORTING CLEAN DATA ==========")

date_map = {
    "mon.csv": "2026-10-12",
    "tue.csv": "2026-10-13",
    "wed.csv": "2026-10-14",
    "thur.csv": "2026-10-15",
    "fri.csv": "2026-10-16"
}

output_file = "output/participation_clean.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "date",
            "day",
            "commander",
            "ocr_name",
            "points"
        ]
    )

    writer.writeheader()

    for row in clean_rows:
        writer.writerow({
            "date": date_map[row["day"]],
            "day": row["day"],
            "commander": row["canonical_name"],
            "ocr_name": row["commander"],
            "points": row["points"]
        })

print("Saved", len(clean_rows), "rows to", output_file)