@echo off
REM Nagrik Parivartan - Quick Setup Script for Windows

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   Nagrik Parivartan - Neighbourhood Problem Reporter   ║
echo ║          Quick Setup Script (Windows)                  ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Step 1: Create virtual environment
echo [1] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and in your PATH
    pause
    exit /b 1
)
echo ✓ Virtual environment created

REM Step 2: Activate virtual environment
echo.
echo [2] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Step 3: Install dependencies
echo.
echo [3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Step 4: Create database and admin user
echo.
echo [4] Creating database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✓ Database created')"

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║              CREATE ADMIN USER                         ║
echo ╚════════════════════════════════════════════════════════╝
echo.

python -c "from app import app; app.app_context().push(); exec(open('app.py').read().split('if __name__')[0]); exec(app.cli.commands['create_admin'].callback())" 2>nul || (
    echo Please create admin user manually:
    echo.ppython
    echo   python
    echo   ^> from app import app, db, Admin
    echo   ^> app.app_context().push()
    echo   ^> admin = Admin(username='admin', password_hash='...')
    echo   ^> admin.set_password('admin123')
    echo   ^> db.session.add(admin)
    echo   ^> db.session.commit()
    echo   ^> exit()
    echo.
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║              SETUP COMPLETE!                           ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo.
echo 1. Keep this terminal open
echo 2. Run the application:
echo    python app.py
echo.
echo 3. Open your browser and go to:
echo    http://localhost:5000
echo.
echo 4. Admin login at:
echo    http://localhost:5000/admin/login
echo    Username: admin
echo    Password: admin123 (or what you set)
echo.
echo ✓ Setup complete! Ready to start.
echo.
pause
