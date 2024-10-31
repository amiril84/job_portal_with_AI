from app import app, db
from extensions import db
from models.job import Job

def init_jobs():
    jobs = [
        {
            'title': 'Software Engineer',
            'location': 'San Francisco, CA',
            'description': 'We are seeking a skilled Software Engineer to join our development team. The ideal candidate will have strong programming skills and experience in building scalable applications.',
            'requirements': '''
                - Bachelor's degree in Computer Science or related field
                - 3+ years experience in software development
                - Proficiency in Python, JavaScript, and SQL
                - Experience with web frameworks (Flask, Django, or similar)
                - Strong problem-solving and analytical skills
                - Experience with version control systems (Git)
            ''',
            'summary': 'Full-time position for an experienced software developer with strong programming skills',
            'status': 'Active'
        },
        {
            'title': 'Chef',
            'location': 'New York, NY',
            'description': 'Looking for an experienced Chef to lead our kitchen team. The successful candidate will be responsible for menu planning, food preparation, and kitchen management.',
            'requirements': '''
                - Culinary degree or equivalent experience
                - 5+ years experience in professional kitchen
                - Strong leadership and team management skills
                - Knowledge of food safety regulations
                - Menu planning and cost control expertise
                - Ability to work in fast-paced environment
            ''',
            'summary': 'Lead chef position for upscale restaurant with kitchen management responsibilities',
            'status': 'Active'
        },
        {
            'title': 'Finance Manager',
            'location': 'Chicago, IL',
            'description': 'Seeking a Finance Manager to oversee financial operations and strategy. The role involves financial planning, reporting, and team leadership.',
            'requirements': '''
                - MBA or related advanced degree
                - 7+ years of financial management experience
                - CPA certification preferred
                - Experience with financial modeling and analysis
                - Strong leadership and communication skills
                - Proficiency in financial software and Excel
            ''',
            'summary': 'Senior finance position overseeing company financial operations and strategy',
            'status': 'Active'
        },
        {
            'title': 'Nurse',
            'location': 'Boston, MA',
            'description': 'Join our healthcare team as a Registered Nurse. The position involves direct patient care and collaboration with healthcare professionals.',
            'requirements': '''
                - BSN degree required
                - Current RN license
                - 2+ years clinical experience
                - BLS and ACLS certification
                - Strong patient care and communication skills
                - Experience with electronic health records
            ''',
            'summary': 'Registered Nurse position in leading healthcare facility',
            'status': 'Active'
        },
        {
            'title': 'IT Program Manager',
            'location': 'Seattle, WA',
            'description': 'Leading IT projects and programs across the organization. The role requires both technical knowledge and project management expertise.',
            'requirements': '''
                - Bachelor's degree in IT or related field
                - PMP certification required
                - 8+ years IT project management experience
                - Strong technical background
                - Agile methodology expertise
                - Excellent stakeholder management skills
            ''',
            'summary': 'Senior IT role managing complex technical projects and programs',
            'status': 'Active'
        }
    ]

    for job_data in jobs:
        job = Job(**job_data)
        db.session.add(job)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_jobs()
        print("Job database initialized successfully!")