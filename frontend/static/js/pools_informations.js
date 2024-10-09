$(document).ready(function() {
    // Pool 1 - Récupérer les données à partir des attributs data-*
    var pool1 = $('[data-capacity]').first();
    var capacity1 = parseFloat(pool1.data('capacity'));
    var allocation1 = parseFloat(pool1.data('allocation'));
    var allocationPercentage1 = (allocation1 / capacity1) * 100;

    $("#allocationProgress1").css("width", allocationPercentage1 + "%").attr("aria-valuenow", allocationPercentage1);
    $("#allocationProgress1").css("background-color", "#7b2cbf"); 
    $("#allocationProgress1").text(allocationPercentage1.toFixed(2) + "%");
    $("#allocationProgress1").css("color", "white");

    var ctx1 = document.getElementById('capacityChart1').getContext('2d');
    var capacityChart1 = new Chart(ctx1, {
        type: 'doughnut',
        data: {
            labels: ['Capacité', 'Allocation'],
            datasets: [{
                label: 'MB',
                data: [capacity1, allocation1],
                backgroundColor: ['#7b2cbf', '#dec9e9'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            legend: {
                labels: {
                    fontColor: "white",
                    fontSize: 15
                }
            },
            rotation: -Math.PI / 2,
            circumference: Math.PI * 2,
            animation: {
                animateRotate: false,
                reverse: true
            }
        }
    });

    // Pool 2 - Récupérer les données à partir des attributs data-*
    var pool2 = $('[data-capacity]').last();
    var capacity2 = parseFloat(pool2.data('capacity'));
    var allocation2 = parseFloat(pool2.data('allocation'));
    var allocationPercentage2 = (allocation2 / capacity2) * 100;

    $("#allocationProgress2").css("width", allocationPercentage2 + "%").attr("aria-valuenow", allocationPercentage2);
    $("#allocationProgress2").css("background-color", "#7b2cbf");
    $("#allocationProgress2").text(allocationPercentage2.toFixed(2) + "%");
    $("#allocationProgress2").css("color", "white");

    var ctx2 = document.getElementById('capacityChart2').getContext('2d');
    var capacityChart2 = new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: ['Capacité', 'Allocation'],
            datasets: [{
                label: 'MB',
                data: [capacity2, allocation2],
                backgroundColor: ['#7b2cbf', '#dec9e9'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            legend: {
                labels: {
                    fontColor: "white",
                    fontSize: 15
                }
            },
            rotation: -Math.PI / 2,
            circumference: Math.PI * 2,
            animation: {
                animateRotate: false,
                reverse: true
            }
        }
    });

    // Reformatage du contenu des balises <pre> dans les modales pour les rendre plus lisibles
    $('.modal-body pre').each(function() {
        let rawContent = $(this).text();
        let beautifiedContent = js_beautify(rawContent);
        let trimmedContent = beautifiedContent.replace(/^\s+/gm, '');
        $(this).text(trimmedContent);
    });
});