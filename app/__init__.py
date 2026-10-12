import os
from flask import Flask, session
from flask_login import LoginManager
from app.config import Config
from app.models import db, User, Admin, Crop, Weather, Fertilizer, Pest, Disease, Irrigation, MarketPrice, News, GovernmentScheme, Feedback, Notification

login_manager = LoginManager()
login_manager.login_view = 'public.login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    role = session.get('user_role')
    if role == 'admin':
        return Admin.query.get(int(user_id))
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register Blueprints
    from app.routes.public import public_bp
    from app.routes.farmer import farmer_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(farmer_bp, url_prefix='/farmer')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Auto-create and seed database (primarily for SQLite out-of-the-box experience)
    with app.app_context():
        db.create_all()
        seed_if_empty()
        
    return app

def seed_if_empty():
    # If admin doesn't exist, seed basic data
    if Admin.query.first() is None:
        print("Database is empty. Seeding sample data...")
        
        # 1. Seed Admin
        admin = Admin(username='admin', email='admin@smartagri.com', name='Admin Officer')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 2. Seed Farmer
        farmer = User(username='farmer', email='farmer@smartagri.com', name='Ramesh Kumar', 
                      phone='9876543210', state='Karnataka', district='Dharwad', soil_type='Black Soil', farm_size=5.5)
        farmer.set_password('farmer123')
        db.session.add(farmer)
        db.session.commit() # Commit to get farmer.id
        
        # 3. Seed Crops
        crops = [
            Crop(name='Rice', type='Cereal', growing_season='Kharif', soil_type='Clayey', water_requirement='High', 
                 growing_tips='Maintain 2-5 cm standing water during early stages. Keep fields weed-free.', 
                 expected_yield='2.5 - 3.5 tons/acre', advantages='High demand, stable market prices, food security staple.'),
            Crop(name='Wheat', type='Cereal', growing_season='Rabi', soil_type='Loamy', water_requirement='Medium', 
                 growing_tips='Sow in November. Require 4-6 irrigations at critical growth stages.', 
                 expected_yield='1.8 - 2.5 tons/acre', advantages='High nutritional value, straw is excellent fodder for livestock.'),
            Crop(name='Cotton', type='Fiber', growing_season='Kharif', soil_type='Black', water_requirement='Medium', 
                 growing_tips='Ensure deep ploughing. Maintain spacing of 90x60 cm. Control bollworms early.', 
                 expected_yield='0.8 - 1.2 tons/acre', advantages='Excellent cash crop with high commercial value in textile industries.'),
            Crop(name='Maize', type='Cereal', growing_season='Kharif', soil_type='Loamy', water_requirement='Medium', 
                 growing_tips='Provide good drainage. Apply nitrogen fertilizers in split doses.', 
                 expected_yield='2.0 - 3.0 tons/acre', advantages='Short duration crop, useful for food, poultry feed, and starch industries.'),
            Crop(name='Tomato', type='Vegetable', growing_season='Year-round', soil_type='Sandy Loam', water_requirement='Medium', 
                 growing_tips='Stake the plants for support. Prune side shoots. Water consistently to avoid blossom end rot.', 
                 expected_yield='10 - 15 tons/acre', advantages='Quick returns, high yielding, high market demand in local and export markets.'),
            Crop(name='Coffee', type='Beverage', growing_season='Year-round', soil_type='Red Loam', water_requirement='High', 
                 growing_tips='Grow under shade trees. Keep soil organic-rich. Prune regularly after harvest.', 
                 expected_yield='0.5 - 0.8 tons/acre', advantages='High export value, long-term profitable crop, grows well in hilly terrains.')
        ]
        db.session.bulk_save_objects(crops)
        
        # 4. Seed Weather
        weather_tips = [
            Weather(weather_condition='Sunny', temp_min=20.0, temp_max=38.0, humidity=40.0, 
                    recommendation='Clear skies ahead. Ideal time for weeding, pesticide spraying, and harvesting crops. Ensure proper irrigation for young seedlings.'),
            Weather(weather_condition='Rainy', temp_min=15.0, temp_max=30.0, humidity=90.0, 
                    recommendation='Heavy rain expected. Avoid spraying pesticides or applying fertilizers. Postpone irrigation and clear drainage channels to prevent waterlogging.'),
            Weather(weather_condition='Cloudy', temp_min=18.0, temp_max=32.0, humidity=75.0, 
                    recommendation='Overcast conditions. High humidity can trigger fungal diseases. Inspect crops for pests. Postpone solar drying of grains.'),
            Weather(weather_condition='Windy', temp_min=15.0, temp_max=35.0, humidity=50.0, 
                    recommendation='Strong winds forecasted. Secure weak stakes for vegetable crops. Avoid overhead sprinkler irrigation as wind affects water distribution.')
        ]
        db.session.bulk_save_objects(weather_tips)
        
        # 5. Seed Fertilizers
        fertilizers = [
            Fertilizer(name='Urea (Nitrogen)', crop_name='Rice', soil_type='Clayey', growth_stage='Vegetative', 
                       recommended_quantity='50 kg/acre', method='Broadcasting in standing water', 
                       safety_tips='Wear gloves during application. Wash hands thoroughly. Avoid skin contact.'),
            Fertilizer(name='DAP (Di-Ammonium Phosphate)', crop_name='Wheat', soil_type='Loamy', growth_stage='Sowing/Basal', 
                       recommended_quantity='40 kg/acre', method='Soil incorporation during sowing', 
                       safety_tips='Avoid inhaling dust. Store in dry place away from children.'),
            Fertilizer(name='NPK 19-19-19', crop_name='Tomato', soil_type='Sandy Loam', growth_stage='Flowering', 
                       recommended_quantity='5 kg/acre', method='Drip irrigation (Fertigation)', 
                       safety_tips='Dilute in water correctly. Do not mix with calcium fertilizers.'),
            Fertilizer(name='Organic Compost', crop_name='Coffee', soil_type='Red Loam', growth_stage='Harvest/Post-harvest', 
                       recommended_quantity='5 tonnes/acre', method='Basal dressing around the tree base', 
                       safety_tips='Ensure it is fully decomposed to prevent weed seeds and pathogens.')
        ]
        db.session.bulk_save_objects(fertilizers)
        
        # 6. Seed Pests
        pests = [
            Pest(name='Stem Borer', crop_name='Rice', 
                 symptoms='Dead hearts (withered central shoots), white heads (empty panicles).', 
                 causes='Moth larvae boring into the plant stems during warm and humid weather.', 
                 prevention='Sow resistant varieties. Maintain clean cultivation and destroy stubbles.', 
                 treatment='Set up light traps to catch moths. Release Trichogramma wasps.', 
                 recommended_pesticides='Chlorantraniliprole 18.5% SC', image_path='pest_stem_borer.jpg'),
            Pest(name='Aphids', crop_name='Tomato', 
                 symptoms='Curled leaves, stunted growth, sticky honeydew secretion with black soot.', 
                 causes='Small sucking insects spreading rapidly in dry, cool conditions.', 
                 prevention='Encourage natural predators like ladybugs and lacewings.', 
                 treatment='Spray neem oil solution (1-2%). Clean fields of host weeds.', 
                 recommended_pesticides='Imidacloprid 17.8% SL', image_path='pest_aphids.jpg')
        ]
        db.session.bulk_save_objects(pests)
        
        # 7. Seed Diseases
        diseases = [
            Disease(name='Blast Disease', crop_name='Rice', 
                    symptoms='Spindle-shaped lesions on leaves with grey centers and brown borders.', 
                    causes='Magnaporthe oryzae fungus spreading via wind-borne spores in humid weather.', 
                    prevention='Avoid excessive nitrogen application. Clean farm implements.', 
                    treatment='Apply balanced fertilizers. Keep water level consistent.', 
                    recommended_pesticides='Tricyclazole 75% WP', image_path='disease_rice_blast.jpg'),
            Disease(name='Rust Disease', crop_name='Wheat', 
                    symptoms='Orange-brown pustules on leaves and leaf sheaths forming parallel lines.', 
                    causes='Puccinia graminis fungus spreading rapidly in cool, wet environments.', 
                    prevention='Plant rust-resistant wheat varieties. Destroy wild barberry plants.', 
                    treatment='Apply spray fungicides immediately at the first sign of rust.', 
                    recommended_pesticides='Propiconazole 25% EC', image_path='disease_wheat_rust.jpg')
        ]
        db.session.bulk_save_objects(diseases)
        
        # 8. Seed Irrigation
        irrigation_tips = [
            Irrigation(crop_name='Rice', water_requirement='1200 - 1500 mm', irrigation_method='Alternate Wetting and Drying (AWD)', 
                       water_saving_tips='Adopt AWD to save up to 30% water without reducing yield. Maintain bunds to avoid leaks.', 
                       schedule='Keep 2-5 cm water, let it dry naturally, then re-irrigate.'),
            Irrigation(crop_name='Wheat', water_requirement='450 - 650 mm', irrigation_method='Border Strip Irrigation', 
                       water_saving_tips='Irrigate during critical stages: Crown Root Initiation (21 days), Flowering, and Milking.', 
                       schedule='Irrigate once every 20-25 days depending on soil moisture.'),
            Irrigation(crop_name='Tomato', water_requirement='600 - 800 mm', irrigation_method='Drip Irrigation', 
                       water_saving_tips='Use plastic mulch sheets to reduce evaporation and control weeds. Schedule irrigation in the morning.', 
                       schedule='Apply 2-3 liters/plant daily using drip emitters.')
        ]
        db.session.bulk_save_objects(irrigation_tips)
        
        # 9. Seed Market Prices
        market_prices = [
            MarketPrice(crop_name='Rice (Paddy)', market_name='Dharwad Market', current_price=2300.0, previous_price=2250.0),
            MarketPrice(crop_name='Rice (Paddy)', market_name='Hubli Market', current_price=2350.0, previous_price=2400.0),
            MarketPrice(crop_name='Wheat', market_name='Gadag Market', current_price=2600.0, previous_price=2550.0),
            MarketPrice(crop_name='Cotton', market_name='Havery Market', current_price=7200.0, previous_price=7100.0),
            MarketPrice(crop_name='Tomato', market_name='Bangalore APMC', current_price=1500.0, previous_price=1800.0),
            MarketPrice(crop_name='Coffee (Robusta)', market_name='Chikmagalur Market', current_price=18500.0, previous_price=18000.0)
        ]
        db.session.bulk_save_objects(market_prices)
        
        # 10. Seed News
        news_items = [
            News(title='PM-KISAN 17th Installment Released', 
                 description='The government has released the 17th installment of PM-KISAN, transferring benefits to over 9.5 crore farmers across India. Check your status online.', 
                 category='Schemes'),
            News(title='Monsoon Rainfall Forecast Update', 
                 description='The Meteorological department expects normal to heavy rainfall in the southern districts of Karnataka this week. Farmers are advised to clear field drainage.', 
                 category='Weather'),
            News(title='Emergence of New Fungal Blight in Vegetables', 
                 description='Horticulture experts warn vegetable growers of potential blight outbreaks due to high relative humidity. Organic solutions and preventive sprays are recommended.', 
                 category='Technology')
        ]
        db.session.bulk_save_objects(news_items)
        
        # 11. Seed Government Schemes
        schemes = [
            GovernmentScheme(scheme_name='PM-KISAN Samman Nidhi', 
                             description='An initiative by the Government of India providing income support to all landholding farmers families across the country.', 
                             benefits='Financial benefit of Rs. 6,000 per year in three equal installments of Rs. 2,000.', 
                             eligibility='All small and marginal landholding farmer families who own cultivable land.', 
                             apply_link='https://pmkisan.gov.in/', deadline='Open Year-Round'),
            GovernmentScheme(scheme_name='Pradhan Mantri Fasal Bima Yojana (PMFBY)', 
                             description='A government-sponsored crop insurance scheme that integrates multiple stakeholders to protect farmers from crop loss.', 
                             benefits='Low premium rates (1.5% to 5%) with full financial coverage against natural calamities, pests, and diseases.', 
                             eligibility='All farmers growing notified crops in notified areas, including tenant farmers.', 
                             apply_link='https://pmfby.gov.in/', deadline='August 15, 2026'),
            GovernmentScheme(scheme_name='Kisan Credit Card (KCC) Scheme', 
                             description='A scheme designed to provide farmers with quick access to short-term loans for crop production, maintenance, and emergency expenses.', 
                             benefits='Access to credit at low interest rates (around 4% after subvention) with simplified application process.', 
                             eligibility='All farmers, owner-cultivators, tenant farmers, sharecroppers, and self-help groups.', 
                             apply_link='https://www.sbi.co.in/web/personal-banking/loans/agriculture-loans/kisan-credit-card', deadline='Open Year-Round')
        ]
        db.session.bulk_save_objects(schemes)
        
        # 12. Seed Feedbacks
        feedbacks = [
            Feedback(user_id=farmer.id, rating=5, message='Excellent app! The crop recommendations are highly accurate for my soil. The market price update is very helpful.', status='Reviewed'),
            Feedback(user_id=farmer.id, rating=4, message='Very good dashboard. Can we get Kannada voice alerts in the future?', status='Pending')
        ]
        db.session.bulk_save_objects(feedbacks)
        
        # 13. Seed Notifications
        notifications = [
            Notification(user_id=farmer.id, title='Welcome to Smart Agriculture System!', 
                         message='Hello Ramesh! Explore the dashboards to get your personalized crop recommendations, weather advisory, and market price updates.')
        ]
        db.session.bulk_save_objects(notifications)
        
        db.session.commit()
        print("Database seeded successfully!")
