import json

with open("candidates_dump.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("candidate_details.txt", "w", encoding="utf-8") as out:
    out.write("=== SRC-01 p.21 ===\n")
    out.write(data["SRC-01"]["21"] + "\n\n")
    out.write("=== SRC-01 p.22 ===\n")
    out.write(data["SRC-01"]["22"] + "\n\n")
    out.write("=== SRC-01 p.23 ===\n")
    out.write(data["SRC-01"]["23"] + "\n\n")

    out.write("=== SRC-02 pages 1 to 17 ===\n")
    for p in range(1, 18):
        out.write(f"\n--- SRC-02 Page {p} ---\n")
        out.write(data["SRC-02"][str(p)] + "\n")
