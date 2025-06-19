export default async function handler(req, res) {
  const AIRTABLE_TOKEN = process.env.AIRTABLE_READ_TOKEN;
  const BASE_ID = process.env.AIRTABLE_BASE_ID;
  const TABLE_NAME = "Table 1";

  let offset = '';
  let allRecords = [];

  try {
    do {
      const url = `https://api.airtable.com/v0/${BASE_ID}/${encodeURIComponent(TABLE_NAME)}${offset ? `?offset=${offset}` : ''}`;
      const response = await fetch(url, {
        headers: {
          Authorization: `Bearer ${AIRTABLE_TOKEN}`
        }
      });

      const data = await response.json();
      if (data.records) {
        allRecords = allRecords.concat(data.records);
      }
      offset = data.offset;
    } while (offset);

    res.status(200).json(allRecords);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to fetch records from Airtable" });
  }
}
