# 🗺️ Nagrik Parivartan - Neighbourhood Problem Reporter

> **Aapki Samasya, Seedha Sarkaar Tak** | *Your concerns, Straight to the government*

A modern, production-ready web application for citizens to report neighborhood problems and government officials to manage and resolve them.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-blue)
![License](https://img.shields.io/badge/License-Open%20Source-green)

---

## ✨ Features

### 👤 For Citizens
- 📝 **Easy Reporting** - Simple form with title, description, category, location, and photo
- 🆔 **Unique Report ID** - Get immediate tracking ID (e.g., RPT-1234)
- 🔍 **Track Status** - Real-time tracking with timeline (Pending → In Review → Resolved)
- 📊 **Browse Reports** - View all community reports with filters
- 📈 **Statistics** - Beautiful dashboards showing problem distribution
- 🔔 **Notifications** - Get updates on your report status

### 🛠️ For Government
- 🔐 **Secure Admin Panel** - Protected by username/password authentication
- 📋 **Report Management** - View all submitted reports in organized dashboard
- ✏️ **Status Updates** - Change report status and add official responses
- 📸 **Evidence Review** - View citizen-submitted photos and evidence
- 📊 **Analytics** - Charts showing problem categories and resolution rates
- 🗑️ **Moderation** - Delete spam or invalid reports

---

## 🎯 Categories

The system supports reporting of:
- 🚧 **Road Damage** - Potholes, broken roads, pavements
- 💡 **Streetlight** - Non-functional lights, broken poles  
- 🚰 **Water Supply** - Leaks, supply issues
- 🗑️ **Garbage** - Waste, littering
- 🌊 **Drainage** - Blocked drains, water accumulation
- 🌳 **Other** - Any other neighborhood issues

---

## 🚀 Quick Start

### Windows Users
```bash
# Double-click setup.bat
setup.bat

# Then run
python app.py
```

### macOS/Linux Users
```bash
# Make script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Then run
python3 app.py
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create admin user
flask shell
> create_admin()
> exit()

# Run application
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 📁 Project Structure

```
Nagrik-Parivartan/
├── app.py                    # Main Flask application (600+ lines)
├── requirements.txt          # Python dependencies
├── SETUP_GUIDE.md           # Detailed setup instructions
├── README.md                # This file
├── setup.bat               # Windows quick setup
├── setup.sh                # macOS/Linux quick setup
├── uploads/                # User-uploaded photos (auto-created)
├── templates/              # HTML templates (8 files)
│   ├── index.html         # Home page with hero
│   ├── report.html        # Report submission form
│   ├── track.html         # Track report status
│   ├── reports.html       # Browse all reports
│   ├── stats.html         # Dashboard & statistics
│   ├── admin_login.html   # Admin login page
│   ├── admin_dashboard.html # Admin panel
│   ├── 404.html           # Error page
│   └── 500.html           # Error page
└── static/                # Static assets
    └── style.css          # Complete CSS (1500+ lines)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.8+ |
| **Framework** | Flask 2.3.3 |
| **ORM** | SQLAlchemy |
| **Database** | SQLite |
| **Frontend** | HTML5 + CSS3 |
| **JavaScript** | Vanilla JS (no jQuery) |
| **Charts** | Chart.js 3.9.1 |
| **Icons** | Font Awesome 6.4.0 |
| **Fonts** | Google Fonts (Poppins, Inter) |
| **Authentication** | Flask Sessions |
| **Security** | Werkzeug (password hashing) |

---

## 🔑 Admin Credentials

After setup, use these to login at `/admin/login`:
- **Username**: admin (or your chosen username)
- **Password**: admin123 (or your chosen password)

---

## 📊 Database Schema

### Admin Users
```sql
- id (Primary Key)
- username (Unique String)
- password_hash (String)
```

### Reports
```sql
- id (Primary Key)
- report_id (Unique) - "RPT-1234"
- title (String, min 5 chars)
- description (Text, min 10 chars)
- category (String)
- location (String)
- photo_filename (String, nullable)
- reporter_name (String, nullable)
- reporter_email (String, nullable)
- status (Enum: Pending, In Review, Resolved)
- admin_response (Text, nullable)
- created_at (DateTime)
- updated_at (DateTime)
```

---

## 🌐 API Documentation

### Public API Endpoints

#### Submit Report
```
POST /api/submit-report
Content-Type: multipart/form-data

Parameters:
- title (string, required, min 5 chars)
- description (string, required, min 10 chars)
- category (string, required)
- location (string, required)
- photo (file, optional)
- reporter_name (string, optional)
- reporter_email (string, optional)

Response:
{
  "success": true,
  "message": "Report submitted successfully!",
  "report_id": "RPT-1234"
}
```

#### Get Report Details
```
GET /api/get-report/<report_id>

Response:
{
  "success": true,
  "data": {
    "id": 1,
    "report_id": "RPT-1234",
    "title": "Pothole on Main Street",
    "description": "...",
    "category": "Road Damage",
    "location": "Main Street, Sector 5",
    "photo_filename": "123456_image.jpg",
    "reporter_name": "John Doe",
    "status": "In Review",
    "admin_response": "...",
    "created_at": "2024-05-09 10:30:00",
    "updated_at": "2024-05-09 11:00:00"
  }
}
```

#### Get All Reports
```
GET /api/get-all-reports?category=Road+Damage&status=Pending&sort=newest

Query Parameters:
- category (optional)
- status (optional)
- location (optional)
- sort (optional: newest or urgent)

Response:
{
  "success": true,
  "data": [...],
  "count": 42
}
```

#### Get Statistics
```
GET /api/get-stats

Response:
{
  "success": true,
  "data": {
    "total": 42,
    "pending": 15,
    "in_review": 8,
    "resolved": 19,
    "category_stats": {
      "Road Damage": 12,
      "Streetlight": 8,
      ...
    },
    "recent": [...]
  }
}
```

### Admin API Endpoints

#### Get All Reports (Admin)
```
GET /api/admin/get-all-reports
(Requires session authentication)
```

#### Update Report
```
PUT /api/admin/update-report/<id>
Content-Type: application/json
(Requires session authentication)

Body:
{
  "status": "Resolved",
  "admin_response": "Issue has been fixed by the road department."
}
```

#### Delete Report
```
DELETE /api/admin/delete-report/<id>
(Requires session authentication)
```

---

## 🎨 Design Highlights

- **Modern Gradient UI** - Professional orange-to-red gradient theme
- **Smooth Animations** - Page transitions and hover effects
- **Responsive Design** - Works perfectly on mobile, tablet, desktop
- **Dark Mode Ready** - CSS variables for easy theme switching
- **Accessibility** - Semantic HTML, ARIA labels, keyboard navigation
- **Performance** - Minimal CSS, no unnecessary JavaScript
- **Beautiful Typography** - Poppins (display) + Inter (body)

---

## 📱 Responsive Breakpoints

- **Mobile** - 320px to 480px
- **Tablet** - 481px to 768px
- **Desktop** - 769px to 1200px
- **Large Desktop** - 1201px+

---

## 🔒 Security Features

✅ Password hashing with Werkzeug
✅ Session-based authentication
✅ CSRF protection ready
✅ SQL injection prevention (ORM)
✅ File upload validation
✅ Input sanitization
✅ XSS prevention
✅ Rate limiting ready

---

## 📊 Charts & Visualizations

The dashboard includes:
- **Bar Chart** - Reports by category
- **Doughnut Chart** - Status distribution
- **Counter Animation** - Live statistics
- **Activity Feed** - Recent submissions

Powered by Chart.js 3.9.1

---

## 🎯 How It Works

### For Citizens:
1. **Report** → Fill form, upload photo, get Report ID
2. **Track** → Enter Report ID, see real-time status
3. **Receive Updates** → Get official responses from government

### For Government:
1. **Login** → Secure admin panel
2. **Review** → View reports with evidence (photos)
3. **Respond** → Update status and add official response
4. **Resolve** → Mark as completed with details

---

## ⚙️ Configuration

### Change Secret Key (Important for Production)
Edit `app.py`:
```python
app.config['SECRET_KEY'] = 'your-very-long-random-key-here'
```

### Modify Max Upload Size
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

### Change Database Location
Edit `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/db.sqlite'
```

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Use different port
python app.py --port 5001

# Or kill process on port 5000
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -i :5000
```

### Module Not Found Errors
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Locked
```bash
# Delete old database and recreate
rm neighbourhood_reporter.db
python app.py
```

### Admin Login Not Working
```bash
# Create new admin user
python
> from app import app, db, Admin
> app.app_context().push()
> admin = Admin(username='admin')
> admin.set_password('password123')
> db.session.add(admin)
> db.session.commit()
> exit()
```

---

## 📈 Future Enhancements

- [ ] Email notifications to reporters
- [ ] SMS alerts for urgent issues
- [ ] Google Maps integration for location picker
- [ ] Real-time WebSocket notifications
- [ ] AI-powered automatic categorization
- [ ] Multi-language support (Hindi, Marathi, etc.)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Department assignment system
- [ ] Priority levels for issues
- [ ] Comment/discussion threads
- [ ] Social sharing features
- [ ] Gamification (badges, rewards)
- [ ] Integration with government systems
- [ ] Automated reminders

---

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🙏 Acknowledgments

- Flask community for the amazing framework
- Chart.js for beautiful charts
- Font Awesome for icons
- Google Fonts for typography

---

## 💡 Perfect For

✅ Hackathons
✅ University Projects  
✅ Portfolio Showcase
✅ Learning Web Development
✅ Government Tech Solutions
✅ Civic Tech Initiatives
✅ Real-World Deployments

---

## 📞 Support & Contact

For issues:
1. Check SETUP_GUIDE.md for detailed instructions
2. Review error messages carefully
3. Check Python and dependencies versions
4. Verify file permissions and paths

---

## 🌟 Show Your Support

⭐ Star this repository if you find it helpful
🍴 Fork it to create your own version
📢 Share it with others interested in civic tech

---

**Made with ❤️ for better communities**

**Nagrik Parivartan** - Making neighborhoods better, one report at a time.

*Aapki Samasya, Seedha Sarkaar Tak*

---

## 📊 Statistics

- **Lines of Code**: 2000+
- **HTML Templates**: 8
- **CSS Code**: 1500+ lines
- **Python Code**: 600+ lines
- **Database Tables**: 2
- **API Endpoints**: 7
- **Pages**: 5 (public) + 3 (admin)
- **Categories**: 6
- **Status Types**: 3
- **Development Time**: Production-ready

---

**Version 1.0.0** | Last Updated: May 2024

Ready to deploy and use! 🚀
