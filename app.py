from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import string
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neighbourhood_reporter.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    photo_filename = db.Column(db.String(200))
    reporter_name = db.Column(db.String(100))
    reporter_email = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Pending')  # Pending, In Review, Resolved
    admin_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'location': self.location,
            'photo_filename': self.photo_filename,
            'reporter_name': self.reporter_name or 'Anonymous',
            'status': self.status,
            'admin_response': self.admin_response,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def generate_report_id():
    """Generate unique report ID like #RPT-0042"""
    num = random.randint(1000, 9999)
    return f"RPT-{num}"

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes - Public Pages
@app.route('/')
def index():
    """Home page"""
    total_reports = Report.query.count()
    resolved_reports = Report.query.filter_by(status='Resolved').count()
    pending_reports = Report.query.filter_by(status='Pending').count()
    
    return render_template('index.html', 
                         total_reports=total_reports,
                         resolved_reports=resolved_reports,
                         pending_reports=pending_reports)

@app.route('/report')
def report_page():
    """Report a problem page"""
    return render_template('report.html')

@app.route('/track')
def track_page():
    """Track report page"""
    return render_template('track.html')

@app.route('/reports')
def reports_page():
    """Browse all reports page"""
    return render_template('reports.html')

@app.route('/stats')
def stats_page():
    """Dashboard/Stats page"""
    return render_template('stats.html')

# Routes - API
@app.route('/api/submit-report', methods=['POST'])
def submit_report():
    """Submit a new report"""
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        reporter_name = request.form.get('reporter_name', '').strip() or None
        reporter_email = request.form.get('reporter_email', '').strip() or None
        
        # Validation
        if not all([title, description, category, location]):
            return jsonify({'success': False, 'message': 'Please fill all required fields'}), 400
        
        if len(title) < 5:
            return jsonify({'success': False, 'message': 'Title must be at least 5 characters'}), 400
        
        if len(description) < 10:
            return jsonify({'success': False, 'message': 'Description must be at least 10 characters'}), 400
        
        # Handle file upload
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo_filename = filename
        
        # Create report
        report_id = generate_report_id()
        
        # Make sure report_id is unique
        while Report.query.filter_by(report_id=report_id).first():
            report_id = generate_report_id()
        
        new_report = Report(
            report_id=report_id,
            title=title,
            description=description,
            category=category,
            location=location,
            photo_filename=photo_filename,
            reporter_name=reporter_name,
            reporter_email=reporter_email
        )
        
        db.session.add(new_report)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report submitted successfully!',
            'report_id': report_id
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/get-report/<report_id>', methods=['GET'])
def get_report(report_id):
    """Get specific report by ID"""
    report = Report.query.filter_by(report_id=report_id).first()
    
    if not report:
        return jsonify({'success': False, 'message': 'Report not found'}), 404
    
    return jsonify({
        'success': True,
        'data': report.to_dict()
    }), 200

@app.route('/api/get-all-reports', methods=['GET'])
def get_all_reports():
    """Get all reports with optional filters"""
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    location = request.args.get('location', '').strip()
    sort = request.args.get('sort', 'newest')  # newest or urgent
    
    query = Report.query
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if location:
        query = query.filter(Report.location.ilike(f'%{location}%'))
    
    if sort == 'newest':
        query = query.order_by(Report.created_at.desc())
    elif sort == 'urgent':
        # Urgent = Pending and created earlier
        query = query.filter_by(status='Pending').order_by(Report.created_at.asc())
    
    reports = query.all()
    
    return jsonify({
        'success': True,
        'data': [report.to_dict() for report in reports],
        'count': len(reports)
    }), 200

@app.route('/api/get-stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    total = Report.query.count()
    pending = Report.query.filter_by(status='Pending').count()
    in_review = Report.query.filter_by(status='In Review').count()
    resolved = Report.query.filter_by(status='Resolved').count()
    
    # Category breakdown
    categories = ['Road Damage', 'Streetlight', 'Water Supply', 'Garbage', 'Drainage', 'Other']
    category_stats = {}
    for cat in categories:
        category_stats[cat] = Report.query.filter_by(category=cat).count()
    
    # Recent reports (last 5)
    recent = Report.query.order_by(Report.created_at.desc()).limit(5).all()
    
    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'pending': pending,
            'in_review': in_review,
            'resolved': resolved,
            'category_stats': category_stats,
            'recent': [r.to_dict() for r in recent]
        }
    }), 200

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials'), 401
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html')

@app.route('/api/admin/get-all-reports', methods=['GET'])
def admin_get_all_reports():
    """Get all reports for admin (with auth)"""
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    reports = Report.query.order_by(Report.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [report.to_dict() for report in reports],
        'count': len(reports)
    }), 200

@app.route('/api/admin/update-report/<int:report_id>', methods=['PUT'])
def admin_update_report(report_id):
    """Update report status and add response"""
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            if data['status'] not in ['Pending', 'In Review', 'Resolved']:
                return jsonify({'success': False, 'message': 'Invalid status'}), 400
            report.status = data['status']
        
        if 'admin_response' in data:
            report.admin_response = data['admin_response']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report updated successfully',
            'data': report.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/delete-report/<int:report_id>', methods=['DELETE'])
def admin_delete_report(report_id):
    """Delete a report"""
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({'success': False, 'message': 'Report not found'}), 404
        
        # Delete photo if exists
        if report.photo_filename:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], report.photo_filename)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        db.session.delete(report)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Report deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# CLI command to create admin
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Admin': Admin, 'Report': Report}

@app.cli.command()
def create_admin():
    """Create an admin user"""
    username = input('Enter admin username: ')
    password = input('Enter admin password: ')
    
    if Admin.query.filter_by(username=username).first():
        print('Username already exists!')
        return
    
    admin = Admin(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f'Admin user "{username}" created successfully!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
