// Smart Agriculture Advisory System - Farmer Module Actions

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Market Prices Filters
    initMarketPricesFilter();
});

// Dynamic Searching, Filtering, and Sorting of Market Prices Table
function initMarketPricesFilter() {
    const searchInput = document.getElementById('marketSearch');
    const cropFilter = document.getElementById('cropFilter');
    const marketFilter = document.getElementById('marketFilter');
    const tableBody = document.getElementById('marketTableBody');
    
    if (!tableBody) return; // Exit if not on market prices page

    const rows = Array.from(tableBody.querySelectorAll('tr'));

    // Apply Filter & Search combined
    function applyFilters() {
        const query = searchInput.value.toLowerCase().trim();
        const selectedCrop = cropFilter.value;
        const selectedMarket = marketFilter.value;

        rows.forEach(row => {
            const cropName = row.dataset.crop;
            const marketName = row.dataset.market;
            const rowText = row.innerText.toLowerCase();

            const matchesSearch = rowText.includes(query);
            const matchesCrop = !selectedCrop || cropName === selectedCrop;
            const matchesMarket = !selectedMarket || marketName === selectedMarket;

            if (matchesSearch && matchesCrop && matchesMarket) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    if (searchInput) searchInput.addEventListener('input', applyFilters);
    if (cropFilter) cropFilter.addEventListener('change', applyFilters);
    if (marketFilter) marketFilter.addEventListener('change', applyFilters);

    // Sorting Logic
    const sortPriceBtn = document.getElementById('sortPrice');
    let sortAscending = true;

    if (sortPriceBtn) {
        sortPriceBtn.addEventListener('click', () => {
            sortAscending = !sortAscending;
            
            // Toggle icon
            const icon = sortPriceBtn.querySelector('i');
            if (icon) {
                icon.className = sortAscending ? 'fas fa-sort-amount-down-alt' : 'fas fa-sort-amount-up';
            }

            const visibleRows = rows.filter(r => r.style.display !== 'none');
            const hiddenRows = rows.filter(r => r.style.display === 'none');

            visibleRows.sort((a, b) => {
                const valA = parseFloat(a.dataset.price);
                const valB = parseFloat(b.dataset.price);
                return sortAscending ? valA - valB : valB - valA;
            });

            // Re-render rows
            tableBody.innerHTML = '';
            visibleRows.forEach(r => tableBody.appendChild(r));
            hiddenRows.forEach(r => tableBody.appendChild(r));
        });
    }
}
