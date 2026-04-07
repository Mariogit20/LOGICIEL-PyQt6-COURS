$(document).ready(function() {
    // 1. Initialisation de la carte (Centrée sur la France par défaut)
    var map = L.map('map').setView([46.603354, 1.888334], 5);

    // 2. Définition des couches de fond
    var coucheCroquis = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    });

    var coucheSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19,
        attribution: 'Tiles © Esri'
    });

    // 3. Application de la couche satellite par défaut
    coucheSatellite.addTo(map);

    // 4. Création du contrôleur pour choisir entre les deux images
    var baseMaps = {
        "IMAGE PAR SATELITE": coucheSatellite,
        "IMAGE CROQUIS": coucheCroquis
    };
    L.control.layers(baseMaps).addTo(map);

    // 5. Ajout d'une légende en bas à droite
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML += '<h4>Légende</h4>';
        div.innerHTML += '<i class="legend-color" style="background: #a3ccff"></i> Eau<br>';
        div.innerHTML += '<i class="legend-color" style="background: #c2e699"></i> Végétation<br>';
        div.innerHTML += '<i class="legend-color" style="background: #e0e0e0"></i> Zones Urbaines<br>';
        return div;
    };
    legend.addTo(map);

    // 6. Fonctionnalité de recherche
    var searchMarker; // Garde la trace du marqueur actuel

    function lancerRecherche() {
        var query = $('#search-input').val();
        
        if (query.trim() !== '') {
            // Requête AJAX vers Nominatim
            $.ajax({
                url: 'https://nominatim.openstreetmap.org/search',
                type: 'GET',
                data: {
                    format: 'json',
                    q: query,
                    limit: 1 // On prend le résultat le plus pertinent
                },
                success: function(data) {
                    if (data && data.length > 0) {
                        var result = data[0];
                        var lat = result.lat;
                        var lon = result.lon;

                        // Animation vers la destination
                        map.flyTo([lat, lon], 13, {
                            duration: 2
                        });

                        // Supprime l'ancien marqueur s'il existe
                        if (searchMarker) {
                            map.removeLayer(searchMarker);
                        }

                        // Ajoute le nouveau marqueur
                        searchMarker = L.marker([lat, lon]).addTo(map)
                            .bindPopup('<b>Résultat :</b><br>' + result.display_name)
                            .openPopup();
                    } else {
                        alert("Lieu introuvable. Essayez avec un autre nom.");
                    }
                },
                error: function() {
                    alert("Erreur de connexion au service de recherche.");
                }
            });
        }
    }

    // Lancer la recherche au clic
    $('#search-button').click(function() {
        lancerRecherche();
    });

    // Lancer la recherche avec la touche "Entrée"
    $('#search-input').keypress(function(e) {
        if (e.which == 13) { 
            lancerRecherche();
        }
    });
});