# nfejar.online - IR Explosion Map

## Overview

nfejar.online visualizes explosion events in Iran, during regional conflicts in the middle east, based on citizen-submitted reports from Telegram. The platform aggregates, processes, and analyzes reports to provide approximate locations, event types, and target classifications. The website aims to inform the general public about areas affected by explosions.

## Features

* Interactive map of Iran displaying explosion events as markers.
* Clickable markers show:

  * Date of event
  * Description
  * Event type
  * Target type (e.g., military, industrial)
  * Probable location
  * Link to original Telegram reports
* City search functionality.
* Data updates automatically on a scheduled interval.

## Architecture

* **Frontend:** HTML & CSS
* **Backend/Data Pipeline:** Python scripts executed via GitHub Actions
* **Database:** Airtable
* **Hosting:** Vercel
* **External APIs:** OpenAI API (GPT-3.5 & GPT-4.5)

### Pipeline Overview

1. **Scraping:** Reports are gathered from Telegram (bot located in a separate repository).
2. **Pre-Clustering:** Similar reports are grouped together.
3. **GPT-3.5 Cleaning:** Each report is translated and structured into JSON.
4. **GPT-4.5 Analysis:** Clusters or individual reports are analyzed to determine:

   * Event type
   * Likely target type
   * Estimated latitude and longitude
   * Summary reasoning in Farsi
5. **Database Integration:** Structured results are saved to Airtable.
6. **Website Rendering:** Data is fetched from Airtable and displayed on the map.

## Installation & Setup

This repository primarily serves as a data visualization frontend; the backend pipeline runs via GitHub Actions. For development or local execution:

1. Clone the repository:

```bash
git clone https://github.com/your-org/ir-explosion-map.git
cd ir-explosion-map
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set environment variables:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export AIRTABLE_API_KEY="your_airtable_api_key"
export AIRTABLE_BASE_ID="your_airtable_base_id"
```

4. Place input Telegram data (`telegram_posts.json` or `grouped_reports.json`) in the project root if running scripts locally.

5. Run scripts:

```bash
python process_reports.py   # GPT-3.5 translation and cleaning
python analyze_reports.py   # GPT-4.5 cluster analysis
```


## Usage

* Use Airtable to display the markers in the website
* Click markers to inspect event details.
* Use the search bar to locate events by city.
* Note: Data updates may have slight delays due to scheduled GitHub Actions.

## Limitations

* Accuracy depends on citizen reports from Telegram.
* Approximate locations and classifications are model predictions and may contain errors.
* Some events may be missing or misclassified.

## Contributing

* Contributions to the frontend map visualization or documentation are welcome.
* The Telegram bot and scraping logic reside in a separate repository.
* Ensure API keys and sensitive data are not committed.

## License

* This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Acknowledgments

* OpenAI for GPT-3.5 and GPT-4.5 APIs.
* Airtable for database management.
* Vercel for hosting.
* Citizen reporters on Telegram whose submissions power this platform.
