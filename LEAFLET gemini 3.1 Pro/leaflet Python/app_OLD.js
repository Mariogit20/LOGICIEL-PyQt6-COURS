$(document).ready(function() {
    var map = L.map('map').setView([46.603354, 1.888334], 6);

    // Couches (avec crossOrigin: true pour la capture)
    var coucheCroquis = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors',
        crossOrigin: true 
    });

    var instanceId = 'VOTRE_INSTANCE_ID'; // <--- REMPLACEZ CECI PAR VOTRE ID SENTINEL HUB
    var urlSentinel = 'https://services.sentinel-hub.com/ogc/wms/' + instanceId;
    
    var coucheSentinelRecent = L.tileLayer.wms(urlSentinel, {
        layers: 'TRUE-COLOR-S2L2A',
        format: 'image/jpeg',
        transparent: false,
        maxZoom: 16,
        attribution: '© Copernicus',
        crossOrigin: true
    });

    coucheSentinelRecent.addTo(map);

    var baseMaps = {
        "IMAGE SATELLITE (Récente)": coucheSentinelRecent,
        "IMAGE CROQUIS": coucheCroquis
    };
    L.control.layers(baseMaps).addTo(map);

    // Légende
    var legend = L.control({position: 'bottomright'});
    legend.onAdd = function () {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML += '<h4>Légende</h4>';
        div.innerHTML += '<i class="legend-color" style="background: #a3ccff"></i> Eau<br>';
        div.innerHTML += '<i class="legend-color" style="background: #c2e699"></i> Végétation<br>';
        div.innerHTML += '<i class="legend-color" style="background: #e0e0e0"></i> Zones Urbaines<br>';
        return div;
    };
    legend.addTo(map);

    // Affichage des coordonnées GPS
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

    map.on('move', function() {
        coordsControl.update(map.getCenter());
    });

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
                        map.flyTo([lat, lon], 13, { duration: 2 });
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
            link.download = 'capture_satellite.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
            btn.text(texteOriginal);
        }).catch(err => {
            console.error(err);
            alert("Erreur lors de la capture.");
            btn.text(texteOriginal);
        });
    });

    // --- OUTIL DE MESURE DE DISTANCE ---
    var isMeasuring = false;
    var measureLayer = L.featureGroup().addTo(map); // Groupe pour contenir les lignes de mesure
    var pointsMesure = [];

    $('#measure-button').click(function() {
        isMeasuring = !isMeasuring;
        
        if (isMeasuring) {
            // Mode mesure activé
            $(this).css('background-color', '#ffc107').css('color', 'black').text('Annuler la mesure');
            $('.leaflet-container').css('cursor', 'crosshair'); // Change le curseur
            measureLayer.clearLayers(); // Efface l'ancienne mesure
            pointsMesure = [];
        } else {
            // Mode mesure désactivé
            $(this).css('background-color', '#17a2b8').css('color', 'white').text('📏 Mesurer une distance');
            $('.leaflet-container').css('cursor', ''); // Restaure le curseur normal
            measureLayer.clearLayers();
        }
    });

    map.on('click', function(e) {
        if (!isMeasuring) return;

        // Ajoute le point cliqué à notre liste
        pointsMesure.push(e.latlng);
        
        // Ajoute un petit cercle rouge là où l'utilisateur a cliqué
        L.circleMarker(e.latlng, { color: 'red', radius: 5 }).addTo(measureLayer);

        // Si on a cliqué sur 2 points, on trace la ligne et on calcule
        if (pointsMesure.length === 2) {
            // Dessine la ligne entre les deux points
            var polyline = L.polyline(pointsMesure, {color: 'red', weight: 4}).addTo(measureLayer);
            
            // Calcule la distance physique (en mètres)
            var distanceMetres = map.distance(pointsMesure[0], pointsMesure[1]);
            var distanceKm = (distanceMetres / 1000).toFixed(2); // Convertit en km
            
            // Affiche le résultat sur la ligne
            polyline.bindPopup("<b>Distance :</b> " + distanceKm + " km").openPopup();
            
            // Réinitialise l'outil pour la prochaine fois
            isMeasuring = false;
            $('#measure-button').css('background-color', '#17a2b8').css('color', 'white').text('📏 Mesurer une distance');
            $('.leaflet-container').css('cursor', '');
            pointsMesure = [];
        }
    });
});