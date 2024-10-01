$(document).ready(function() {
    var REFRESH_INTERVAL = 500;

    // Reformatage du contenu des balises <pre> dans les modales pour les rendre plus lisibles
    $('.modal-body pre').each(function() {
        let rawContent = $(this).text();
        let beautifiedContent = js_beautify(rawContent);
        let trimmedContent = beautifiedContent.replace(/^\s+/gm, '');
        $(this).text(trimmedContent);
    });

    // Charger les données CPU et RAM depuis localStorage ou initialiser des tableaux vides
    var cpuMhzData = JSON.parse(localStorage.getItem('cpuMhzData')) || [];
    var ramData = JSON.parse(localStorage.getItem('ramData')) || [];
    var timeLabels = JSON.parse(localStorage.getItem('timeLabels')) || [];

    // Limiter les données à 50 points (pour des raisons de performance)
    if (cpuMhzData.length > 50) {
        cpuMhzData = cpuMhzData.slice(-50);
        timeLabels = timeLabels.slice(-50);
    }
    if (ramData.length > 50) {
        ramData = ramData.slice(-50);
    }

    // Configuration du graphique CPU MHz
    var ctxCpu = document.getElementById('cpuMhzChart').getContext('2d');
    var cpuMhzChart = new Chart(ctxCpu, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'CPU Usage (MHz)',
                data: cpuMhzData,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'realtime',
                    realtime: {
                        delay: REFRESH_INTERVAL,
                        refresh: REFRESH_INTERVAL,
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Configuration du graphique RAM
    var ctxRam = document.getElementById('ramChart').getContext('2d');
    var ramChart = new Chart(ctxRam, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'RAM Usage (MB)',
                data: ramData,
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'realtime',
                    realtime: {
                        delay: REFRESH_INTERVAL,
                        refresh: REFRESH_INTERVAL,
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });

    // Fonction pour calculer la moyenne
    function calculateAverage(data) {
        if (data.length === 0) return 0;
        const sum = data.reduce((a, b) => a + b, 0);
        return (sum / data.length).toFixed(2);
    }

    // Générer des données aléatoires pour la RAM
    function generateRandomRam() {
        return Math.floor(Math.random() * 8000) + 2000;
    }

    function updateProgressBars(cpuPercentage, ramPercentage) {
        // Mise à jour de la barre de progression du CPU moyen
        $('.progress-bar.cpu').css('width', cpuPercentage + '%')
        .attr('aria-valuenow', cpuPercentage).text(cpuPercentage + '%');
        
        // Mise à jour de la barre de progression de la RAM moyenne
        $('.progress-bar.ram').css('width', ramPercentage + '%')
        .attr('aria-valuenow', ramPercentage).text(ramPercentage + '%');
    }

    function refreshData() {
        fetch('/host_informations')
            .then(response => response.json())
            .then(data => {
                // Mise à jour des éléments du DOM
                $('#hostname').text(data.hostname);
                $('#libvirt_version').text(data.libvirt_version);
                $('#uri').text(data.uri);
                $('#cpu_model').text(data.cpu_model);
                $('#total_memory_size').text(data.total_memory_size);
                $('#number_of_cpus').text(data.number_of_cpus);
                $('#cpu_mhz').text(data.cpu_mhz);
                $('#number_of_nodes').text(data.number_of_nodes);
                $('#number_of_sockets').text(data.number_of_sockets);
                $('#number_of_cores_per_socket').text(data.number_of_cores_per_socket);
                $('#number_of_threads_per_core').text(data.number_of_threads_per_core);
                $('#max_vcpus').text(data.max_vcpus);

                // Ajouter les nouvelles données du CPU au tableau
                var currentTime = new Date().toLocaleTimeString();
                timeLabels.push(currentTime);
                cpuMhzData.push(data.cpu_mhz);

                // Générer des valeurs aléatoires pour la RAM
                var ramUsage = generateRandomRam();
                ramData.push(ramUsage);

                // Limiter le nombre de points de données visibles (histoire que ça soit visible)
                if (cpuMhzData.length > 50) {
                    timeLabels.shift();
                    cpuMhzData.shift();
                }
                if (ramData.length > 50) {
                    ramData.shift();
                }

                // Sauvegarder les données dans localStorage
                localStorage.setItem('cpuMhzData', JSON.stringify(cpuMhzData));
                localStorage.setItem('ramData', JSON.stringify(ramData));
                localStorage.setItem('timeLabels', JSON.stringify(timeLabels));

                // Calculer la moyenne et mettre à jour l'affichage
                var averageCpuMhz = calculateAverage(cpuMhzData);
                var averageRam = calculateAverage(ramData);
                $('#cpuMhzAverage').text(averageCpuMhz + " MHz");
                $('#ramAverage').text(averageRam + " MB");

                // Calcul des pourcentages d'utilisation CPU et RAM
                var cpuPercentage = Math.min(Math.round((averageCpuMhz / 5000) * 100), 100); // Utilisation réelle du CPU en pourcentage
                var ramPercentage = Math.min(Math.round((averageRam / data.total_memory_size) * 100), 100);  // Pourcentage RAM
    
                // Mettre à jour les barres de progression
                updateProgressBars(cpuPercentage, ramPercentage);

                // Mettre à jour les graphiques
                cpuMhzChart.update();
                ramChart.update();

                // Beautification des données JSON et refresh de la modal
                var rawContent = JSON.stringify(data, null, 4);  
                $('#hostInfoRaw pre').text(rawContent);
            })
            .catch(error => console.error('Error:', error));
    }

    // Actualiser les données automatiquement
    setInterval(refreshData, REFRESH_INTERVAL);
});
