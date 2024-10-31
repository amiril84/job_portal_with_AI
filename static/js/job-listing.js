document.addEventListener('DOMContentLoaded', function() {
    fetchJobs();
});

async function fetchJobs() {
    try {
        const response = await fetch('/api/jobs');
        const jobs = await response.json();
        displayJobs(jobs);
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

function displayJobs(jobs) {
    const jobListings = document.getElementById('jobListings');
    
    jobs.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.className = 'job-card';
        
        jobCard.innerHTML = `
            <h2 class="job-title">${job.title}</h2>
            <p class="job-location">${job.location}</p>
            <p class="job-summary">${job.summary}</p>
            <span class="job-status status-${job.status.toLowerCase()}">
                ${job.status}
            </span>
            <a href="/job/${job.id}" class="btn">View Details</a>
        `;
        
        jobListings.appendChild(jobCard);
    });
}