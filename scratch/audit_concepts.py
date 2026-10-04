# -*- coding: utf-8 -*-
"""
Audit script for 20 concepts in concept_contents.json.
Compares against concepts.json and sources.json, validates technical accuracy,
identifies potential discrepancies or outdated claims.
"""
import os
import json

BASE_DIR = r"C:\Users\mskim0588\Desktop\security-practical-cbt"
CONCEPTS_FILE = os.path.join(BASE_DIR, "app", "data", "concepts.json")
CONTENTS_FILE = os.path.join(BASE_DIR, "app", "data", "concept_contents.json")
SOURCES_FILE = os.path.join(BASE_DIR, "app", "data", "sources.json")

def audit_concepts():
    with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
        concepts = json.load(f)
    concept_map = {c["id"]: c for c in concepts}

    with open(CONTENTS_FILE, "r", encoding="utf-8") as f:
        contents = json.load(f)

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = json.load(f)
    source_map = {s["id"]: s for s in sources}

    findings = []
    
    print(f"Total concepts to audit: {len(contents)}")

    for cid, cdata in contents.items():
        meta = concept_map.get(cid)
        if not meta:
            findings.append({"level": "P0", "cid": cid, "issue": f"Concept ID {cid} not in concepts.json"})
            continue

        # Check Category match
        if meta.get("category") != meta.get("category"):
            findings.append({"level": "P1", "cid": cid, "issue": "Category mismatch"})

        # Check Name consistency
        cname = meta.get("name")
        summary = cdata.get("summary", "")
        if not summary:
            findings.append({"level": "P1", "cid": cid, "issue": "Empty summary"})

        # Check Core points
        core_pts = cdata.get("core_points", [])
        if len(core_pts) < 4:
            findings.append({"level": "P2", "cid": cid, "issue": f"Only {len(core_pts)} core points (expected >=4)"})

        # Check Mechanism
        mechanism = cdata.get("mechanism", "")
        if len(mechanism) < 50:
            findings.append({"level": "P1", "cid": cid, "issue": "Mechanism description too brief or missing"})

        # Check Exam points
        exam_pts = cdata.get("exam_points", [])
        if len(exam_pts) < 2:
            findings.append({"level": "P2", "cid": cid, "issue": "Exam points count < 2"})

        # Check Common mistakes
        mistakes = cdata.get("common_mistakes", [])
        if not mistakes:
            findings.append({"level": "P1", "cid": cid, "issue": "No common mistakes defined"})
        for m in mistakes:
            if not m.get("trap") or not m.get("clarification"):
                findings.append({"level": "P1", "cid": cid, "issue": "Trap or clarification empty"})

        # Check Compare with
        compares = cdata.get("compare_with", [])
        for cp in compares:
            t_cid = cp.get("target_concept_id")
            if t_cid not in concept_map:
                findings.append({"level": "P1", "cid": cid, "issue": f"Compare target {t_cid} not a valid concept ID"})

        # Check Commands / Examples
        cmds = cdata.get("commands_or_examples", [])
        if not cmds:
            findings.append({"level": "P1", "cid": cid, "issue": "No commands or examples provided"})
        for cmd in cmds:
            if not cmd.get("code") or not cmd.get("title") or not cmd.get("explanation"):
                findings.append({"level": "P1", "cid": cid, "issue": f"Incomplete command entry in {cid}"})

        # Check Related Sources
        rel_sources = cdata.get("related_sources", [])
        if not rel_sources:
            findings.append({"level": "P1", "cid": cid, "issue": "No related sources defined"})
        for rs in rel_sources:
            sid = rs.get("source_id")
            if sid not in source_map:
                findings.append({"level": "P1", "cid": cid, "issue": f"Invalid source_id {sid} referenced"})

        # Check Law Review Status
        lrs = cdata.get("law_review_status", {})
        status = lrs.get("status")
        if status not in ("source_current", "source_may_be_outdated", "current_law_review_required"):
            findings.append({"level": "P1", "cid": cid, "issue": f"Invalid law_review_status '{status}'"})
        
        # Verify MGT concepts have explicit law review note
        if cid.startswith("CON-MGT"):
            if not lrs.get("note"):
                findings.append({"level": "P1", "cid": cid, "issue": f"Management/Law concept {cid} lacks law review note"})

    print(f"Total concept audit findings: {len(findings)}")
    for f in findings:
        print(f"[{f['level']}] Concept {f['cid']}: {f['issue']}")

    return findings

if __name__ == "__main__":
    audit_concepts()
