from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    district = db.Column(db.String(50), nullable=True)
    soil_type = db.Column(db.String(50), nullable=True)
    farm_size = db.Column(db.Float, nullable=True)
    profile_pic = db.Column(db.String(200), default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('CropRecommendation', backref='farmer', lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship('Feedback', backref='farmer', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='farmer', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=True)  # Cereal, Pulse, Fruit, Vegetable, Fiber, Oilseed
    growing_season = db.Column(db.String(50), nullable=True)  # Kharif, Rabi, Zaid, Year-round
    soil_type = db.Column(db.String(100), nullable=True)  # Clayey, Loamy, Sandy, Black, Red
    water_requirement = db.Column(db.String(50), nullable=True)  # High, Medium, Low
    growing_tips = db.Column(db.Text, nullable=True)
    expected_yield = db.Column(db.String(100), nullable=True)
    advantages = db.Column(db.Text, nullable=True)

class CropRecommendation(db.Model):
    __tablename__ = 'crop_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    state = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    soil_type = db.Column(db.String(50), nullable=False)
    water_availability = db.Column(db.String(50), nullable=False)
    farm_size = db.Column(db.Float, nullable=True)
    recommended_crops = db.Column(db.String(255), nullable=False)  # Comma-separated crop names
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Weather(db.Model):
    __tablename__ = 'weather'
    
    id = db.Column(db.Integer, primary_key=True)
    weather_condition = db.Column(db.String(50), nullable=False)  # Sunny, Rainy, Cloudy, Stormy, Wind
    temp_min = db.Column(db.Float, nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)  # Tips for farmers

class Fertilizer(db.Model):
    __tablename__ = 'fertilizers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    soil_type = db.Column(db.String(50), nullable=True)
    growth_stage = db.Column(db.String(50), nullable=True)  # Sowing, Vegetative, Flowering, Harvesting
    recommended_quantity = db.Column(db.String(100), nullable=True)
    method = db.Column(db.String(100), nullable=True)  # Broadcasting, Foliar spray, Drip line
    safety_tips = db.Column(db.Text, nullable=True)

class Pest(db.Model):
    __tablename__ = 'pests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    causes = db.Column(db.Text, nullable=True)
    prevention = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)
    recommended_pesticides = db.Column(db.String(255), nullable=True)
    image_path = db.Column(db.String(250), default='default_pest.jpg')

class Disease(db.Model):
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    causes = db.Column(db.Text, nullable=True)
    prevention = db.Column(db.Text, nullable=True)
    treatment = db.Column(db.Text, nullable=True)
    recommended_pesticides = db.Column(db.String(255), nullable=True)
    image_path = db.Column(db.String(250), default='default_disease.jpg')

class Irrigation(db.Model):
    __tablename__ = 'irrigation'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    water_requirement = db.Column(db.String(100), nullable=True)
    irrigation_method = db.Column(db.String(100), nullable=True)  # Drip, Sprinkler, Surface
    water_saving_tips = db.Column(db.Text, nullable=True)
    schedule = db.Column(db.String(100), nullable=True)

class MarketPrice(db.Model):
    __tablename__ = 'market_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    market_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)  # Price per Quintal or KG
    previous_price = db.Column(db.Float, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(250), default='default_news.jpg')
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)  # Schemes, Market, Technology, Weather, General
    published_at = db.Column(db.DateTime, default=datetime.utcnow)

class GovernmentScheme(db.Model):
    __tablename__ = 'government_schemes'
    
    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=True)
    eligibility = db.Column(db.Text, nullable=True)
    apply_link = db.Column(db.String(250), nullable=True)
    deadline = db.Column(db.String(100), nullable=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Pending, Reviewed
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
