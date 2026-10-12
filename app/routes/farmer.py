import os
from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, User, Crop, CropRecommendation, Weather, Fertilizer, Pest, Disease, Irrigation, MarketPrice, News, GovernmentScheme, Feedback, Notification

farmer_bp = Blueprint('farmer', __name__)

# Decorator to restrict access to farmers only
def farmer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or session.get('user_role') != 'farmer':
            flash('Access restricted to Farmers. Please log in.', 'danger')
            return redirect(url_for('public.login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@farmer_bp.route('/dashboard')
@farmer_required
def dashboard():
    # Gather statistics
    total_crops = Crop.query.count()
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(5).all()
    recent_recs = CropRecommendation.query.filter_by(user_id=current_user.id).order_by(CropRecommendation.created_at.desc()).limit(3).all()
    latest_news = News.query.order_by(News.published_at.desc()).limit(3).all()
    latest_schemes = GovernmentScheme.query.limit(3).all()
    
    # Get mock weather for the farmer's district
    district = current_user.district or 'Dharwad'
    temp = 28.5
    humidity = 65.0
    weather_cond = 'Sunny'
    
    # Get weather advice
    weather_tip = Weather.query.filter_by(weather_condition=weather_cond).first()
    weather_recommendation = weather_tip.recommendation if weather_tip else 'No advisory available for today.'
    
    # Get latest market price update
    latest_price = MarketPrice.query.order_by(MarketPrice.updated_at.desc()).first()
    
    return render_template(
        'farmer/dashboard.html',
        total_crops=total_crops,
        notifications=notifications,
        recent_recs=recent_recs,
        latest_news=latest_news,
        latest_schemes=latest_schemes,
        weather_cond=weather_cond,
        temp=temp,
        humidity=humidity,
        weather_recommendation=weather_recommendation,
        latest_price=latest_price,
        district=district
    )

@farmer_bp.route('/profile', methods=['GET', 'POST'])
@farmer_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        state = request.form.get('state')
        district = request.form.get('district')
        soil_type = request.form.get('soil_type')
        farm_size = request.form.get('farm_size')
        
        # Server-side validation
        if not name:
            flash('Name is required.', 'danger')
            return redirect(url_for('farmer.profile'))
            
        try:
            farm_size_val = float(farm_size) if farm_size else None
        except ValueError:
            flash('Farm size must be a valid number.', 'danger')
            return redirect(url_for('farmer.profile'))
            
        current_user.name = name
        current_user.phone = phone
        current_user.state = state
        current_user.district = district
        current_user.soil_type = soil_type
        current_user.farm_size = farm_size_val
        
        # Handle file upload
        file = request.files.get('profile_pic')
        if file and file.filename != '':
            if allowed_file(file.filename):
                filename = secure_filename(f"user_{current_user.id}_{file.filename}")
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                current_user.profile_pic = filename
            else:
                flash('Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF', 'danger')
                return redirect(url_for('farmer.profile'))
                
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('farmer.profile'))
        
    return render_template('farmer/profile.html')

@farmer_bp.route('/crop-recommendation', methods=['GET', 'POST'])
@farmer_required
def crop_recommendation():
    if request.method == 'POST':
        state = request.form.get('state')
        district = request.form.get('district')
        season = request.form.get('season')
        soil_type = request.form.get('soil_type')
        water_availability = request.form.get('water_availability')
        farm_size = request.form.get('farm_size')
        
        # Recommendation Logic
        query = Crop.query
        
        # Season filter
        if season:
            query = query.filter((Crop.growing_season == season) | (Crop.growing_season == 'Year-round'))
            
        # Soil type filter
        if soil_type:
            # Matches if crop soil_type includes selected soil type (case insensitive)
            query = query.filter(Crop.soil_type.like(f"%{soil_type}%"))
            
        # Water availability filter
        if water_availability == 'Low':
            query = query.filter(Crop.water_requirement == 'Low')
        elif water_availability == 'Medium':
            query = query.filter((Crop.water_requirement == 'Low') | (Crop.water_requirement == 'Medium'))
        # If water availability is High, all water requirements are eligible
        
        recommended_list = query.all()
        
        # Fallback if no crop matches
        if not recommended_list:
            # Recommend crops matching season and soil type without water restrictions
            fallback_query = Crop.query
            if season:
                fallback_query = fallback_query.filter((Crop.growing_season == season) | (Crop.growing_season == 'Year-round'))
            recommended_list = fallback_query.limit(2).all()
            
        recommended_names = ", ".join([crop.name for crop in recommended_list]) if recommended_list else "None"
        
        try:
            farm_size_val = float(farm_size) if farm_size else None
        except ValueError:
            farm_size_val = None
            
        # Save recommendation history
        rec = CropRecommendation(
            user_id=current_user.id,
            state=state,
            district=district,
            season=season,
            soil_type=soil_type,
            water_availability=water_availability,
            farm_size=farm_size_val,
            recommended_crops=recommended_names
        )
        db.session.add(rec)
        db.session.commit()
        
        flash('Recommendation generated successfully!', 'success')
        return render_template('farmer/crop_recommendation.html', recommended_crops=recommended_list, inputs=request.form)
        
    return render_template('farmer/crop_recommendation.html')

@farmer_bp.route('/weather-advisory')
@farmer_required
def weather_advisory():
    # Simulated weather forecast
    forecasts = [
        {'day': 'Today', 'condition': 'Sunny', 'temp': '30°C / 22°C', 'humidity': '45%', 'wind': '12 km/h', 'icon': 'fa-sun text-warning'},
        {'day': 'Tomorrow', 'condition': 'Cloudy', 'temp': '29°C / 21°C', 'humidity': '60%', 'wind': '15 km/h', 'icon': 'fa-cloud text-secondary'},
        {'day': 'Day after', 'condition': 'Rainy', 'temp': '26°C / 20°C', 'humidity': '85%', 'wind': '18 km/h', 'icon': 'fa-cloud-showers-heavy text-primary'},
    ]
    
    # Get advisories for Sunny, Rainy, Cloudy conditions
    sunny_adv = Weather.query.filter_by(weather_condition='Sunny').first()
    rainy_adv = Weather.query.filter_by(weather_condition='Rainy').first()
    cloudy_adv = Weather.query.filter_by(weather_condition='Cloudy').first()
    
    return render_template('farmer/weather.html', forecasts=forecasts, sunny_adv=sunny_adv, rainy_adv=rainy_adv, cloudy_adv=cloudy_adv)

@farmer_bp.route('/fertilizer-recommendation', methods=['GET', 'POST'])
@farmer_required
def fertilizer_recommendation():
    crops = Crop.query.all()
    results = None
    
    if request.method == 'POST':
        crop_name = request.form.get('crop_name')
        soil_type = request.form.get('soil_type')
        growth_stage = request.form.get('growth_stage')
        
        # Match fertilizers
        query = Fertilizer.query.filter_by(crop_name=crop_name)
        if soil_type:
            query = query.filter_by(soil_type=soil_type)
        if growth_stage:
            query = query.filter_by(growth_stage=growth_stage)
            
        results = query.all()
        
        # Fallback to general crop fertilizers if exact match fails
        if not results:
            results = Fertilizer.query.filter_by(crop_name=crop_name).all()
            
        return render_template('farmer/fertilizer.html', crops=crops, results=results, inputs=request.form)
        
    return render_template('farmer/fertilizer.html', crops=crops)

@farmer_bp.route('/pest-disease')
@farmer_required
def pest_disease():
    pests = Pest.query.all()
    diseases = Disease.query.all()
    return render_template('farmer/pest_disease.html', pests=pests, diseases=diseases)

@farmer_bp.route('/pest-disease/<type>/<int:id>')
@farmer_required
def pest_disease_detail(type, id):
    if type == 'pest':
        item = Pest.query.get_or_404(id)
        is_pest = True
    else:
        item = Disease.query.get_or_404(id)
        is_pest = False
    return render_template('farmer/pest_disease_detail.html', item=item, is_pest=is_pest)

@farmer_bp.route('/irrigation-advisory')
@farmer_required
def irrigation_advisory():
    irrigation_list = Irrigation.query.all()
    return render_template('farmer/irrigation.html', irrigation_list=irrigation_list)

@farmer_bp.route('/market-prices')
@farmer_required
def market_prices():
    prices = MarketPrice.query.all()
    
    # Extract unique crop and market lists for filters
    crops = sorted(list(set([p.crop_name for p in prices])))
    markets = sorted(list(set([p.market_name for p in prices])))
    
    return render_template('farmer/market_prices.html', prices=prices, crops=crops, markets=markets)

@farmer_bp.route('/agricultural-news')
@farmer_required
def agricultural_news():
    news_list = News.query.order_by(News.published_at.desc()).all()
    return render_template('farmer/news.html', news_list=news_list)

@farmer_bp.route('/government-schemes')
@farmer_required
def government_schemes():
    schemes = GovernmentScheme.query.all()
    return render_template('farmer/schemes.html', schemes=schemes)

@farmer_bp.route('/feedback', methods=['GET', 'POST'])
@farmer_required
def feedback():
    if request.method == 'POST':
        rating = request.form.get('rating')
        message = request.form.get('message')
        
        if not rating or not message:
            flash('Rating and message are required.', 'danger')
            return redirect(url_for('farmer.feedback'))
            
        feedback_obj = Feedback(
            user_id=current_user.id,
            rating=int(rating),
            message=message
        )
        db.session.add(feedback_obj)
        db.session.commit()
        
        flash('Feedback submitted successfully! Thank you.', 'success')
        return redirect(url_for('farmer.feedback'))
        
    feedback_history = Feedback.query.filter_by(user_id=current_user.id).order_by(Feedback.submitted_at.desc()).all()
    return render_template('farmer/feedback.html', feedbacks=feedback_history)

@farmer_bp.route('/settings', methods=['GET', 'POST'])
@farmer_required
def settings():
    if request.method == 'POST':
        # Language switching is handled in JS (using client translation maps),
        # but we can also store the farmer's preference in session
        language = request.form.get('language')
        if language in ['en', 'kn']:
            session['lang'] = language
            
        # Change password logic
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_new = request.form.get('confirm_new_password')
        
        if old_password and new_password:
            if not current_user.check_password(old_password):
                flash('Incorrect current password.', 'danger')
                return redirect(url_for('farmer.settings'))
            if new_password != confirm_new:
                flash('New passwords do not match.', 'danger')
                return redirect(url_for('farmer.settings'))
                
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('farmer.settings'))
        
    return render_template('farmer/settings.html')

@farmer_bp.route('/notifications/read/<int:id>')
@farmer_required
def read_notification(id):
    notif = Notification.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    notif.is_read = True
    db.session.commit()
    return redirect(request.referrer or url_for('farmer.dashboard'))
