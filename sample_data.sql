-- Seed Data for Smart Agriculture Advisory System
USE smart_agri;

-- Insert Admins
INSERT INTO admins (username, password, email, name) VALUES 
('admin', 'scrypt:32768:8:1$qnVx57a9lW0MyRhd$103c27706939bb7f9f5a7398dd6d5f1006f5ab6c58dc01ddc3ce2f93310afa96f306249fd8fafe4d640d46b4fc7af683a5a7569eb68281343f7c951907d59ed2', 'admin@smartagri.com', 'Admin Officer');

-- Insert Users (Farmers)
INSERT INTO users (username, password, email, name, phone, state, district, soil_type, farm_size, profile_pic) VALUES 
('farmer', 'scrypt:32768:8:1$PiJ9gi1mC2cQwSdZ$6ba8f1f677aae7f3141ffef74b158f5af28b983068c6ec18d88d2e14760046479d7b01e51bc48b82d25bb395b097dc6a1e93f672abbb7a0009f6cd0ce8e5b4bf', 'farmer@smartagri.com', 'Ramesh Kumar', '9876543210', 'Karnataka', 'Dharwad', 'Black Soil', 5.5, 'default.jpg');

-- Insert Crops
INSERT INTO crops (name, type, growing_season, soil_type, water_requirement, growing_tips, expected_yield, advantages) VALUES 
('Rice', 'Cereal', 'Kharif', 'Clayey', 'High', 'Maintain 2-5 cm standing water during early stages. Keep fields weed-free.', '2.5 - 3.5 tons/acre', 'High demand, stable market prices, food security staple.'),
('Wheat', 'Cereal', 'Rabi', 'Loamy', 'Medium', 'Sow in November. Require 4-6 irrigations at critical growth stages.', '1.8 - 2.5 tons/acre', 'High nutritional value, straw is excellent fodder for livestock.'),
('Cotton', 'Fiber', 'Kharif', 'Black', 'Medium', 'Ensure deep ploughing. Maintain spacing of 90x60 cm. Control bollworms early.', '0.8 - 1.2 tons/acre', 'Excellent cash crop with high commercial value in textile industries.'),
('Maize', 'Cereal', 'Kharif', 'Loamy', 'Medium', 'Provide good drainage. Apply nitrogen fertilizers in split doses.', '2.0 - 3.0 tons/acre', 'Short duration crop, useful for food, poultry feed, and starch industries.'),
('Tomato', 'Vegetable', 'Year-round', 'Sandy Loam', 'Medium', 'Stake the plants for support. Prune side shoots. Water consistently to avoid blossom end rot.', '10 - 15 tons/acre', 'Quick returns, high yielding, high market demand in local and export markets.'),
('Coffee', 'Beverage', 'Year-round', 'Red Loam', 'High', 'Grow under shade trees. Keep soil organic-rich. Prune regularly after harvest.', '0.5 - 0.8 tons/acre', 'High export value, long-term profitable crop, grows well in hilly terrains.');

-- Insert Weather Advisories
INSERT INTO weather (weather_condition, temp_min, temp_max, humidity, recommendation) VALUES 
('Sunny', 20.0, 38.0, 40.0, 'Clear skies ahead. Ideal time for weeding, pesticide spraying, and harvesting crops. Ensure proper irrigation for young seedlings.'),
('Rainy', 15.0, 30.0, 90.0, 'Heavy rain expected. Avoid spraying pesticides or applying fertilizers. Postpone irrigation and clear drainage channels to prevent waterlogging.'),
('Cloudy', 18.0, 32.0, 75.0, 'Overcast conditions. High humidity can trigger fungal diseases. Inspect crops for pests. Postpone solar drying of grains.'),
('Windy', 15.0, 35.0, 50.0, 'Strong winds forecasted. Secure weak stakes for vegetable crops. Avoid overhead sprinkler irrigation as wind affects water distribution.');

-- Insert Fertilizers
INSERT INTO fertilizers (name, crop_name, soil_type, growth_stage, recommended_quantity, method, safety_tips) VALUES 
('Urea (Nitrogen)', 'Rice', 'Clayey', 'Vegetative', '50 kg/acre', 'Broadcasting in standing water', 'Wear gloves during application. Wash hands thoroughly. Avoid skin contact.'),
('DAP (Di-Ammonium Phosphate)', 'Wheat', 'Loamy', 'Sow/Basal', '40 kg/acre', 'Soil incorporation during sowing', 'Avoid inhaling dust. Store in dry place away from children.'),
('NPK 19-19-19', 'Tomato', 'Sandy Loam', 'Flowering', '5 kg/acre', 'Drip irrigation (Fertigation)', 'Dilute in water correctly. Do not mix with calcium fertilizers.'),
('Organic Compost', 'Coffee', 'Red Loam', 'Harvest/Post-harvest', '5 tonnes/acre', 'Basal dressing around the tree base', 'Ensure it is fully decomposed to prevent weed seeds and pathogens.');

-- Insert Pests
INSERT INTO pests (name, crop_name, symptoms, causes, prevention, treatment, recommended_pesticides, image_path) VALUES 
('Stem Borer', 'Rice', 'Dead hearts (withered central shoots), white heads (empty panicles).', 'Moth larvae boring into the plant stems during warm and humid weather.', 'Sow resistant varieties. Maintain clean cultivation and destroy stubbles.', 'Set up light traps to catch moths. Release Trichogramma wasps.', 'Chlorantraniliprole 18.5% SC', 'pest_stem_borer.jpg'),
('Aphids', 'Tomato', 'Curled leaves, stunted growth, sticky honeydew secretion with black soot.', 'Small sucking insects spreading rapidly in dry, cool conditions.', 'Encourage natural predators like ladybugs and lacewings.', 'Spray neem oil solution (1-2%). Clean fields of host weeds.', 'Imidacloprid 17.8% SL', 'pest_aphids.jpg');

-- Insert Diseases
INSERT INTO diseases (name, crop_name, symptoms, causes, prevention, treatment, recommended_pesticides, image_path) VALUES 
('Blast Disease', 'Rice', 'Spindle-shaped lesions on leaves with grey centers and brown borders.', 'Magnaporthe oryzae fungus spreading via wind-borne spores in humid weather.', 'Avoid excessive nitrogen application. Clean farm implements.', 'Apply balanced fertilizers. Keep water level consistent.', 'Tricyclazole 75% WP', 'disease_rice_blast.jpg'),
('Rust Disease', 'Wheat', 'Orange-brown pustules on leaves and leaf sheaths forming parallel lines.', 'Puccinia graminis fungus spreading rapidly in cool, wet environments.', 'Plant rust-resistant wheat varieties. Destroy wild barberry plants.', 'Apply spray fungicides immediately at the first sign of rust.', 'Propiconazole 25% EC', 'disease_wheat_rust.jpg');

-- Insert Irrigation
INSERT INTO irrigation (crop_name, water_requirement, irrigation_method, water_saving_tips, schedule) VALUES 
('Rice', '1200 - 1500 mm', 'Alternate Wetting and Drying (AWD)', 'Adopt AWD to save up to 30% water without reducing yield. Maintain bunds to avoid leaks.', 'Keep 2-5 cm water, let it dry naturally, then re-irrigate.'),
('Wheat', '450 - 650 mm', 'Border Strip Irrigation', 'Irrigate during critical stages: Crown Root Initiation (21 days), Flowering, and Milking.', 'Irrigate once every 20-25 days depending on soil moisture.'),
('Tomato', '600 - 800 mm', 'Drip Irrigation', 'Use plastic mulch sheets to reduce evaporation and control weeds. Schedule irrigation in the morning.', 'Apply 2-3 liters/plant daily using drip emitters.');

-- Insert Market Prices
INSERT INTO market_prices (crop_name, market_name, current_price, previous_price) VALUES 
('Rice (Paddy)', 'Dharwad Market', 2300.0, 2250.0),
('Rice (Paddy)', 'Hubli Market', 2350.0, 2400.0),
('Wheat', 'Gadag Market', 2600.0, 2550.0),
('Cotton', 'Havery Market', 7200.0, 7100.0),
('Tomato', 'Bangalore APMC', 1500.0, 1800.0),
('Coffee (Robusta)', 'Chikmagalur Market', 18500.0, 18000.0);

-- Insert News
INSERT INTO news (title, description, category) VALUES 
('PM-KISAN 17th Installment Released', 'The government has released the 17th installment of PM-KISAN, transferring benefits to over 9.5 crore farmers across India. Check your status online.', 'Schemes'),
('Monsoon Rainfall Forecast Update', 'The Meteorological department expects normal to heavy rainfall in the southern districts of Karnataka this week. Farmers are advised to clear field drainage.', 'Weather'),
('Emergence of New Fungal Blight in Vegetables', 'Horticulture experts warn vegetable growers of potential blight outbreaks due to high relative humidity. Organic solutions and preventive sprays are recommended.', 'Technology');

-- Insert Government Schemes
INSERT INTO government_schemes (scheme_name, description, benefits, eligibility, apply_link, deadline) VALUES 
('PM-KISAN Samman Nidhi', 'An initiative by the Government of India providing income support to all landholding farmers families across the country.', 'Financial benefit of Rs. 6,000 per year in three equal installments of Rs. 2,000.', 'All small and marginal landholding farmer families who own cultivable land.', 'https://pmkisan.gov.in/', 'Open Year-Round'),
('Pradhan Mantri Fasal Bima Yojana (PMFBY)', 'A government-sponsored crop insurance scheme that integrates multiple stakeholders to protect farmers from crop loss.', 'Low premium rates (1.5% to 5%) with full financial coverage against natural calamities, pests, and diseases.', 'All farmers growing notified crops in notified areas, including tenant farmers.', 'https://pmfby.gov.in/', 'August 15, 2026'),
('Kisan Credit Card (KCC) Scheme', 'A scheme designed to provide farmers with quick access to short-term loans for crop production, maintenance, and emergency expenses.', 'Access to credit at low interest rates (around 4% after subvention) with simplified application process.', 'All farmers, owner-cultivators, tenant farmers, sharecroppers, and self-help groups.', 'https://www.sbi.co.in/web/personal-banking/loans/agriculture-loans/kisan-credit-card', 'Open Year-Round');

-- Insert Feedback
INSERT INTO feedback (user_id, rating, message, status) VALUES 
(1, 5, 'Excellent app! The crop recommendations are highly accurate for my soil. The market price update is very helpful.', 'Reviewed'),
(1, 4, 'Very good dashboard. Can we get Kannada voice alerts in the future?', 'Pending');

-- Insert Contact Messages
INSERT INTO contact_messages (name, email, subject, message) VALUES 
('Suresh Patil', 'suresh@gmail.com', 'KCC Loan Issue', 'I want help in applying for Kisan Credit Card from Dharwad district.'),
('Ananya Hegde', 'ananya@gmail.com', 'Feedback on Soil Testing', 'We need more information on nearby soil testing laboratories.');

-- Insert Notifications
INSERT INTO notifications (user_id, title, message) VALUES 
(1, 'Welcome to Smart Agriculture System!', 'Hello Ramesh! Explore the dashboards to get your personalized crop recommendations, weather advisory, and market price updates.');
