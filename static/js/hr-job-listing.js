document.addEventListener('DOMContentLoaded', function() {
    fetchHRJobs();
});

async function fetchHRJobs() {
    try {
        const response = await fetch('/api/hr/jobs');
        const jobs = await response.json();
        displayHRJobs(jobs);
    } catch (error) {
        console.error('Error fetching jobs:', error);
    }
}

function displayHRJobs(jobs) {
    const tableBody = document.getElementById('jobTableBody');
    tableBody.innerHTML = '';
    
    jobs.forEach(job => {
        tableBody.innerHTML += createJobRow(job);
    });
}

function createJobRow(job) {
    return `
        <tr>
            <td>${job.title}</td>
            <td>${job.location}</td>
            <td>${job.summary}</td>
            <td>${job.status}</td>
            <td>
                <a href="/hr/job/${job.id}" class="btn">Edit</a>
                <button onclick="deleteJob(${job.id})" class="btn btn-danger">Delete</button>
            </td>
        </tr>
    `;
}


async function deleteJob(jobId) {
    if (confirm('Are you sure you want to delete this job?')) {
        try {
            const response = await fetch(`/api/hr/jobs/${jobId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                alert('Job deleted successfully');
                // Refresh the job listing by calling fetchHRJobs instead of loadJobs
                fetchHRJobs();
            } else {
                alert('Failed to delete job');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error deleting job');
        }
    }
}

