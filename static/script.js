let map = L.map('map').setView([43.7, -79.42], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let selectedLatLng = null;

map.on('click', function(e) {
    map.eachLayer((layer) => {
        if (layer instanceof L.Marker && !(layer instanceof L.CircleMarker)) {
            map.removeLayer(layer);
        }
    });
    selectedLatLng = e.latlng;
    L.marker(e.latlng).addTo(map);
});

document.getElementById('reportForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    if (!selectedLatLng) {
        alert('Click on the map to choose a location.');
        return;
    }

    const formData = new FormData();
    formData.append('lat', selectedLatLng.lat);
    formData.append('lon', selectedLatLng.lng);
    formData.append('description', document.getElementById('description').value);
    formData.append('issue_type', document.getElementById('issueType').value);
    const imageFile = document.getElementById('imgUpload').files[0];
    if (imageFile) {
        formData.append('image', imageFile);
    }

    const res = await fetch('/report', {
        method: 'POST',
        body: formData
    });

    const data = await res.json();
    if (data.status === 'duplicate') {
        alert('This issue has already been reported nearby.');
    } else if (data.status === 'unauthorized') {
        alert('You must be logged in to report.');
    } else {
        alert('Issue reported successfully!');
    }
    document.getElementById('reportForm').reset();
    selectedLatLng = null;
    previewPic.src = "";
});

const select = document.getElementById('reportList');
let selectedReportId = null;

const image = document.getElementById('previewImage');
const reportImage = document.getElementById('reportImage');

let reportMarkers = {};
fetch('/reports')
    .then(res => res.json())
    .then(reports => {
        reports.forEach(r => {
            let markerColor = 'yellow';
            switch(r.issue_type) {
                case 'Pothole': markerColor = 'red'; break;
                case 'Streetlight': markerColor = 'green'; break;
                case 'Garbage': markerColor = 'blue'; break;
                case 'Graffiti': markerColor = 'orange'; break;
            }
            const marker = L.circleMarker([r.lat, r.lon], { color: markerColor })
                .bindPopup(`${r.issue_type}: ${r.description}`)
                .addTo(map);
            reportMarkers[r.unique_id] = marker;
            const option = document.createElement('option');
            option.innerHTML = r.unique_id + ": " + r.issue_type + " - " + r.description;
            option.value = r.unique_id;
            select.appendChild(option);
            
            marker.on('click', function() {
                reportImage.src = `/image/${r.unique_id}`;
                reportImage.style.display = 'block';
            });
        });
    });

select.addEventListener('change', function() {
    selectedReportId = this.value;
    if (selectedReportId) {
        reportImage.src = `/image/${selectedReportId}`;
        reportImage.style.display = 'block';
    } else {
        reportImage.style.display = 'none';
    }
});

async function resolve() {
    const uniqueIdToDelete = select.value;
    if (!uniqueIdToDelete) return;

    await fetch('/resolved', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ unique_id: uniqueIdToDelete })
    });

    if (reportMarkers[uniqueIdToDelete]) {
        map.removeLayer(reportMarkers[uniqueIdToDelete]);
        delete reportMarkers[uniqueIdToDelete];
    }

    await refreshReportList();  // Always reload clean list
}


const resolveButton = document.getElementById('resolveButton');
if (resolveButton) {
    resolveButton.addEventListener('click', resolve);
}

let previewPic = document.getElementById("previewImage");
let uploadedPic = document.getElementById("imgUpload");

uploadedPic.onchange = function() {
    if (this.files && this.files[0]) {
        previewPic.src = URL.createObjectURL(this.files[0]);
        previewPic.style.display = 'block';
    }
};

async function refreshReportList() {
    select.innerHTML = ''; // Clear all options
    const res = await fetch('/reports');
    const reports = await res.json();

    reports.forEach(r => {
        const option = document.createElement('option');
        option.innerHTML = r.unique_id + ": " + r.issue_type + " - " + r.description;
        option.value = r.unique_id;
        select.appendChild(option);
    });
}
