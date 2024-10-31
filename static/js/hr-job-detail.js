document.addEventListener('DOMContentLoaded', function() {
    const jobForm = document.getElementById('jobForm');
    const jobId = window.location.pathname.split('/').pop();
    
    jobForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            title: document.getElementById('title').value,
            location: document.getElementById('location').value,
            description: document.getElementById('description').value,
            requirements: document.getElementById('requirements').value,
            status: document.getElementById('status').value
        };
        
        const url = jobId === 'new' ? '/api/hr/jobs' : `/api/hr/jobs/${jobId}`;
        const method = jobId === 'new' ? 'POST' : 'PUT';
        
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                window.location.href = '/hr/jobs';  // Correct redirect URL
            }
        } catch (error) {
            console.error('Error saving job:', error);
        }
    });
});