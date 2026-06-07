# ALGORA Render Deployment Guide

## Step 1: Prepare Your Repository ✅
Your code is already pushed to GitHub!

## Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub account
3. Authorize Render to access your repositories

## Step 3: Create Web Service

### 3.1 Create New Web Service
- Click "New +" button → "Web Service"
- Select repository: `algora`
- Name: `algora` (or any name)
- Region: Choose closest to your users
- Runtime: `Python 3.9`

### 3.2 Build & Start Commands
- **Build Command:**
  ```
  pip install -r requirements.txt && python init_db.py
  ```

- **Start Command:**
  ```
  gunicorn app:app
  ```

### 3.3 Environment Variables
Click "Environment" and add:

```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here-change-this
```

**Generate secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3.4 Create PostgreSQL Database (Optional but Recommended)

1. Click "New +" → "PostgreSQL"
2. Name it: `algora-db`
3. Copy the **Internal Database URL**
4. In your Web Service, add environment variable:
   ```
   DATABASE_URL=postgresql://...(copy from database)
   ```

## Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Initialize database
   - Deploy your app
   - Give you a public URL

## Step 5: Access Your App

Your app will be live at: `https://algora.render.dev` (or similar)

Login with:
- **Username:** `admin`
- **Password:** `admin123`

## ⚠️ Important: Database Persistence

### SQLite (Current Setup - NOT Recommended for Production)
- Data is lost when dyno restarts
- Only for testing

### PostgreSQL (Recommended)
Add to Render:
1. Create PostgreSQL database
2. Get connection string
3. Add to environment variables as `DATABASE_URL`
4. Update `app.py` to use `DATABASE_URL`

## 🔧 Update app.py for Render

Replace the database config section with:

```python
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# Use DATABASE_URL if available (Render), else SQLite
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///algora.db'

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
```

## 📊 Monitoring

- **Logs:** Dashboard → "Logs" tab
- **Metrics:** View CPU, memory, requests
- **Environment:** Edit variables anytime

## 🆘 Troubleshooting

### Build Fails
- Check logs: Dashboard → "Logs" tab
- Ensure `requirements.txt` has all dependencies
- Make sure `Procfile` exists

### Database Not Initializing
- Check build command includes `python init_db.py`
- Or use PostgreSQL database instead

### App Crashes
- View logs for error messages
- Check environment variables are set
- Ensure `SECRET_KEY` is set

### Cold Starts (Free Tier)
- Free tier goes to sleep after 15 min inactivity
- Takes 30 seconds to wake up (acceptable for learning)
- Upgrade to paid for always-on

## 💰 Pricing

**Free Tier:**
- ✅ Web service hosting
- ✅ 750 compute hours/month
- ❌ PostgreSQL not included
- ❌ Goes to sleep after inactivity

**Paid Tier ($12.50/month):**
- ✅ Always on
- ✅ Priority support
- ✅ Included PostgreSQL database

## ✅ Deployment Checklist

- [ ] GitHub repo created and pushed
- [ ] Render account created
- [ ] Web Service created
- [ ] Build command: `pip install -r requirements.txt && python init_db.py`
- [ ] Start command: `gunicorn app:app`
- [ ] Environment variables added (SECRET_KEY, FLASK_ENV)
- [ ] PostgreSQL database created (optional)
- [ ] DATABASE_URL environment variable added (if using PostgreSQL)
- [ ] Deploy button clicked
- [ ] Wait 5-10 minutes for deployment
- [ ] Test at your Render URL

## 🎉 Success!

Once deployed, your ALGORA app will be live and accessible worldwide! 🚀

---

**Need help?** Check Render docs: https://render.com/docs
