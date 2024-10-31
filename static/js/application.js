document.getElementById('applicationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/api/submit-application', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Show success message with score and evaluation
            alert(`Application submitted successfully!\nScore: ${data.score}\n\nEvaluation: ${data.evaluation}`);
            window.location.href = '/thank-you';
        } else {
            alert(data.error || 'Failed to submit application');
        }
    } catch (error) {
        alert('Error submitting application. Please try again.');
    }
});