from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///algora.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True, cascade='all, delete-orphan')
    quiz_responses = db.relationship('QuizResponse', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    class_level = db.Column(db.Integer, nullable=False)  # 11 or 12
    icon = db.Column(db.String(50))  # emoji or icon name
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    resources = db.relationship('Resource', backref='chapter', lazy=True, cascade='all, delete-orphan')
    quiz_questions = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Chapter {self.name}>'

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # notes, pyq, video, important_questions
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text)  # For text content or URLs
    file_path = db.Column(db.String(255))  # For uploaded files
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resource {self.title}>'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    explanation = db.Column(db.Text)
    responses = db.relationship('QuizResponse', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz {self.question[:50]}...>'

class QuizResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    selected_answer = db.Column(db.String(1))
    is_correct = db.Column(db.Boolean)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    resource = db.relationship('Resource', backref='bookmarks')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== DECORATORS ====================

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROUTES ====================

# HOME PAGE
@app.route('/')
def home():
    subjects_11 = Subject.query.filter_by(class_level=11).all()
    subjects_12 = Subject.query.filter_by(class_level=12).all()
    return render_template('home.html', subjects_11=subjects_11, subjects_12=subjects_12)

# AUTHENTICATION ROUTES
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# DASHBOARD ROUTES
@app.route('/dashboard')
@login_required
def dashboard():
    subjects_11 = Subject.query.filter_by(class_level=11).all()
    subjects_12 = Subject.query.filter_by(class_level=12).all()
    return render_template('dashboard.html', subjects_11=subjects_11, subjects_12=subjects_12)

@app.route('/class/<int:class_level>')
@login_required
def view_class(class_level):
    if class_level not in [11, 12]:
        flash('Invalid class level.', 'danger')
        return redirect(url_for('dashboard'))
    
    subjects = Subject.query.filter_by(class_level=class_level).all()
    return render_template('class.html', class_level=class_level, subjects=subjects)

@app.route('/subject/<int:subject_id>')
@login_required
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).order_by(Chapter.order).all()
    return render_template('subject.html', subject=subject, chapters=chapters)

@app.route('/chapter/<int:chapter_id>')
@login_required
def view_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    resources = Resource.query.filter_by(chapter_id=chapter_id).all()
    quiz_questions = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    # Get user's bookmarks for this chapter's resources
    bookmarked_ids = set()
    if current_user.is_authenticated:
        bookmarked_ids = {b.resource_id for b in Bookmark.query.filter_by(user_id=current_user.id).all()}
    
    return render_template('chapter.html', chapter=chapter, resources=resources, quiz_questions=quiz_questions, bookmarked_ids=bookmarked_ids)

# RESOURCE ROUTES
@app.route('/download/<int:resource_id>')
@login_required
def download_resource(resource_id):
    from flask import send_file
    resource = Resource.query.get_or_404(resource_id)
    
    if not resource.file_path or not os.path.exists(resource.file_path):
        flash('File not found.', 'danger')
        return redirect(url_for('view_chapter', chapter_id=resource.chapter_id))
    
    return send_file(resource.file_path, as_attachment=True, download_name=secure_filename(resource.title))

@app.route('/bookmark/<int:resource_id>', methods=['POST'])
@login_required
def toggle_bookmark(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, resource_id=resource_id).first()
    
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({'status': 'removed', 'message': 'Bookmark removed'}), 200
    else:
        bookmark = Bookmark(user_id=current_user.id, resource_id=resource_id)
        db.session.add(bookmark)
        db.session.commit()
        return jsonify({'status': 'added', 'message': 'Bookmark added'}), 200

@app.route('/bookmarks')
@login_required
def view_bookmarks():
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    resources = [b.resource for b in bookmarks]
    return render_template('bookmarks.html', resources=resources)

# QUIZ ROUTES
@app.route('/quiz/<int:chapter_id>')
@login_required
def take_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quiz_questions = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    if not quiz_questions:
        flash('No quiz questions available for this chapter.', 'info')
        return redirect(url_for('view_chapter', chapter_id=chapter_id))
    
    return render_template('quiz.html', chapter=chapter, quiz_questions=quiz_questions)

@app.route('/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    data = request.get_json()
    chapter_id = data.get('chapter_id')
    answers = data.get('answers', {})
    
    correct_count = 0
    total_count = len(answers)
    
    for quiz_id, selected_answer in answers.items():
        quiz = Quiz.query.get(int(quiz_id))
        if quiz and quiz.chapter_id == int(chapter_id):
            is_correct = selected_answer.upper() == quiz.correct_answer.upper()
            
            response = QuizResponse(
                user_id=current_user.id,
                quiz_id=int(quiz_id),
                selected_answer=selected_answer.upper(),
                is_correct=is_correct
            )
            db.session.add(response)
            
            if is_correct:
                correct_count += 1
    
    db.session.commit()
    
    percentage = (correct_count / total_count * 100) if total_count > 0 else 0
    return jsonify({
        'correct': correct_count,
        'total': total_count,
        'percentage': round(percentage, 2)
    }), 200

# SEARCH ROUTE
@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return render_template('search.html', query=query, chapters=[], resources=[])
    
    chapters = Chapter.query.filter(Chapter.name.ilike(f'%{query}%')).all()
    resources = Resource.query.filter(Resource.title.ilike(f'%{query}%')).all()
    
    return render_template('search.html', query=query, chapters=chapters, resources=resources)

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    total_users = User.query.filter_by(is_admin=False).count()
    total_subjects = Subject.query.count()
    total_chapters = Chapter.query.count()
    total_resources = Resource.query.count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_subjects=total_subjects,
                         total_chapters=total_chapters,
                         total_resources=total_resources)

@app.route('/admin/subjects')
@admin_required
def admin_subjects():
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@app.route('/admin/subject/add', methods=['GET', 'POST'])
@admin_required
def admin_add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        class_level = request.form.get('class_level')
        icon = request.form.get('icon')
        
        subject = Subject(name=name, description=description, class_level=int(class_level), icon=icon)
        db.session.add(subject)
        db.session.commit()
        
        flash('Subject added successfully.', 'success')
        return redirect(url_for('admin_subjects'))
    
    return render_template('admin/subject_form.html', subject=None)

@app.route('/admin/subject/<int:subject_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        subject.name = request.form.get('name')
        subject.description = request.form.get('description')
        subject.class_level = int(request.form.get('class_level'))
        subject.icon = request.form.get('icon')
        db.session.commit()
        
        flash('Subject updated successfully.', 'success')
        return redirect(url_for('admin_subjects'))
    
    return render_template('admin/subject_form.html', subject=subject)

@app.route('/admin/subject/<int:subject_id>/delete', methods=['POST'])
@admin_required
def admin_delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    
    flash('Subject deleted successfully.', 'success')
    return redirect(url_for('admin_subjects'))

@app.route('/admin/chapters/<int:subject_id>')
@admin_required
def admin_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).order_by(Chapter.order).all()
    return render_template('admin/chapters.html', subject=subject, chapters=chapters)

@app.route('/admin/chapter/add/<int:subject_id>', methods=['GET', 'POST'])
@admin_required
def admin_add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        order = request.form.get('order', 0)
        
        chapter = Chapter(subject_id=subject_id, name=name, description=description, order=int(order))
        db.session.add(chapter)
        db.session.commit()
        
        flash('Chapter added successfully.', 'success')
        return redirect(url_for('admin_chapters', subject_id=subject_id))
    
    return render_template('admin/chapter_form.html', subject=subject, chapter=None)

@app.route('/admin/chapter/<int:chapter_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        chapter.name = request.form.get('name')
        chapter.description = request.form.get('description')
        chapter.order = int(request.form.get('order', 0))
        db.session.commit()
        
        flash('Chapter updated successfully.', 'success')
        return redirect(url_for('admin_chapters', subject_id=chapter.subject_id))
    
    return render_template('admin/chapter_form.html', subject=chapter.subject, chapter=chapter)

@app.route('/admin/chapter/<int:chapter_id>/delete', methods=['POST'])
@admin_required
def admin_delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id
    db.session.delete(chapter)
    db.session.commit()
    
    flash('Chapter deleted successfully.', 'success')
    return redirect(url_for('admin_chapters', subject_id=subject_id))

@app.route('/admin/resources/<int:chapter_id>')
@admin_required
def admin_resources(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    resources = Resource.query.filter_by(chapter_id=chapter_id).all()
    return render_template('admin/resources.html', chapter=chapter, resources=resources)

@app.route('/admin/resource/add/<int:chapter_id>', methods=['GET', 'POST'])
@admin_required
def admin_add_resource(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        resource_type = request.form.get('type')
        content = request.form.get('content')
        file = request.files.get('file')
        
        file_path = None
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        
        resource = Resource(
            chapter_id=chapter_id,
            type=resource_type,
            title=title,
            content=content,
            file_path=file_path
        )
        db.session.add(resource)
        db.session.commit()
        
        flash('Resource added successfully.', 'success')
        return redirect(url_for('admin_resources', chapter_id=chapter_id))
    
    return render_template('admin/resource_form.html', chapter=chapter, resource=None)

@app.route('/admin/resource/<int:resource_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    
    if request.method == 'POST':
        resource.title = request.form.get('title')
        resource.type = request.form.get('type')
        resource.content = request.form.get('content')
        
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            resource.file_path = file_path
        
        db.session.commit()
        flash('Resource updated successfully.', 'success')
        return redirect(url_for('admin_resources', chapter_id=resource.chapter_id))
    
    return render_template('admin/resource_form.html', chapter=resource.chapter, resource=resource)

@app.route('/admin/resource/<int:resource_id>/delete', methods=['POST'])
@admin_required
def admin_delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    chapter_id = resource.chapter_id
    db.session.delete(resource)
    db.session.commit()
    
    flash('Resource deleted successfully.', 'success')
    return redirect(url_for('admin_resources', chapter_id=chapter_id))

@app.route('/admin/quiz/<int:chapter_id>')
@admin_required
def admin_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quiz_questions = Quiz.query.filter_by(chapter_id=chapter_id).all()
    return render_template('admin/quiz.html', chapter=chapter, quiz_questions=quiz_questions)

@app.route('/admin/quiz/add/<int:chapter_id>', methods=['GET', 'POST'])
@admin_required
def admin_add_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        question = request.form.get('question')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_answer = request.form.get('correct_answer')
        explanation = request.form.get('explanation')
        
        quiz = Quiz(
            chapter_id=chapter_id,
            question=question,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            explanation=explanation
        )
        db.session.add(quiz)
        db.session.commit()
        
        flash('Quiz question added successfully.', 'success')
        return redirect(url_for('admin_quiz', chapter_id=chapter_id))
    
    return render_template('admin/quiz_form.html', chapter=chapter, quiz=None)

@app.route('/admin/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        quiz.question = request.form.get('question')
        quiz.option_a = request.form.get('option_a')
        quiz.option_b = request.form.get('option_b')
        quiz.option_c = request.form.get('option_c')
        quiz.option_d = request.form.get('option_d')
        quiz.correct_answer = request.form.get('correct_answer')
        quiz.explanation = request.form.get('explanation')
        db.session.commit()
        
        flash('Quiz question updated successfully.', 'success')
        return redirect(url_for('admin_quiz', chapter_id=quiz.chapter_id))
    
    return render_template('admin/quiz_form.html', chapter=quiz.chapter, quiz=quiz)

@app.route('/admin/quiz/<int:quiz_id>/delete', methods=['POST'])
@admin_required
def admin_delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id
    db.session.delete(quiz)
    db.session.commit()
    
    flash('Quiz question deleted successfully.', 'success')
    return redirect(url_for('admin_quiz', chapter_id=chapter_id))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin_users'))

# ERROR HANDLERS
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
