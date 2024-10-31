from extensions import db
from datetime import datetime

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    cv_path = db.Column(db.String(200), nullable=False)
    evaluation = db.Column(db.Text)
    score = db.Column(db.Float, default=0.0)
    is_shortlisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    job = db.relationship('Job', backref='applications')