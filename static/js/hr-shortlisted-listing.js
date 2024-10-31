document.addEventListener('DOMContentLoaded', function() {
    fetchShortlistedCandidates();
    setupSorting();
});

async function fetchShortlistedCandidates() {
    try {
        const response = await fetch('/api/hr/shortlisted/list');
        const candidates = await response.json();
        console.log('Fetched candidates:', candidates);
        displayShortlistedCandidates(candidates);
    } catch (error) {
        console.error('Error fetching shortlisted candidates:', error);
    }
}

function displayShortlistedCandidates(candidates) {
    const tableBody = document.getElementById('shortlistedTableBody');
    tableBody.innerHTML = '';
    
    candidates.forEach(candidate => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${candidate.full_name}</td>
            <td>${candidate.email}</td>
            <td>${candidate.job_title}</td>
            <td>${candidate.score}</td>
            <td><a href="/download-cv/${candidate.id}" class="btn btn-download">Download CV</a></td>
            <td>
                <button onclick="excludeFromShortlist(${candidate.id})" class="btn btn-warning">
                    Exclude from Shortlist
                </button>
            </td>
            <td>${candidate.evaluation}</td>
            <td>
                <button onclick="removeFromShortlist(${candidate.id})" class="btn btn-remove">
                    Remove
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

async function excludeFromShortlist(candidateId) {
    if (!confirm('Are you sure you want to exclude this candidate from the shortlist?')) return;
    
    try {
        const response = await fetch(`/api/hr/exclude-shortlist/${candidateId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            // Refresh the shortlisted candidates table
            fetchShortlistedCandidates();
        }
    } catch (error) {
        console.error('Error excluding from shortlist:', error);
    }
}
async function removeFromShortlist(candidateId) {
    if (!confirm('Are you sure you want to remove this candidate from the shortlist?')) return;
    
    try {
        const response = await fetch(`/api/hr/remove-shortlist/${candidateId}`, {
            method: 'POST'
        });
        if (response.ok) {
            fetchShortlistedCandidates();
        }
    } catch (error) {
        console.error('Error removing from shortlist:', error);
    }
}

function setupSorting() {
    const headers = document.querySelectorAll('th[data-sort]');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.sort;
            sortTable(column);
        });
    });
}

function sortTable(column) {
    const tbody = document.getElementById('shortlistedTableBody');
    const rows = Array.from(tbody.getElementsByTagName('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.querySelector(`td:nth-child(${getColumnIndex(column)})`).textContent;
        const bValue = b.querySelector(`td:nth-child(${getColumnIndex(column)})`).textContent;
        
        if (column === 'score') {
            return parseFloat(bValue) - parseFloat(aValue);
        }
        return aValue.localeCompare(bValue);
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

function getColumnIndex(column) {
    const columns = {
        'name': 1,
        'email': 2,
        'job': 3,
        'score': 4
    };
    return columns[column];
}

document.getElementById('exportExcel').addEventListener('click', async function() {
    try {
        const response = await fetch('/api/hr/export-excel?shortlisted=true');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'shortlisted_candidates.xlsx';
        a.click();
    } catch (error) {
        console.error('Error exporting to Excel:', error);
    }
});