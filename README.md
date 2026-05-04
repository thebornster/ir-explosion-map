# nfejar.online - IR Explosion Map

## Overview

nfejar.online visualizes explosion events in Iran, based on citizen-submitted reports from Telegram. The platform aggregates, processes, and analyzes reports to provide approximate locations, event types, and target classifications. The website aims to inform the general public about areas affected by explosions.

## Features

* Interactive map of Iran displaying explosion events as color-coded markers.
* Clickable markers show:

  * Date of event
  * Description
  * Event type (explosion, strike, fire, other)
  * Target type (e.g., military, industrial)
  * Probable location
  * Link to original Telegram reports
* City/event search functionality with autocomplete.
* Side panel for submitting new event reports to Airtable.
* Data updates automatically on a scheduled interval.
* Toast notifications for user feedback.
* Mobile responsive layout.

## Architecture

* **Frontend:** Single-file HTML with inline CSS/JS (`index.html`)
* **Backend/Data Pipeline:** Python scripts executed via GitHub Actions
* **API:** Vercel Serverless Functions (`api/fetchMarkers.js`, `api/submitMarker.js`)
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
6. **Website Rendering:** Data is fetched from Airtable via serverless API and displayed on the map.

## Deployment

This project is deployed on Vercel as a static site with serverless API functions.

### Environment Variables (set in Vercel dashboard)

```
AIRTABLE_READ_TOKEN    — Airtable read-only personal access token
AIRTABLE_WRITE_TOKEN   — Airtable write personal access token
AIRTABLE_BASE_ID       — Airtable base ID
```

### Local Development

For local development with API routes, use the Vercel CLI:

```bash
npm i -g vercel
vercel dev
```

## Usage

* Events are automatically loaded from Airtable on page load.
* Click markers to inspect event details.
* Use the search bar to locate events by city or description.
* Click "ثبت رویداد" to submit new event reports.
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
