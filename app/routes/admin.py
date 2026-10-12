import csv
from io import StringIO
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, Response
from flask_login import login_required, current_user
from app.models import db, User, Admin, Crop, Weather, Fertilizer, Pest, Disease, Irrigation, MarketPrice, News, GovernmentScheme, Feedback, ContactMessage, Notification

admin_bp = Blueprint('admin', __name__)

# Decorator to restrict access to administrators only
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or session.get('user_role') != 'admin':
            flash('Access restricted to Administrators. Please log in.', 'danger')
            return redirect(url_for('public.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Gather statistics
    farmer_count = User.query.count()
    crop_count = Crop.query.count()
    pest_count = Pest.query.count()
    disease_count = Disease.query.count()
    feedback_count = Feedback.query.count()
    news_count = News.query.count()
    scheme_count = GovernmentScheme.query.count()
    contact_count = ContactMessage.query.count()
    
    # Recent items
    recent_farmers = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_feedbacks = Feedback.query.order_by(Feedback.submitted_at.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        farmer_count=farmer_count,
        crop_count=crop_count,
        pest_count=pest_count,
        disease_count=disease_count,
        feedback_count=feedback_count,
        news_count=news_count,
        scheme_count=scheme_count,
        contact_count=contact_count,
        recent_farmers=recent_farmers,
        recent_feedbacks=recent_feedbacks
    )

# --- CRUD: MANAGING USERS (FARMERS) ---
@admin_bp.route('/users', methods=['GET', 'POST'])
@admin_required
def manage_users():
    if request.method == 'POST':
        # Add new farmer
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        state = request.form.get('state')
        district = request.form.get('district')
        soil_type = request.form.get('soil_type')
        
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('admin.manage_users'))
            
        new_user = User(username=username, email=email, name=name, phone=phone, state=state, district=district, soil_type=soil_type)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Farmer added successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
        
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/edit/<int:id>', methods=['POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    user.name = request.form.get('name')
    user.email = request.form.get('email')
    user.phone = request.form.get('phone')
    user.state = request.form.get('state')
    user.district = request.form.get('district')
    user.soil_type = request.form.get('soil_type')
    
    password = request.form.get('password')
    if password:
        user.set_password(password)
        
    db.session.commit()
    flash('Farmer updated successfully!', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/delete/<int:id>')
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Farmer profile deleted.', 'success')
    return redirect(url_for('admin.manage_users'))

# --- CRUD: MANAGING CROPS ---
@admin_bp.route('/crops', methods=['GET', 'POST'])
@admin_required
def manage_crops():
    if request.method == 'POST':
        name = request.form.get('name')
        crop_type = request.form.get('type')
        season = request.form.get('growing_season')
        soil = request.form.get('soil_type')
        water = request.form.get('water_requirement')
        tips = request.form.get('growing_tips')
        y = request.form.get('expected_yield')
        adv = request.form.get('advantages')
        
        new_crop = Crop(name=name, type=crop_type, growing_season=season, soil_type=soil, water_requirement=water, growing_tips=tips, expected_yield=y, advantages=adv)
        db.session.add(new_crop)
        db.session.commit()
        flash('Crop created successfully!', 'success')
        return redirect(url_for('admin.manage_crops'))
        
    crops = Crop.query.all()
    return render_template('admin/crops.html', crops=crops)

@admin_bp.route('/crops/edit/<int:id>', methods=['POST'])
@admin_required
def edit_crop(id):
    crop = Crop.query.get_or_404(id)
    crop.name = request.form.get('name')
    crop.type = request.form.get('type')
    crop.growing_season = request.form.get('growing_season')
    crop.soil_type = request.form.get('soil_type')
    crop.water_requirement = request.form.get('water_requirement')
    crop.growing_tips = request.form.get('growing_tips')
    crop.expected_yield = request.form.get('expected_yield')
    crop.advantages = request.form.get('advantages')
    
    db.session.commit()
    flash('Crop updated successfully!', 'success')
    return redirect(url_for('admin.manage_crops'))

@admin_bp.route('/crops/delete/<int:id>')
@admin_required
def delete_crop(id):
    crop = Crop.query.get_or_404(id)
    db.session.delete(crop)
    db.session.commit()
    flash('Crop deleted.', 'success')
    return redirect(url_for('admin.manage_crops'))

# --- CRUD: MANAGING FERTILIZERS ---
@admin_bp.route('/fertilizers', methods=['GET', 'POST'])
@admin_required
def manage_fertilizers():
    if request.method == 'POST':
        name = request.form.get('name')
        crop_name = request.form.get('crop_name')
        soil_type = request.form.get('soil_type')
        growth_stage = request.form.get('growth_stage')
        quantity = request.form.get('recommended_quantity')
        method = request.form.get('method')
        safety = request.form.get('safety_tips')
        
        new_fert = Fertilizer(name=name, crop_name=crop_name, soil_type=soil_type, growth_stage=growth_stage, recommended_quantity=quantity, method=method, safety_tips=safety)
        db.session.add(new_fert)
        db.session.commit()
        flash('Fertilizer recommendations created!', 'success')
        return redirect(url_for('admin.manage_fertilizers'))
        
    ferts = Fertilizer.query.all()
    crops = Crop.query.all()
    return render_template('admin/fertilizers.html', fertilizers=ferts, crops=crops)

@admin_bp.route('/fertilizers/edit/<int:id>', methods=['POST'])
@admin_required
def edit_fertilizer(id):
    fert = Fertilizer.query.get_or_404(id)
    fert.name = request.form.get('name')
    fert.crop_name = request.form.get('crop_name')
    fert.soil_type = request.form.get('soil_type')
    fert.growth_stage = request.form.get('growth_stage')
    fert.recommended_quantity = request.form.get('recommended_quantity')
    fert.method = request.form.get('method')
    fert.safety_tips = request.form.get('safety_tips')
    
    db.session.commit()
    flash('Fertilizer recommendations updated!', 'success')
    return redirect(url_for('admin.manage_fertilizers'))

@admin_bp.route('/fertilizers/delete/<int:id>')
@admin_required
def delete_fertilizer(id):
    fert = Fertilizer.query.get_or_404(id)
    db.session.delete(fert)
    db.session.commit()
    flash('Fertilizer details deleted.', 'success')
    return redirect(url_for('admin.manage_fertilizers'))

# --- CRUD: MANAGING WEATHER TIPS ---
@admin_bp.route('/weather-tips', methods=['GET', 'POST'])
@admin_required
def manage_weather():
    if request.method == 'POST':
        condition = request.form.get('weather_condition')
        temp_min = float(request.form.get('temp_min'))
        temp_max = float(request.form.get('temp_max'))
        humidity = float(request.form.get('humidity'))
        recommendation = request.form.get('recommendation')
        
        new_weather = Weather(weather_condition=condition, temp_min=temp_min, temp_max=temp_max, humidity=humidity, recommendation=recommendation)
        db.session.add(new_weather)
        db.session.commit()
        flash('Weather Advisory Tip added!', 'success')
        return redirect(url_for('admin.manage_weather'))
        
    tips = Weather.query.all()
    return render_template('admin/weather.html', tips=tips)

@admin_bp.route('/weather-tips/edit/<int:id>', methods=['POST'])
@admin_required
def edit_weather(id):
    tip = Weather.query.get_or_404(id)
    tip.weather_condition = request.form.get('weather_condition')
    tip.temp_min = float(request.form.get('temp_min'))
    tip.temp_max = float(request.form.get('temp_max'))
    tip.humidity = float(request.form.get('humidity'))
    tip.recommendation = request.form.get('recommendation')
    
    db.session.commit()
    flash('Weather Advisory Tip updated!', 'success')
    return redirect(url_for('admin.manage_weather'))

@admin_bp.route('/weather-tips/delete/<int:id>')
@admin_required
def delete_weather(id):
    tip = Weather.query.get_or_404(id)
    db.session.delete(tip)
    db.session.commit()
    flash('Weather Tip deleted.', 'success')
    return redirect(url_for('admin.manage_weather'))

# --- CRUD: MANAGING PESTS ---
@admin_bp.route('/pests', methods=['GET', 'POST'])
@admin_required
def manage_pests():
    if request.method == 'POST':
        name = request.form.get('name')
        crop_name = request.form.get('crop_name')
        symptoms = request.form.get('symptoms')
        causes = request.form.get('causes')
        prevention = request.form.get('prevention')
        treatment = request.form.get('treatment')
        pesticides = request.form.get('recommended_pesticides')
        
        new_pest = Pest(name=name, crop_name=crop_name, symptoms=symptoms, causes=causes, prevention=prevention, treatment=treatment, recommended_pesticides=pesticides)
        db.session.add(new_pest)
        db.session.commit()
        flash('Pest details created!', 'success')
        return redirect(url_for('admin.manage_pests'))
        
    pests = Pest.query.all()
    crops = Crop.query.all()
    return render_template('admin/pests.html', pests=pests, crops=crops)

@admin_bp.route('/pests/edit/<int:id>', methods=['POST'])
@admin_required
def edit_pest(id):
    pest = Pest.query.get_or_404(id)
    pest.name = request.form.get('name')
    pest.crop_name = request.form.get('crop_name')
    pest.symptoms = request.form.get('symptoms')
    pest.causes = request.form.get('causes')
    pest.prevention = request.form.get('prevention')
    pest.treatment = request.form.get('treatment')
    pest.recommended_pesticides = request.form.get('recommended_pesticides')
    
    db.session.commit()
    flash('Pest details updated!', 'success')
    return redirect(url_for('admin.manage_pests'))

@admin_bp.route('/pests/delete/<int:id>')
@admin_required
def delete_pest(id):
    pest = Pest.query.get_or_404(id)
    db.session.delete(pest)
    db.session.commit()
    flash('Pest removed.', 'success')
    return redirect(url_for('admin.manage_pests'))

# --- CRUD: MANAGING DISEASES ---
@admin_bp.route('/diseases', methods=['GET', 'POST'])
@admin_required
def manage_diseases():
    if request.method == 'POST':
        name = request.form.get('name')
        crop_name = request.form.get('crop_name')
        symptoms = request.form.get('symptoms')
        causes = request.form.get('causes')
        prevention = request.form.get('prevention')
        treatment = request.form.get('treatment')
        pesticides = request.form.get('recommended_pesticides')
        
        new_disease = Disease(name=name, crop_name=crop_name, symptoms=symptoms, causes=causes, prevention=prevention, treatment=treatment, recommended_pesticides=pesticides)
        db.session.add(new_disease)
        db.session.commit()
        flash('Disease details created!', 'success')
        return redirect(url_for('admin.manage_diseases'))
        
    diseases = Disease.query.all()
    crops = Crop.query.all()
    return render_template('admin/diseases.html', diseases=diseases, crops=crops)

@admin_bp.route('/diseases/edit/<int:id>', methods=['POST'])
@admin_required
def edit_disease(id):
    d = Disease.query.get_or_404(id)
    d.name = request.form.get('name')
    d.crop_name = request.form.get('crop_name')
    d.symptoms = request.form.get('symptoms')
    d.causes = request.form.get('causes')
    d.prevention = request.form.get('prevention')
    d.treatment = request.form.get('treatment')
    d.recommended_pesticides = request.form.get('recommended_pesticides')
    
    db.session.commit()
    flash('Disease details updated!', 'success')
    return redirect(url_for('admin.manage_diseases'))

@admin_bp.route('/diseases/delete/<int:id>')
@admin_required
def delete_disease(id):
    d = Disease.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    flash('Disease removed.', 'success')
    return redirect(url_for('admin.manage_diseases'))

# --- CRUD: MANAGING IRRIGATION ---
@admin_bp.route('/irrigation', methods=['GET', 'POST'])
@admin_required
def manage_irrigation():
    if request.method == 'POST':
        crop_name = request.form.get('crop_name')
        water = request.form.get('water_requirement')
        method = request.form.get('irrigation_method')
        tips = request.form.get('water_saving_tips')
        schedule = request.form.get('schedule')
        
        new_irr = Irrigation(crop_name=crop_name, water_requirement=water, irrigation_method=method, water_saving_tips=tips, schedule=schedule)
        db.session.add(new_irr)
        db.session.commit()
        flash('Irrigation schedule added!', 'success')
        return redirect(url_for('admin.manage_irrigation'))
        
    irrs = Irrigation.query.all()
    crops = Crop.query.all()
    return render_template('admin/irrigation.html', irrigation_list=irrs, crops=crops)

@admin_bp.route('/irrigation/edit/<int:id>', methods=['POST'])
@admin_required
def edit_irrigation(id):
    irr = Irrigation.query.get_or_404(id)
    irr.crop_name = request.form.get('crop_name')
    irr.water_requirement = request.form.get('water_requirement')
    irr.irrigation_method = request.form.get('irrigation_method')
    irr.water_saving_tips = request.form.get('water_saving_tips')
    irr.schedule = request.form.get('schedule')
    
    db.session.commit()
    flash('Irrigation details updated!', 'success')
    return redirect(url_for('admin.manage_irrigation'))

@admin_bp.route('/irrigation/delete/<int:id>')
@admin_required
def delete_irrigation(id):
    irr = Irrigation.query.get_or_404(id)
    db.session.delete(irr)
    db.session.commit()
    flash('Irrigation advisory removed.', 'success')
    return redirect(url_for('admin.manage_irrigation'))

# --- CRUD: MANAGING MARKET PRICES ---
@admin_bp.route('/market-prices', methods=['GET', 'POST'])
@admin_required
def manage_market_prices():
    if request.method == 'POST':
        crop_name = request.form.get('crop_name')
        market_name = request.form.get('market_name')
        current = float(request.form.get('current_price'))
        prev = request.form.get('previous_price')
        previous = float(prev) if prev else None
        
        new_price = MarketPrice(crop_name=crop_name, market_name=market_name, current_price=current, previous_price=previous)
        db.session.add(new_price)
        db.session.commit()
        flash('Market Price successfully listed!', 'success')
        return redirect(url_for('admin.manage_market_prices'))
        
    prices = MarketPrice.query.all()
    crops = Crop.query.all()
    return render_template('admin/market_prices.html', prices=prices, crops=crops)

@admin_bp.route('/market-prices/edit/<int:id>', methods=['POST'])
@admin_required
def edit_market_price(id):
    price = MarketPrice.query.get_or_404(id)
    price.crop_name = request.form.get('crop_name')
    price.market_name = request.form.get('market_name')
    price.previous_price = price.current_price
    price.current_price = float(request.form.get('current_price'))
    
    db.session.commit()
    flash('Market price updated!', 'success')
    return redirect(url_for('admin.manage_market_prices'))

@admin_bp.route('/market-prices/delete/<int:id>')
@admin_required
def delete_market_price(id):
    price = MarketPrice.query.get_or_404(id)
    db.session.delete(price)
    db.session.commit()
    flash('Market price listing removed.', 'success')
    return redirect(url_for('admin.manage_market_prices'))

# --- CRUD: MANAGING NEWS ---
@admin_bp.route('/news', methods=['GET', 'POST'])
@admin_required
def manage_news():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        cat = request.form.get('category')
        
        new_n = News(title=title, description=desc, category=cat)
        db.session.add(new_n)
        db.session.commit()
        flash('News article published!', 'success')
        return redirect(url_for('admin.manage_news'))
        
    news_list = News.query.order_by(News.published_at.desc()).all()
    return render_template('admin/news.html', news_list=news_list)

@admin_bp.route('/news/edit/<int:id>', methods=['POST'])
@admin_required
def edit_news(id):
    n = News.query.get_or_404(id)
    n.title = request.form.get('title')
    n.description = request.form.get('description')
    n.category = request.form.get('category')
    
    db.session.commit()
    flash('News article modified!', 'success')
    return redirect(url_for('admin.manage_news'))

@admin_bp.route('/news/delete/<int:id>')
@admin_required
def delete_news(id):
    n = News.query.get_or_404(id)
    db.session.delete(n)
    db.session.commit()
    flash('News article deleted.', 'success')
    return redirect(url_for('admin.manage_news'))

# --- CRUD: MANAGING GOVERNMENT SCHEMES ---
@admin_bp.route('/schemes', methods=['GET', 'POST'])
@admin_required
def manage_schemes():
    if request.method == 'POST':
        name = request.form.get('scheme_name')
        desc = request.form.get('description')
        benefits = request.form.get('benefits')
        eligibility = request.form.get('eligibility')
        link = request.form.get('apply_link')
        deadline = request.form.get('deadline')
        
        new_s = GovernmentScheme(scheme_name=name, description=desc, benefits=benefits, eligibility=eligibility, apply_link=link, deadline=deadline)
        db.session.add(new_s)
        db.session.commit()
        flash('Government scheme added successfully!', 'success')
        return redirect(url_for('admin.manage_schemes'))
        
    schemes = GovernmentScheme.query.all()
    return render_template('admin/schemes.html', schemes=schemes)

@admin_bp.route('/schemes/edit/<int:id>', methods=['POST'])
@admin_required
def edit_scheme(id):
    s = GovernmentScheme.query.get_or_404(id)
    s.scheme_name = request.form.get('scheme_name')
    s.description = request.form.get('description')
    s.benefits = request.form.get('benefits')
    s.eligibility = request.form.get('eligibility')
    s.apply_link = request.form.get('apply_link')
    s.deadline = request.form.get('deadline')
    
    db.session.commit()
    flash('Scheme updated successfully!', 'success')
    return redirect(url_for('admin.manage_schemes'))

@admin_bp.route('/schemes/delete/<int:id>')
@admin_required
def delete_scheme(id):
    s = GovernmentScheme.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Scheme deleted.', 'success')
    return redirect(url_for('admin.manage_schemes'))

# --- CRUD: FEEDBACK VIEWING ---
@admin_bp.route('/feedback', methods=['GET'])
@admin_required
def view_feedback():
    feedbacks = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    return render_template('admin/feedback.html', feedbacks=feedbacks)

@admin_bp.route('/feedback/review/<int:id>')
@admin_required
def review_feedback(id):
    f = Feedback.query.get_or_404(id)
    f.status = 'Reviewed'
    db.session.commit()
    flash('Feedback marked as reviewed.', 'success')
    return redirect(url_for('admin.view_feedback'))

@admin_bp.route('/feedback/delete/<int:id>')
@admin_required
def delete_feedback(id):
    f = Feedback.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    flash('Feedback removed.', 'success')
    return redirect(url_for('admin.view_feedback'))

# --- VIEW CONTACT MESSAGES ---
@admin_bp.route('/contact-messages')
@admin_required
def contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.submitted_at.desc()).all()
    return render_template('admin/contact_messages.html', messages=messages)

@admin_bp.route('/contact-messages/delete/<int:id>')
@admin_required
def delete_contact_message(id):
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Contact query deleted.', 'success')
    return redirect(url_for('admin.contact_messages'))

# --- REPORTS ---
@admin_bp.route('/reports')
@admin_required
def reports():
    # Summary of stats
    farmer_count = User.query.count()
    crop_count = Crop.query.count()
    feedback_count = Feedback.query.count()
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar() or 0.0
    avg_rating = round(avg_rating, 2)
    
    return render_template('admin/reports.html', farmer_count=farmer_count, crop_count=crop_count, feedback_count=feedback_count, avg_rating=avg_rating)

# CSV Export Helpers
@admin_bp.route('/reports/export/<type>')
@admin_required
def export_report_csv(type):
    si = StringIO()
    cw = csv.writer(si)
    
    if type == 'farmers':
        cw.writerow(['Farmer ID', 'Username', 'Name', 'Email', 'Phone', 'Location', 'Soil Type', 'Farm Size (Acres)', 'Date Joined'])
        records = User.query.all()
        for r in records:
            cw.writerow([r.id, r.username, r.name, r.email, r.phone, f"{r.district or ''}, {r.state or ''}", r.soil_type or '', r.farm_size or '', r.created_at])
    elif type == 'crops':
        cw.writerow(['Crop ID', 'Name', 'Type', 'Season', 'Soil Type', 'Water Req.', 'Expected Yield'])
        records = Crop.query.all()
        for r in records:
            cw.writerow([r.id, r.name, r.type, r.growing_season, r.soil_type, r.water_requirement, r.expected_yield])
    elif type == 'feedback':
        cw.writerow(['Feedback ID', 'Farmer Name', 'Rating', 'Message', 'Status', 'Date Submitted'])
        records = Feedback.query.all()
        for r in records:
            name = r.farmer.name if r.farmer else 'Anonymous'
            cw.writerow([r.id, name, r.rating, r.message, r.status, r.submitted_at])
    else:
        return redirect(url_for('admin.reports'))
        
    response = Response(si.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename=smart_agri_{type}_report.csv'
    return response

# --- SETTINGS ---
@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_new = request.form.get('confirm_new_password')
        
        if old_password and new_password:
            if not current_user.check_password(old_password):
                flash('Incorrect current password.', 'danger')
                return redirect(url_for('admin.settings'))
            if new_password != confirm_new:
                flash('New passwords do not match.', 'danger')
                return redirect(url_for('admin.settings'))
                
            current_user.set_password(new_password)
            db.session.commit()
            flash('Admin password updated successfully!', 'success')
            return redirect(url_for('admin.settings'))
            
        flash('No changes made.', 'info')
        return redirect(url_for('admin.settings'))
        
    return render_template('admin/settings.html')
