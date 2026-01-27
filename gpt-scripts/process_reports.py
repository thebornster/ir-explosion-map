import json
import os
import openai
from json import JSONDecodeError

openai.api_key = os.getenv("OPENAI_API_KEY")

def validate_output(obj, required_keys):
    for key in required_keys:
        if key not in obj:
            raise ValueError(f"Missing key in GPT output: {key}")

def process_report(item):
    report_text = item.get("report")
    datetime_val = item.get("datetime")
    report_id = item.get("id", "")
    link = item.get("link", "")

    if not report_text or not datetime_val:
        raise ValueError("Missing required fields 'report' or 'datetime'")

    prompt = f"""
You are a multilingual analyst. A citizen has submitted the following Farsi report about a possible explosion:

---
Report: "{report_text}"
Datetime: {datetime_val}
---

Your tasks:
1. Translate the report into English.
2. Extract structured data:
    - "id": from input
    - "translated_text": your translation
    - "location_guess": approximate place mentioned
    - "event_features": list of features (e.g., ["sound", "flash", "shockwave"])
    - "relative_time": expression like "a few minutes ago" or "just now"
    - "certainty": "high", "medium", or "low" based on how confident the report sounds
    - "landmarks_mentioned": list of places or facilities mentioned
    - "link": from input

Return only a valid JSON object.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content.strip()
        result = json.loads(content)
        validate_output(result, [
            "id", "translated_text", "location_guess", "event_features",
            "relative_time", "certainty", "landmarks_mentioned", "link"
        ])
        return result

    except JSONDecodeError:
        print("⚠️ Invalid JSON from GPT for report ID:", report_id)
        print(content)
        raise
    except Exception as e:
        print(f"❌ Error processing report ID {report_id}: {e}")
        raise

def main():
    with open("telegram_posts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    for item in data:
        try:
            structured = process_report(item)
            results.append(structured)
        except Exception:
            continue  # Already printed inside process_report()

    with open("processed_reports.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
