document.addEventListener('DOMContentLoaded', function() {
    const jobId = window.location.pathname.split('/').pop();
    fetchJobDetails(jobId);
});

async function fetchJobDetails(jobId) {
    try {
        const response = await fetch(`/api/jobs/${jobId}`);
        const job = await response.json();
        displayJobDetails(job);
    } catch (error) {
        console.error('Error fetching job details:', error);
    }
}

function displayJobDetails(job) {
    const jobDetail = document.getElementById('jobDetail');
    const applyBtn = document.querySelector('.apply-btn');
    
    if (job.status !== 'Active') {
        applyBtn.disabled = true;
        applyBtn.textContent = 'Position Closed';
    }
}