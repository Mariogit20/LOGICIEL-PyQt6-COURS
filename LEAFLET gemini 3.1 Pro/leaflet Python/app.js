$(document).ready(function() {
    // Initialisation centrée sur Antananarivo
    var map = L.map('map').setView([-18.8792, 47.5079], 12);

    // 1. Couche Croquis (CartoDB - sans erreur 403)
    var coucheCroquis = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors, © CARTO',
        crossOrigin: true 
    });

    // 2. Couche Satellite HD (Esri World Imagery - Gratuit, HD, pas d'API requise)
    var coucheSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,
        attribution: 'Tiles © Esri',
        crossOrigin: true
    });

    // Affichage de la couche satellite par défaut
    coucheSatellite.addTo(map);

    var baseMaps = {
        "IMAGE SATELLITE (Esri HD)": coucheSatellite,
        "IMAGE CROQUIS (Carto)": coucheCroquis
    };
    L.control.layers(baseMaps).addTo(map);

    // --- COORDONNÉES GPS ---
    var coordsControl = L.control({position: 'bottomleft'});
    coordsControl.onAdd = function(map) {
        this._div = L.DomUtil.create('div', 'info coords');
        this.update(map.getCenter());
        return this._div;
    };
    coordsControl.update = function(latlng) {
        this._div.innerHTML = '🌍 Centre : ' + latlng.lat.toFixed(5) + ' N, ' + latlng.lng.toFixed(5) + ' E';
    };
    coordsControl.addTo(map);

    map.on('move', function() { coordsControl.update(map.getCenter()); });

    // --- RECHERCHE ---
    var searchMarker;
    function lancerRecherche() {
        var query = $('#search-input').val();
        if (query.trim() !== '') {
            $.ajax({
                url: 'https://nominatim.openstreetmap.org/search',
                type: 'GET',
                data: { format: 'json', q: query, limit: 1 },
                success: function(data) {
                    if (data && data.length > 0) {
                        var lat = data[0].lat;
                        var lon = data[0].lon;
                        map.flyTo([lat, lon], 15, { duration: 2 });
                        if (searchMarker) map.removeLayer(searchMarker);
                        searchMarker = L.marker([lat, lon]).addTo(map)
                            .bindPopup('<b>Résultat :</b><br>' + data[0].display_name).openPopup();
                    } else {
                        alert("Lieu introuvable.");
                    }
                }
            });
        }
    }
    $('#search-button').click(lancerRecherche);
    $('#search-input').keypress(function(e) { if (e.which == 13) lancerRecherche(); });

    // --- CAPTURE D'ÉCRAN ---
    $('#capture-button').click(function() {
        var btn = $(this);
        var texteOriginal = btn.text();
        btn.text('⏳ Capture...');

        html2canvas(document.querySelector("#map"), {
            useCORS: true,
            allowTaint: false
        }).then(canvas => {
            var link = document.createElement('a');
            link.download = 'capture_carte.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
            btn.text(texteOriginal);
        }).catch(err => {
            console.error(err);
            btn.text(texteOriginal);
        });
    });

    // --- OUTIL DE MESURE ---
    var isMeasuring = false;
    var measureLayer = L.featureGroup().addTo(map);
    var pointsMesure = [];

    $('#measure-button').click(function() {
        isMeasuring = !isMeasuring;
        if (isMeasuring) {
            $(this).css('background-color', '#ffc107').css('color', 'black').text('Annuler la mesure');
            $('.leaflet-container').css('cursor', 'crosshair');
            measureLayer.clearLayers();
            pointsMesure = [];
        } else {
            $(this).css('background-color', '#17a2b8').css('color', 'white').text('📏 Mesurer une distance');
            $('.leaflet-container').css('cursor', '');
            measureLayer.clearLayers();
        }
    });

    map.on('click', function(e) {
        if (!isMeasuring) return;
        pointsMesure.push(e.latlng);
        L.circleMarker(e.latlng, { color: 'red', radius: 5 }).addTo(measureLayer);

        if (pointsMesure.length === 2) {
            var polyline = L.polyline(pointsMesure, {color: 'red', weight: 4}).addTo(measureLayer);
            var distanceMetres = map.distance(pointsMesure[0], pointsMesure[1]);
            var distanceKm = (distanceMetres / 1000).toFixed(2);
            polyline.bindPopup("<b>Distance :</b> " + distanceKm + " km").openPopup();
            
            isMeasuring = false;
            $('#measure-button').css('background-color', '#17a2b8').css('color', 'white').text('📏 Mesurer une distance');
            $('.leaflet-container').css('cursor', '');
            pointsMesure = [];
        }
    });
});