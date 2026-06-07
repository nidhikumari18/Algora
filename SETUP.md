# ALGORA Setup & Configuration Guide

## Initial Setup

### Step 1: Database Initialization
```bash
python init_db.py
```

This will:
- Create SQLite database (`algora.db`)
- Create all tables
- Add admin user (username: `admin`, password: `admin123`)
- Add sample student user (username: `student1`, password: `student123`)
- Add 4 sample subjects for Class 11 and 12
- Add 2 sample chapters with resources and quizzes

### Step 2: Run Flask Application
```bash
python app.py
```

Visit: `http://localhost:5000`

## Configuration

### Change Admin Password (Important!)
1. Login as admin
2. In production, change the password immediately

### Database Configuration

Edit `app.py` to change database:

**SQLite (default):**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///algora.db'
```

**PostgreSQL:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/algora'
```

### File Upload Settings

```python
app.config['UPLOAD_FOLDER'] = 'uploads'  # Upload directory
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
```

## Adding Content

### Via Admin Panel

1. **Login as Admin**: `http://localhost:5000/admin`
2. **Add Subjects**: Go to Admin → Manage Subjects
3. **Add Chapters**: Click subject → Add Chapter
4. **Add Resources**: Click chapter → Add Resource
   - Upload PDFs for notes
   - Embed YouTube videos
   - Add text content
5. **Add Quiz**: Click chapter → Add Quiz Question

### Database Structure

**Creating a new subject:**
```python
from app import db, Subject

subject = Subject(
    name='Physics',
    description='Mechanics, Thermodynamics',
    class_level=11,
    icon='🔬'
)
db.session.add(subject)
db.session.commit()
```

## Customization

### Change Color Scheme

Edit `static/css/style.css` - `:root` variables:

```css
:root {
  --powder-blush: #fec5bbff;
  --almond-silk: #fcd5ceff;
  /* ... more colors ... */
}
```

### Change Logo/Branding

Edit `templates/base.html`:
```html
<a href="{{ url_for('home') }}" class="logo">🧬 ALGORA</a>
```

### Change Site Name

Edit `app.py`:
```python
app.title = 'ALGORA'
```

## Troubleshooting

### Database Lock Error
```bash
rm algora.db
python init_db.py
```

### Port Already in Use
```bash
python app.py --port 5001
```

### Module Import Error
```bash
pip install --upgrade -r requirements.txt
```

### File Upload Not Working
```bash
mkdir uploads
chmod 755 uploads
```

## Production Deployment

### Requirements
1. Change `SECRET_KEY` in `app.py`
2. Set `debug=False`
3. Use PostgreSQL
4. Set up environment variables
5. Use production server (Gunicorn, uWSGI)
6. Set up reverse proxy (Nginx, Apache)
7. Enable HTTPS/SSL

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name algora.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/algora/static;
    }
}
```

## Backup

### Database Backup
```bash
cp algora.db algora.db.backup
```

### Full Backup
```bash
tar -czf algora-backup.tar.gz .
```

## Performance Tips

1. **Enable Caching**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

2. **Database Indexing**
```python
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(150), index=True)
```

3. **Lazy Load Relations**
```python
chapters = Chapter.query.options(lazy=False).all()
```

## Monitoring

- Check logs: Look in console output
- Monitor uploads: Check `uploads/` folder
- Database size: `ls -lh algora.db`

## Support

For issues or questions, please open an issue on GitHub!
