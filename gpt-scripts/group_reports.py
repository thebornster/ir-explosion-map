import json
from datetime import datetime, timedelta
from collections import Counter
from rapidfuzz.fuzz import ratio
from statistics import median

def parse_iso(date_str):
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return None

def are_locations_similar(loc1, loc2, threshold=80):
    if not loc1 or not loc2:
        return False
    return ratio(loc1.lower(), loc2.lower()) >= threshold

def validate_report(report):
    required_fields = ["datetime", "location_guess"]
    for field in required_fields:
        if not report.get(field):
            return False
    return True

def most_common(items):
    return Counter(items).most_common(1)[0][0] if items else "Unknown"

def cluster_by_time_and_location(reports, time_window_minutes=30):
    clusters = []
    used = set()
    time_window = timedelta(minutes=time_window_minutes)

    for i, report in enumerate(reports):
        if i in used:
            continue

        candidate_group = [report]
        loc_i = report.get("location_guess", "").strip().lower()
        used.add(i)

        for j, other in enumerate(reports[i+1:], start=i+1):
            if j in used:
                continue
            loc_j = other.get("location_guess", "").strip().lower()
            if are_locations_similar(loc_i, loc_j):
                candidate_group.append(other)

        # Median-based time filtering
        times = [parse_iso(r["datetime"]) for r in candidate_group if parse_iso(r["datetime"])]
        if not times:
            continue
        median_time = sorted(times)[len(times)//2]
        filtered_group = [
            r for r in candidate_group
            if parse_iso(r["datetime"]) and abs(parse_iso(r["datetime"]) - median_time) <= time_window
        ]

        for r in filtered_group:
            idx = reports.index(r)
            used.add(idx)

        clusters.append(filtered_group)

    return clusters

def main():
    with open("processed_reports.json", "r", encoding="utf-8") as f:
        reports = json.load(f)

    valid_reports = [r for r in reports if validate_report(r)]
    print(f"Loaded {len(valid_reports)} valid reports out of {len(reports)} total.")

    clusters = cluster_by_time_and_location(valid_reports)

    output = []
    for i, cluster in enumerate(clusters):
        if not cluster:
            continue
        times = [parse_iso(r["datetime"]) for r in cluster if parse_iso(r["datetime"])]
        locations = [r["location_guess"] for r in cluster if r.get("location_guess")]
        output.append({
            "cluster_id": i + 1,
            "cluster_size": len(cluster),
            "location": most_common(locations),
            "start_time": min(times).isoformat() if times else None,
            "end_time": max(times).isoformat() if times else None,
            "representative_report": cluster[0],
            "all_reports": cluster
        })

    with open("grouped_reports.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
