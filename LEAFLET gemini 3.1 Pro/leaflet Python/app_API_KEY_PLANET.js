$(document).ready(function() {
    var map = L.map('map').setView([46.603354, 1.888334], 6);

    // VOTRE CLÉ API PLANET (À coller ici)
    //   var planetApiKey = 'VOTRE_CLE_API_PLANET_ICI'; 

    var planetApiKey = 'PLAK78a76744bb8b4c35a6d6d346fc278e45';        // https://insights.planet.com/account/#/settings

    // Couche par défaut (Croquis)
    var coucheCroquis = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap',
        crossOrigin: true 
    });

    var baseMaps = {
        "IMAGE CROQUIS": coucheCroquis
    };
    
    var layerControl = L.control.layers(baseMaps).addTo(map);

    // --- CONNEXION À L'API PLANET LABS ---
    // On requête l'API pour obtenir la mosaïque la plus récente de votre compte
    $.ajax({
        url: 'https://api.planet.com/basemaps/v1/mosaics',
        type: 'GET',
        headers: {
            // L'API Planet utilise l'authentification Basic avec la clé API comme nom d'utilisateur
            'Authorization': 'Basic ' + btoa(planetApiKey + ':')
        },
        success: function(response) {
            if (response.mosaics && response.mosaics.length > 0) {
                // On prend la première mosaïque renvoyée (souvent la globale la plus récente)
                var derniereMosaique = response.mosaics[0];
                
                // On construit l'URL pour Leaflet en ajoutant la clé API
                var tileUrl = derniereMosaique._links.tiles + '?api_key=' + planetApiKey;

                var couchePlanet = L.tileLayer(tileUrl, {
                    maxZoom: 18, // Planet permet un zoom beaucoup plus profond !
                    attribution: '© Planet Labs',
                    crossOrigin: true
                });

                // On l'ajoute à la carte et au menu
                couchePlanet.addTo(map);
                layerControl.addBaseLayer(couchePlanet, "IMAGE PLANET LABS (Haute Résiolution)");
            } else {
                console.warn("Aucune mosaïque trouvée sur ce compte Planet.");
                coucheCroquis.addTo(map); // Fallback sur le croquis
            }
        },
        error: function(err) {
            console.error("Erreur d'authentification Planet :", err);
            alert("Impossible de se connecter à Planet. Vérifiez votre clé API.");
            coucheCroquis.addTo(map);
        }
    });

    // --- LÉGENDE ET COORDONNÉES GPS ---
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
                        map.flyTo([lat, lon], 14, { duration: 2 });
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
            link.download = 'capture_planet.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
            btn.text(texteOriginal);
        }).catch(err => {
            console.error(err);
            btn.text(texteOriginal);
        });
    });

    // --- OUTIL DE MESURE DE DISTANCE ---
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