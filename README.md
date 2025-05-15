                                            Direct Market Access for Farmers

This project empowers farmers by giving them **direct access to suitable vendors** using machine learning. By leveraging clustering techniques, we group similar farmers and vendors and recommend smart pairings based on shared characteristics like product type, location, pricing, and reliability.

✨ Project Features
🔄 Bidirectional Recommendation System
 Matches farmers to vendors and vendors to farmers using clustering logic.
📍 Location-Aware Matching
 Ensures that recommendations are geographically relevant.
🌽 Product-Specific Pairing
 Recommendations are based on shared or compatible crop/product types.
📊 Reliability & Pricing Consideration
 Vendors are scored by reliability and average price offered per quintal.
🤖 Machine Learning-Based Clustering
 Farmers and vendors are grouped using K-Means to uncover hidden patterns.
🧼 Data Cleaning & Preprocessing
 Handles missing values, duplicates, and encodes categorical variables.
🔄 Scalable & Flexible Design
 Can handle more data or new product types without code restructuring.
📦 Separation of Farmer and Vendor Logic
 Farmers and vendors are processed independently for accurate groupings.
 

📁 Datasets
1. farmers_dataset.csv
Details of 4,265 farmers:
farmer_id: Unique identifier
name: Farmer's name
location: State or region
product: Primary crop/product grown
2. vendors_extended.csv
Details of 4,825 vendors:
vendor_id: Unique identifier
name: Vendor or business name
location: State or region
product: Product of interest
reliability_score: Rating (0 to 5) based on trustworthiness
avg_price_quintal: Average price offered per quintal



⚙️ Technologies Used
Python
Pandas, NumPy – Data manipulation
Matplotlib – Visualization (optional)
Scikit-learn – Machine Learning:
LabelEncoder, StandardScaler – Preprocessing
KMeans – Clustering



🚀 Workflow
Data Cleaning:
Removed duplicates (name, product)
Dropped entries with missing location or product
Preprocessing:
Encoded categorical variables
Scaled features for uniformity
Clustering:
Farmers and vendors clustered separately using K-Means
Vendors clustered by product type, location, reliability, pricing
Farmers clustered by product type and location
Recommendation System:
Each farmer is matched to one or more vendors from a compatible cluster
Enables smarter, localized trade connections


🧾 Sample Output

Farmer:
- ID: F1888
- Name: Manoj
- Location: UP
- Product: Potato
  
✅ Recommended Vendors:
1. V3931 - FarmDirect (UP) | Reliability: 4.8 | Price: ₹1100
2. V6723 - FreshLink (UP) | Reliability: 4.5 | Price: ₹1150
3. V1021 - HarvestHub (UP) | Reliability: 4.2 | Price: ₹1080

Vendor:
- ID: V2044
- Name: AgroMart
- Location: MH
- Product: Onion
  
✅ Recommended Farmers:
1. F3001 - Suresh (MH) | Product: Onion
2. F1102 - Rekha (MH) | Product: Onion
3. F2450 - Kiran (MH) | Product: Onion

✅ Benefits

Direct Access to Markets for farmers
Improved Matching using machine learning insights
Location-aware vendor selection
Scalable & Flexible – supports new data without retraining

🔮 Future Enhancements

Include distance or logistics cost in clustering
Build a web-based interface for interactive recommendations
Enable real-time dynamic updates as market data changes

Contributers

CH.Harsha luke
K.Navadeep
D.tharun
