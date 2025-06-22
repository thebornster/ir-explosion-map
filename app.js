document.addEventListener('DOMContentLoaded', () => {
  let iranCities = [];

  fetch('iranCities.json')
    .then(response => response.json())
    .then(data => { iranCities = data; })
    .catch(err => console.error('Failed to load iranCities.json:', err));

  const searchBox = document.getElementById('searchBox');
  const suggestionBox = document.getElementById('suggestions');

  Object.assign(suggestionBox.style, {
    position: 'absolute', zIndex: '1001', left: '50%', transform: 'translateX(-50%)',
    width: '300px', background: 'white', listStyle: 'none',
    padding: '0', marginTop: '5px', border: '1px solid #ccc',
    maxHeight: '150px', overflowY: 'auto', fontSize: '14px'
  });

  const map = L.map('map').setView([32.4279, 53.688], 6);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(map);

  let allMarkers = [];

  fetch('/api/fetchMarkers')
    .then(res => res.json())
    .then(records => {
      records.forEach(record => {
        const {
          Latitude: lat,
          Longitude: lon,
          Description: desc = 'بدون توضیح',
          Date: date = 'تاریخ نامشخص',
          Time: time = 'زمان نامشخص',
          EventType: eventType = 'نامشخص',
          TargetType: targetType = 'نامشخص',
          LikelyLocation: likelyLocation = 'نامشخص',
          Link: link = ''
        } = record.fields;

        if (typeof lat !== 'number' || typeof lon !== 'number') return;

        let iconColor = 'gray';
        const dateParts = date.split('-').map(Number);
        const timeDecimal = parseFloat(time);

        if (dateParts.length === 3 && !isNaN(timeDecimal)) {
          const [year, month, day] = dateParts;
          const hours = Math.floor(timeDecimal);
          const minutes = Math.round((timeDecimal - hours) * 100);
          const iranLocalDate = new Date(Date.UTC(year, month - 1, day, hours, minutes));
          const iranOffsetMs = 3.5 * 60 * 60 * 1000;
          const iranTimeUtcMs = iranLocalDate.getTime() - iranOffsetMs;
          const eventDate = new Date(iranTimeUtcMs);
          const nowUtc = new Date();
          const iranNow = new Date(nowUtc.getTime() + iranOffsetMs);
          const isSameIranDay = eventDate.toDateString() === iranNow.toDateString();

          iconColor = isSameIranDay ? 'red' : 'gray';
        }

        const icon = new L.Icon({
          iconUrl: iconColor === 'red' ? '/assets/RedMarkerIcon.png' : '/assets/GrayMarkerIcon.png',
          iconSize: [32, 32],
          iconAnchor: [16, 32],
          popupAnchor: [0, -32]
        });

        const popupHtml = `
          <div style="font-size:14px; line-height:1.6;">
            <strong>تاریخ و زمان:</strong> ${date} - ${parseFloat(time).toFixed(2)}<br>
            <strong>توضیح:</strong> ${desc}<br>
            <strong>نوع رویداد:</strong> ${eventType}<br>
            <strong>نوع هدف:</strong> ${targetType}<br>
            <strong>مکان احتمالی:</strong> ${likelyLocation}<br>
            ${link ? `<strong>لینک:</strong> <a href="${link}" target="_blank">مشاهده</a>` : ''}
          </div>
        `;

        const marker = L.marker([lat, lon], { icon }).addTo(map)
          .bindPopup(popupHtml);

        allMarkers.push(marker);
      });
    }).catch(err => console.error("Error loading marker data:", err));

  searchBox.addEventListener('input', () => {
    const query = searchBox.value.trim().toLowerCase();
    suggestionBox.innerHTML = '';

    if (query.length >= 2) {
      const matched = iranCities.filter(place => place.name.toLowerCase().includes(query));
      matched.forEach(place => {
        const li = document.createElement('li');
        li.textContent = place.name;
        li.style.padding = '8px';
        li.style.cursor = 'pointer';
        li.addEventListener('click', () => {
          map.setView([place.latitude, place.longitude], 10);
          suggestionBox.innerHTML = '';
          searchBox.value = place.name;
        });
        suggestionBox.appendChild(li);
      });
    }
  });
});
