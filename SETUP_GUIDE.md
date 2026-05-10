# 🗺️ Nagrik Parivartan - Neighbourhood Problem Reporter

## Complete Setup Guide

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

---

## 🚀 Quick Start

### Step 1: Extract & Navigate to Project
```bash
# Navigate to your project folder
cd Nagrik-Parivartan
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Admin User
```bash
# Run Flask shell
flask shell

# Inside the shell, run:
create_admin()
```

Follow the prompts to enter:
- Username: (e.g., `admin`)
- Password: (e.g., `admin123`)

Then exit the shell:
```bash
exit()
```

### Step 5: Run the Application
```bash
python app.py
```

The application will start at: **http://localhost:5000**

---

## 🎯 Features

### 👤 Citizen Features
- **Report a Problem**: Submit issues with title, description, category, location, and optional photo
- **Track Report**: Enter Report ID to track status in real-time
- **View All Reports**: Browse community reports with filters by category, status, location
- **Dashboard**: View statistics and charts showing all reported issues

### 🛠️ Admin Features
- **Secure Login**: Username and password protected access
- **Manage Reports**: View all submitted reports in an organized table
- **Update Status**: Change report status (Pending → In Review → Resolved)
- **Add Response**: Leave official responses visible to reporters
- **Delete Reports**: Remove spam or invalid reports

---

## 🗂️ Project Structure

```
Nagrik-Parivartan/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── neighbourhood_reporter.db  # SQLite database (auto-created)
├── uploads/                  # Folder for uploaded photos
│   └── (photo files)
├── templates/                # HTML templates
│   ├── index.html           # Home page
│   ├── report.html          # Report submission
│   ├── track.html           # Track report
│   ├── reports.html         # Browse all reports
│   ├── stats.html           # Dashboard
│   ├── admin_login.html     # Admin login
│   └── admin_dashboard.html # Admin panel
└── static/                  # Static files
    └── style.css            # Modern CSS styling
```

---

## 🔑 Admin Login Credentials

After creating admin user in Step 4:
- **URL**: http://localhost:5000/admin/login
- **Username**: Your chosen username
- **Password**: Your chosen password

---

## 📱 User Flows

### Report a Problem
1. Click "Report Problem" from navigation
2. Fill form with:
   - Problem title (min 5 characters)
   - Description (min 10 characters)
   - Category (Road Damage, Streetlight, Water Supply, Garbage, Drainage, Other)
   - Location (area/street name)
   - Optional photo upload
   - Optional contact info
3. Submit → Get unique Report ID
4. Share or save Report ID for tracking

### Track Report
1. Click "Track Report" from navigation
2. Enter Report ID (e.g., RPT-1234)
3. View:
   - Real-time status updates
   - Full report details
   - Official responses
   - Evidence photo
   - Timeline of progress

### Admin Review
1. Login at http://localhost:5000/admin/login
2. View all reports in dashboard
3. Click "View & Edit" on any report
4. Update status and add official response
5. Changes visible to reporter immediately

---

## 🎨 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python + Flask 2.3.3 |
| Database | SQLite + SQLAlchemy ORM |
| Frontend | HTML5 + Modern CSS3 |
| JavaScript | Vanilla JS (no dependencies) |
| Charts | Chart.js 3.9.1 |
| Icons | Font Awesome 6.4.0 |
| Fonts | Google Fonts (Poppins, Inter) |

---

## 📊 Categories

- 🚧 **Road Damage** - Potholes, broken roads, damaged pavements
- 💡 **Streetlight** - Non-functional streetlights, broken poles
- 🚰 **Water Supply** - Water leakage, supply issues
- 🗑️ **Garbage** - Waste management, littering
- 🌊 **Drainage** - Blocked drains, water accumulation
- 🌳 **Other** - Any other issue

---

## 📊 Report Statuses

- 🟡 **Pending** - Report submitted, awaiting review
- 🔵 **In Review** - Government officials are reviewing
- 🟢 **Resolved** - Issue has been fixed

---

## 🔐 Security Features

✅ Password hashing for admin credentials
✅ Session-based authentication
✅ File upload validation
✅ Input sanitization
✅ CSRF protection ready
✅ SQL injection prevention via ORM

---

## 📈 Database Schema

### Admin Table
- id (Primary Key)
- username (Unique)
- password_hash

### Report Table
- id (Primary Key)
- report_id (Unique) - e.g., "RPT-1234"
- title
- description
- category
- location
- photo_filename
- reporter_name (optional)
- reporter_email (optional)
- status (Pending/In Review/Resolved)
- admin_response
- created_at
- updated_at

---

## 🌐 API Endpoints

### Public Endpoints
- `POST /api/submit-report` - Submit new report
- `GET /api/get-report/<report_id>` - Get specific report
- `GET /api/get-all-reports` - Get all reports with filters
- `GET /api/get-stats` - Get dashboard statistics

### Admin Endpoints (Protected)
- `GET /api/admin/get-all-reports` - Get all reports for admin
- `PUT /api/admin/update-report/<id>` - Update report status/response
- `DELETE /api/admin/delete-report/<id>` - Delete report

---

## 🎯 How It Works (3-Step Process)

### Step 1: Report 📝
Citizen submits a detailed report with location, category, and optional photo. Receives unique Report ID instantly.

### Step 2: Review 🔍
Government officials review the report, update its status, and add official responses. Citizens can see progress in real-time.

### Step 3: Resolve ✅
Once the issue is fixed, officials mark it as "Resolved" with details. The system creates a record of successful resolution.

---

## 🎨 Design Features

✨ Modern, gradient-based UI
✨ Smooth animations and transitions
✨ Responsive design (mobile-friendly)
✨ Dark mode ready components
✨ Accessibility-focused
✨ Fast loading times
✨ Beautiful typography (Poppins + Inter fonts)
✨ Interactive charts and statistics

---

## 🔧 Configuration

### Change Secret Key (Production)
In `app.py`, line 11:
```python
app.config['SECRET_KEY'] = 'your-new-secret-key-here'
```

### Max File Upload Size
In `app.py`, line 12:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Database Location
In `app.py`, line 11:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/database.db'
```

---

## 📱 File Upload

- **Supported Formats**: PNG, JPG, JPEG, GIF, WebP
- **Max Size**: 16MB
- **Storage**: `/uploads/` folder (auto-created)

---

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```bash
# Use a different port
python app.py --port 5001
```

### Issue: Module not found
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Database locked
```bash
# Delete the database and create new
rm neighbourhood_reporter.db
python app.py
```

### Issue: Admin login not working
```bash
# Create new admin user
flask shell
create_admin()
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all files are in correct folders
3. Ensure Python version is 3.8+
4. Check that all dependencies are installed

---

## 🎓 Learning Resources

This project demonstrates:
- ✅ Flask web framework
- ✅ SQLAlchemy ORM
- ✅ RESTful API design
- ✅ Session authentication
- ✅ File upload handling
- ✅ Modern CSS3 & responsive design
- ✅ Chart.js integration
- ✅ Form validation
- ✅ Database design
- ✅ MVC architecture

---

## 📜 License

This is an open-source project for educational purposes.

---

## 🌟 Features Highlights

🎯 **Real-World Problem**: Solves actual civic issue reporting
🎯 **Role-Based Access**: Different interfaces for citizens and officials
🎯 **Media Support**: Photo upload for evidence
🎯 **Tracking System**: Unique ID system for professional tracking
🎯 **Analytics**: Beautiful charts and statistics
🎯 **Responsive**: Works on all devices
🎯 **Modern Design**: Clean, professional UI
🎯 **Scalable**: Easy to extend with more features

---

## 🚀 Future Enhancements

- [ ] Email notifications
- [ ] SMS alerts
- [ ] Map integration
- [ ] Real-time notifications
- [ ] AI-based categorization
- [ ] Multiple language support
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Department assignment
- [ ] Priority levels

---

**Made with ❤️ for better communities**

Nagrik Parivartan - Your voice, Straight to the Government
