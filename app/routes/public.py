import re
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Admin, ContactMessage

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    return render_template('public/index.html')

@public_bp.route('/about')
def about():
    return render_template('public/about.html')

@public_bp.route('/services')
def services():
    return render_template('public/services.html')

@public_bp.route('/features')
def features():
    return render_template('public/features.html')

@public_bp.route('/faq')
def faq():
    return render_template('public/faq.html')

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Server-side validation
        if not name or not email or not message:
            flash('Please fill in all required fields.', 'danger')
            return render_template('public/contact.html')
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('public/contact.html')
            
        # Save contact message
        new_msg = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(new_msg)
        db.session.commit()
        
        flash('Thank you for contacting us! Your message has been received.', 'success')
        return redirect(url_for('public.contact'))
        
    return render_template('public/contact.html')

@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if session.get('user_role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('farmer.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('public/login.html')
            
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_role'] = 'farmer'
            login_user(user)
            flash('Welcome back! Logged in successfully.', 'success')
            return redirect(url_for('farmer.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('public/login.html')

@public_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if session.get('user_role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('farmer.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('public/admin_login.html')
            
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['user_role'] = 'admin'
            login_user(admin)
            flash('Logged in successfully as Administrator.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')
            
    return render_template('public/admin_login.html')

@public_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('farmer.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        state = request.form.get('state')
        district = request.form.get('district')
        soil_type = request.form.get('soil_type')
        farm_size = request.form.get('farm_size')
        
        # Server-side validation
        if not username or not email or not password or not name:
            flash('Please fill in all required fields.', 'danger')
            return render_template('public/register.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('public/register.html')
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('public/register.html')
            
        if User.query.filter_by(username=username).first():
            flash('Username is already taken.', 'danger')
            return render_template('public/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'danger')
            return render_template('public/register.html')
            
        try:
            farm_size_val = float(farm_size) if farm_size else None
        except ValueError:
            flash('Farm size must be a valid number.', 'danger')
            return render_template('public/register.html')
            
        new_user = User(
            username=username,
            email=email,
            name=name,
            phone=phone,
            state=state,
            district=district,
            soil_type=soil_type,
            farm_size=farm_size_val
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('public.login'))
        
    return render_template('public/register.html')

@public_bp.route('/logout')
def logout():
    logout_user()
    session.pop('user_role', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('public.index'))
