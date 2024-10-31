from flask import Flask, send_file, render_template, request, jsonify, redirect, url_for
from models import db, Job, JobApplication
from werkzeug.utils import secure_filename
import os
import PyPDF2
import pandas as pd
import io
from models.job import Job
from models.job_application import JobApplication
from extensions import db
from datetime import datetime
from utils.cv_processor import CVProcessor
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

db.init_app(app)

with app.app_context():
    db.create_all()

cv_processor = CVProcessor()

# Add this near the top of app.py with other configurations
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_score_from_evaluation(evaluation):
    # Extract numerical score from Claude's evaluation
    try:
        score_line = [line for line in evaluation.split('\n') if 'Score' in line][0]
        return float(score_line.split(':')[1].strip().split('/')[0])
    except:
        return 0.0
    



# Routes for candidate pages
@app.route('/')
def candidate_job_listing():
    return render_template('candidate/candidate_job_listing.html')

@app.route('/job/<int:job_id>')
def candidate_job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('candidate/candidate_job_detail.html', job=job)

@app.route('/apply/<int:job_id>')
def candidate_application(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('candidate/candidate_application.html', job=job)

@app.route('/submit-application', methods=['POST'])
def submit_application():
    if 'cv' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['cv']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('thank_you'))

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'location': job.location,
        'summary': job.summary,
        'status': job.status
    } for job in jobs])

@app.route('/api/applications', methods=['GET'])
def get_applications():
    applications = JobApplication.query.all()
    return jsonify([{
        'id': app.id,
        'full_name': app.full_name,
        'email': app.email,
        'job_title': app.job.title,
        'score': app.score,
        'evaluation': app.evaluation,
        'is_shortlisted': app.is_shortlisted
    } for app in applications])



# Routes for HR pages
@app.route('/hr/dashboard')
def hr_dashboard():
    return render_template('hr/hr_dashboard.html')

@app.route('/hr/candidates')
def hr_candidate_listing():
    return render_template('hr/hr_candidate_listing.html')

@app.route('/hr/shortlisted')
def hr_shortlisted_listing():
    shortlisted_candidates = JobApplication.query.filter_by(is_shortlisted=True).order_by(JobApplication.score.desc()).all()
    return render_template('hr/hr_shortlisted_listing.html', candidates=shortlisted_candidates)




@app.route('/hr/jobs')
def hr_job_listing():
    return render_template('hr/hr_job_listing.html')

@app.route('/hr/job/<job_id>', methods=['GET'])
def hr_job_detail(job_id):
    if job_id == 'new':
        job = None
    else:
        job = Job.query.get_or_404(int(job_id))
    return render_template('hr/hr_job_detail.html', job=job)

# Job-related endpoints
@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify({
        'id': job.id,
        'title': job.title,
        'location': job.location,
        'description': job.description,
        'status': job.status,
        'summary': job.summary
    })

@app.route('/api/hr/jobs', methods=['GET'])
def get_hr_jobs():
    jobs = Job.query.all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'location': job.location,
        'summary': job.summary,
        'status': job.status
    } for job in jobs])

@app.route('/api/hr/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted successfully'})

@app.route('/api/hr/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.json
    
    job.title = data['title']
    job.location = data['location']
    job.description = data['description']
    job.requirements = data['requirements']
    job.status = data['status']
    
    db.session.commit()
    return jsonify({'message': 'Job updated successfully'})

@app.route('/api/hr/jobs', methods=['POST'])
def create_job():
    data = request.json
    new_job = Job(
        title=data['title'],
        location=data['location'],
        description=data['description'],
        summary=data.get('summary', data['description'][:200]),  # Use description preview as fallback
        status='Active'
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'message': 'Job created successfully', 'id': new_job.id})

# Candidate-related endpoints
@app.route('/api/hr/candidates', methods=['GET'])
def get_candidates():
    candidates = JobApplication.query.order_by(JobApplication.score.desc()).all()
    return jsonify([{
        'id': c.id,
        'full_name': c.full_name,
        'email': c.email,
        'job_title': c.job.title,
        'score': c.score,
        'evaluation': c.evaluation,
        'is_shortlisted': c.is_shortlisted
    } for c in candidates])

@app.route('/api/hr/shortlist/<int:candidate_id>', methods=['POST'])
def shortlist_candidate(candidate_id):
    application = JobApplication.query.get_or_404(candidate_id)
    application.is_shortlisted = True
    db.session.commit()
    return jsonify({
        'message': 'Candidate shortlisted successfully',
        'candidate': {
            'id': application.id,
            'full_name': application.full_name,
            'email': application.email,
            'job_title': application.job.title,
            'score': application.score,
            'evaluation': application.evaluation,
            'is_shortlisted': application.is_shortlisted
        }
    })

@app.route('/download-cv/<int:candidate_id>')
def download_cv(candidate_id):
    application = JobApplication.query.get_or_404(candidate_id)
    return send_file(application.cv_path, as_attachment=True)

@app.route('/api/hr/candidates/export')
def export_candidates():
    # Get export type from query parameter
    export_type = request.args.get('type', 'all')
    
    # Query based on export type
    if export_type == 'shortlisted':
        candidates = JobApplication.query.filter_by(is_shortlisted=True).order_by(JobApplication.score.desc()).all()
    else:
        candidates = JobApplication.query.filter_by(is_shortlisted=False).all()
    
    # Convert to DataFrame
    data = [{
        'Full Name': c.full_name,
        'Email': c.email,
        'Job Title': c.job.title,
        'Score': c.score,
        'Evaluation': c.evaluation
    } for c in candidates]
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    
    output.seek(0)
    
    filename = 'shortlisted_candidates.xlsx' if export_type == 'shortlisted' else 'candidates.xlsx'
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/submit-application', methods=['POST'])
def api_submit_application():
    if 'cv' not in request.files:
        return jsonify({'error': 'CV file is required'}), 400
    
    file = request.files['cv']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a PDF'}), 400

    job_id = request.form.get('job_id')
    if not job_id:
        return jsonify({'error': 'Job ID is required'}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        job = db.session.get(Job, job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        cv_text = cv_processor.extract_text_from_pdf(file_path)
        evaluation_result = cv_processor.evaluate_cv(cv_text, job)
        score = cv_processor.extract_score(evaluation_result)
        
        new_application = JobApplication(
            job_id=job.id,
            full_name=request.form.get('fullName'),
            email=request.form.get('email'),
            cv_path=file_path,
            evaluation=evaluation_result,
            score=score
        )
        
        db.session.add(new_application)
        db.session.commit()
        
        return redirect(url_for('thank_you'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/hr/exclude-shortlist/<int:candidate_id>', methods=['POST'])
def exclude_from_shortlist(candidate_id):
    application = JobApplication.query.get_or_404(candidate_id)
    application.is_shortlisted = False
    db.session.commit()
    return jsonify({'success': True})
    
@app.route('/thank-you')
def thank_you():
    return render_template('candidate/candidate_thank_you.html', job=None)

@app.route('/api/hr/shortlisted-candidates', methods=['GET'])
def get_shortlisted_candidates():
    candidates = JobApplication.query.filter_by(is_shortlisted=True).order_by(JobApplication.score.desc()).all()
    return jsonify([{
        'id': c.id,
        'full_name': c.full_name,
        'email': c.email,
        'job_title': c.job.title,
        'score': c.score,
        'evaluation': c.evaluation,
        'is_shortlisted': c.is_shortlisted
    } for c in candidates])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)




