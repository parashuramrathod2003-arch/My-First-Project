// Smart Agriculture Advisory System - Admin Dashboard Actions

document.addEventListener('DOMContentLoaded', () => {
    // Delete validation warning handler
    setupDeleteConfirmations();
    
    // Initialize Dashboard/Report Visualizations
    initReportCharts();
});

function setupDeleteConfirmations() {
    document.querySelectorAll('.btn-delete-confirm').forEach(button => {
        button.addEventListener('click', (e) => {
            const confirmMsg = button.dataset.confirmMessage || 'Are you sure you want to delete this item? This action cannot be undone.';
            if (!confirm(confirmMsg)) {
                e.preventDefault();
            }
        });
    });
}

// Chart.js initialization for agricultural analytics report
function initReportCharts() {
    const cropChartCanvas = document.getElementById('cropSeasonChart');
    const ratingChartCanvas = document.getElementById('feedbackRatingChart');

    if (cropChartCanvas) {
        const ctx = cropChartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Kharif Season', 'Rabi Season', 'Year-round', 'Zaid/Summer'],
                datasets: [{
                    label: 'Crops Distribution',
                    data: [3, 1, 2, 0], // Sample data matching our database seed
                    backgroundColor: [
                        '#2e7d32', // Forest green
                        '#81c784', // Light green
                        '#ffb74d', // Orange
                        '#4fc3f7'  // Sky blue
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: getComputedStyle(document.body).getPropertyValue('--text-color').trim()
                        }
                    }
                }
            }
        });
    }

    if (ratingChartCanvas) {
        const ctx = ratingChartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['5 Star', '4 Star', '3 Star', '2 Star', '1 Star'],
                datasets: [{
                    label: 'Number of Feedbacks',
                    data: [1, 1, 0, 0, 0], // Matching seed feedbacks
                    backgroundColor: '#4caf50',
                    borderRadius: 5,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: getComputedStyle(document.body).getPropertyValue('--text-color').trim()
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            color: getComputedStyle(document.body).getPropertyValue('--text-color').trim()
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}
