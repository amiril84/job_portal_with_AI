document.addEventListener('DOMContentLoaded', function() {
    fetchCandidates();
    setupSorting();
});

async function fetchCandidates() {
    try {
        const response = await fetch('/api/hr/candidates');
        const candidates = await response.json();
        displayCandidates(candidates);
    } catch (error) {
        console.error('Error fetching candidates:', error);
    }
}

function displayCandidates(candidates) {
    const tableBody = document.getElementById('candidateTableBody');
    tableBody.innerHTML = '';
    
    candidates.forEach(candidate => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${candidate.full_name}</td>
            <td>${candidate.email}</td>
            <td>${candidate.job_title}</td>
            <td>${candidate.score}</td>
            <td><a href="/download-cv/${candidate.id}" class="btn btn-download">Download CV</a></td>
            <td>${candidate.evaluation}</td>
            <td>
                <button onclick="shortlistCandidate(${candidate.id})" class="btn btn-shortlist">
                    Shortlist
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
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

async function shortlistCandidate(candidateId) {
    try {
        const response = await fetch(`/api/hr/shortlist/${candidateId}`, {
            method: 'POST'
        });
        if (response.ok) {
            fetchCandidates();
        }
    } catch (error) {
        console.error('Error shortlisting candidate:', error);
    }
}

document.getElementById('exportExcel').addEventListener('click', async function() {
    try {
        const response = await fetch('/api/hr/export-candidates');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'candidates.xlsx';
        a.click();
    } catch (error) {
        console.error('Error exporting to Excel:', error);
    }
});