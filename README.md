# ALGORA - Educational Platform for Class 11-12 Science

🧬 A beautiful, modern, full-stack educational website for Class 11-12 Science students built with Flask, SQLite, and aesthetic pastel UI.

## 🎨 Features

✅ **Authentication System**
- Secure user signup/login with password hashing
- Session-based authentication
- Admin panel with special privileges

✅ **Learning Platform**
- Class 11 & 12 Science subjects (Physics, Chemistry, Maths, Biology)
- Organized study structure: Class → Subject → Chapter → Resources
- Multiple resource types: Notes, Videos, PYQs, Important Questions

✅ **Study Materials**
- PDF notes upload/download
- YouTube video embedding
- Important questions compilation
- Previous year questions (PYQs)

✅ **Interactive Features**
- MCQ-based quiz system with instant feedback
- Bookmark resources for quick access
- Search functionality across chapters and resources
- Progress tracking

✅ **Admin Dashboard**
- Manage subjects, chapters, and resources
- Add/edit/delete quiz questions
- User management
- Content statistics

✅ **Design**
- Soft pastel aesthetic with glassmorphism effects
- Smooth animations and hover transitions
- Fully responsive mobile-friendly UI
- Modern, clean, distraction-free interface

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Templates**: Jinja2
- **Security**: Werkzeug (password hashing)
- **Styling**: Custom CSS with pastel color scheme

## 📁 Project Structure

```
algora/
├── app.py                 # Main Flask application
├── init_db.py             # Database initialization with sample data
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with navbar/footer
│   ├── home.html         # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── subject.html      # Subject chapters view
│   ├── chapter.html      # Chapter resources view
│   ├── quiz.html         # Quiz interface
│   ├── bookmarks.html    # Bookmarked resources
│   ├── search.html       # Search results
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── subjects.html
│   │   ├── chapters.html
│   │   ├── resources.html
│   │   ├── quiz.html
│   │   └── users.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/
│   ├── css/
│   │   └── style.css     # Comprehensive styling
│   └── js/
│       └── script.js     # JavaScript functionality
├── uploads/              # Uploaded files (PDFs, etc.)
└── algora.db            # SQLite database
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nidhikumari18/algora.git
cd algora
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**
```bash
python init_db.py
```

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
```
http://localhost:5000
```

## 🔐 Demo Credentials

**Student Account:**
- Username: `student1`
- Password: `student123`

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## 📚 Database Models

### User
- id, username, email, password_hash, is_admin, created_at

### Subject
- id, name, description, class_level (11/12), icon

### Chapter
- id, subject_id, name, description, order

### Resource
- id, chapter_id, type (notes/video/pyq/important_questions), title, content, file_path, created_at

### Quiz
- id, chapter_id, question, option_a-d, correct_answer, explanation

### QuizResponse
- id, user_id, quiz_id, selected_answer, is_correct, attempted_at

### Bookmark
- id, user_id, resource_id, created_at

## 🎨 Design System

**Color Palette (Pastel Theme):**
- Powder Blush: `#fec5bb`
- Almond Silk: `#fcd5ce`
- Soft Blush: `#fae1dd`
- Seashell: `#f8edeb`
- Peach Glow: `#fec89a`

**UI Elements:**
- Rounded cards (16px-24px border-radius)
- Glassmorphism (blur effects)
- Smooth animations
- Minimal, clean design
- Notion + Pinterest style

## 🔄 API Routes

### Public Routes
- `GET /` - Home page
- `GET/POST /login` - User login
- `GET/POST /register` - User registration

### Authenticated Routes
- `GET /dashboard` - User dashboard
- `GET /class/<id>` - Class subjects
- `GET /subject/<id>` - Subject chapters
- `GET /chapter/<id>` - Chapter resources
- `GET/POST /quiz/<id>` - Quiz interface
- `POST /submit-quiz` - Submit quiz answers
- `GET /search` - Search resources
- `GET /bookmarks` - View bookmarks
- `POST /bookmark/<id>` - Toggle bookmark
- `GET /download/<id>` - Download resource
- `GET /logout` - Logout user

### Admin Routes
- `GET /admin` - Admin dashboard
- `GET/POST /admin/subjects` - Manage subjects
- `GET/POST /admin/chapters/<id>` - Manage chapters
- `GET/POST /admin/resources/<id>` - Manage resources
- `GET/POST /admin/quiz/<id>` - Manage quizzes
- `GET /admin/users` - Manage users

## 📝 Usage

### For Students
1. Sign up with username, email, and password
2. Choose Class 11 or 12 from dashboard
3. Select a subject to view chapters
4. Access study materials (notes, videos, questions)
5. Take quizzes to test knowledge
6. Bookmark important resources
7. Use search to find specific topics

### For Admins
1. Login with admin credentials
2. Go to Admin Panel
3. Manage subjects, chapters, resources
4. Add quiz questions with explanations
5. Upload PDFs and manage content
6. Monitor user accounts

## 🔒 Security Features

- ✅ Password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ CSRF protection (Flask-WTF ready)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Secure file uploads
- ✅ Admin-only access control

## 🚀 Deployment

### For Production
1. Change `SECRET_KEY` in `app.py`
2. Set `debug=False`
3. Use PostgreSQL instead of SQLite
4. Configure environment variables
5. Use Gunicorn or uWSGI
6. Set up reverse proxy (Nginx)

### Environment Variables
```
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your-secure-key
DATABASE_URL=postgresql://...
```

## 📱 Responsive Design

- Desktop: Full featured experience
- Tablet: Optimized grid layouts
- Mobile: Touch-friendly, single column
- All breakpoints: 480px, 768px, 1024px, 1400px

## 🎓 Future Enhancements

- [ ] Dark mode toggle
- [ ] Video upload instead of YouTube only
- [ ] Discussion forums
- [ ] Student progress analytics
- [ ] Push notifications
- [ ] Mobile app
- [ ] AI-powered recommendations
- [ ] Certificate generation
- [ ] Payment integration
- [ ] Live classes feature

## 🐛 Known Issues

None currently. Please report issues on GitHub!

## 📄 License

MIT License - feel free to use for educational purposes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📞 Support

For support, email: support@algora.edu or open an issue on GitHub

## 🎉 Credits

Built with ❤️ for Class 11-12 Science students

---

**Made by:** Nidhi Kumari
**GitHub:** https://github.com/nidhikumari18
