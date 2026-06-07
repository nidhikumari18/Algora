from app import app, db, User, Subject, Chapter, Resource, Quiz
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@algora.com'
        )
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.add(admin)
        
        # Create sample student user
        student = User(
            username='student1',
            email='student@algora.com'
        )
        student.set_password('student123')
        db.session.add(student)
        
        db.session.commit()
        
        # Create sample subjects for Class 11
        physics_11 = Subject(
            name='Physics',
            description='Mechanics, Thermodynamics, Waves & Oscillations',
            class_level=11,
            icon='🔬'
        )
        chemistry_11 = Subject(
            name='Chemistry',
            description='Atomic Structure, Bonding, Redox Reactions',
            class_level=11,
            icon='⚗️'
        )
        maths_11 = Subject(
            name='Mathematics',
            description='Algebra, Calculus, Trigonometry',
            class_level=11,
            icon='📐'
        )
        biology_11 = Subject(
            name='Biology',
            description='Cell Biology, Genetics, Ecology',
            class_level=11,
            icon='🧬'
        )
        
        db.session.add_all([physics_11, chemistry_11, maths_11, biology_11])
        db.session.commit()
        
        # Create sample subjects for Class 12
        physics_12 = Subject(
            name='Physics',
            description='Electromagnetism, Modern Physics, Optics',
            class_level=12,
            icon='🔬'
        )
        chemistry_12 = Subject(
            name='Chemistry',
            description='Organic Chemistry, Coordination Compounds, Solutions',
            class_level=12,
            icon='⚗️'
        )
        maths_12 = Subject(
            name='Mathematics',
            description='Vectors, 3D Geometry, Probability',
            class_level=12,
            icon='📐'
        )
        biology_12 = Subject(
            name='Biology',
            description='Human Physiology, Plant Physiology, Evolution',
            class_level=12,
            icon='🧬'
        )
        
        db.session.add_all([physics_12, chemistry_12, maths_12, biology_12])
        db.session.commit()
        
        # Create sample chapters for Physics 11
        chapter1 = Chapter(
            subject_id=physics_11.id,
            name='Motion in One Dimension',
            description='Understanding displacement, velocity, and acceleration',
            order=1
        )
        chapter2 = Chapter(
            subject_id=physics_11.id,
            name='Forces and Newton\'s Laws',
            description='Newton\'s laws of motion and their applications',
            order=2
        )
        db.session.add_all([chapter1, chapter2])
        db.session.commit()
        
        # Create sample resources
        resource1 = Resource(
            chapter_id=chapter1.id,
            type='notes',
            title='Motion in One Dimension - Complete Notes',
            content='Comprehensive notes covering all concepts of motion in one dimension',
            file_path=None
        )
        resource2 = Resource(
            chapter_id=chapter1.id,
            type='video',
            title='Understanding Displacement and Velocity',
            content='https://www.youtube.com/embed/dQw4w9WgXcQ',
            file_path=None
        )
        resource3 = Resource(
            chapter_id=chapter1.id,
            type='important_questions',
            title='10 Important Questions on Motion',
            content='1. Define displacement...\n2. Difference between speed and velocity...\n3. Calculate average velocity from graph...',
            file_path=None
        )
        db.session.add_all([resource1, resource2, resource3])
        db.session.commit()
        
        # Create sample quiz questions
        quiz1 = Quiz(
            chapter_id=chapter1.id,
            question='A car travels 100 km in 2 hours. What is its average speed?',
            option_a='50 km/h',
            option_b='100 km/h',
            option_c='200 km/h',
            option_d='25 km/h',
            correct_answer='A',
            explanation='Average speed = Total distance / Total time = 100/2 = 50 km/h'
        )
        quiz2 = Quiz(
            chapter_id=chapter1.id,
            question='Which of the following is a vector quantity?',
            option_a='Speed',
            option_b='Distance',
            option_c='Displacement',
            option_d='Time',
            correct_answer='C',
            explanation='Displacement is a vector quantity as it has both magnitude and direction.'
        )
        db.session.add_all([quiz1, quiz2])
        db.session.commit()
        
        print('✅ Database initialized successfully!')
        print('📝 Admin credentials: username=admin, password=admin123')
        print('📝 Student credentials: username=student1, password=student123')

if __name__ == '__main__':
    init_database()
