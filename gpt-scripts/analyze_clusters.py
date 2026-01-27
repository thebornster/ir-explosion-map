import json
import os
import openai
from json import JSONDecodeError

openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_output(obj, required_keys):
    for key in required_keys:
        if key not in obj:
            raise ValueError(f"Missing key in GPT output: {key}")

def analyze_single(report):
    prompt = f"""
You are an intelligence analyst. A citizen submitted the following translated report:

---
Report: "{report['translated_text']}"
Location Guess: {report['location_guess']}
Event Features: {', '.join(report['event_features'])}
Certainty: {report['certainty']}
Landmarks Mentioned: {', '.join(report['landmarks_mentioned'])}
Datetime: {report['datetime']}
---

Analyze and answer:
1. Is this likely an explosion event?
2. Where exactly do you think it happened?
3. What kind of facility or target might be involved (military, nuclear, industrial, etc.)?
4. Estimate the approximate latitude and longitude of the likely location.
5. Summarize your reasoning in Farsi.

Output only valid JSON with:
- "event_type"
- "likely_location"
- "likely_target_type"
- "latitude"
- "longitude"
- "summary_farsi"
- "source_link"
    """

    messages = [
        {"role": "system", "content": "You are an intelligence analyst tasked with identifying explosions in Iran based on citizen reports."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()
    try:
        result = json.loads(content)
    except JSONDecodeError:
        print("⚠️ Invalid JSON from GPT for report ID:", report.get("id", "unknown"))
        print(content)
        raise

    validate_output(result, ["event_type", "likely_location", "likely_target_type", "latitude", "longitude", "summary_farsi"])
    result["source_link"] = report.get("link", "")
    return result

def analyze_cluster(cluster):
    reports_text = "\n\n".join(
        f"- {r['translated_text']} (Certainty: {r['certainty']}, Time: {r['datetime']})"
        for r in cluster
    )
    prompt = f"""
You are a multilingual intelligence analyst. Below are citizen reports, likely related to the same event:

{reports_text}

Instructions:
1. Are these reports likely describing the same explosion?
2. If yes, infer:
   - The most probable location (city/area)
   - The type of facility or target (military base, nuclear site, etc.)
   - Approximate latitude and longitude of that location
   - A brief summary of your reasoning in Farsi
3. If not related, explain why.

Return JSON with:
- "related_event": true/false
- "likely_location"
- "likely_target_type"
- "latitude"
- "longitude"
- "summary_farsi"
- "source_link": link from the most confident report
    """

    best = max(cluster, key=lambda r: r.get("certainty", "low") == "high")

    messages = [
        {"role": "system", "content": "You are an intelligence analyst tasked with identifying explosions in Iran based on citizen reports."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()
    try:
        result = json.loads(content)
    except JSONDecodeError:
        print("⚠️ Invalid JSON from GPT for cluster:")
        print(content)
        raise

    validate_output(result, ["related_event", "likely_location", "likely_target_type", "latitude", "longitude", "summary_farsi"])
    result["source_link"] = best.get("link", "")
    return result

def main():
    with open("grouped_reports.json", "r", encoding="utf-8") as f:
        clusters = json.load(f)

    with open("final_analysis.jsonl", "a", encoding="utf-8") as f:
        for idx, cluster_obj in enumerate(clusters):
            cluster = cluster_obj["all_reports"]
            try:
                print(f"\n🔍 Analyzing cluster {idx+1}/{len(clusters)} ({len(cluster)} reports)...")
                result = analyze_single(cluster[0]) if len(cluster) == 1 else analyze_cluster(cluster)
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
            except Exception as e:
                print("❌ Error analyzing cluster:", e)

if __name__ == "__main__":
    main()
