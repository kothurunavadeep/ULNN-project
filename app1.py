import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans

# Load datasets
farmers_df = pd.read_csv("farmers_dataset.csv")
vendors_df = pd.read_csv("vendors_extended.csv")

# Clean data
farmers_df = farmers_df.drop_duplicates(subset=["name", "product"]).reset_index(drop=True)
vendors_df = vendors_df.drop_duplicates(subset=["name", "product"]).reset_index(drop=True)
farmers_df.dropna(subset=["location", "product"], inplace=True)
vendors_df.dropna(subset=["location", "product"], inplace=True)
farmers_df["location"] = farmers_df["location"].str.strip()
farmers_df["product"] = farmers_df["product"].str.strip()
vendors_df["location"] = vendors_df["location"].str.strip()
vendors_df["product"] = vendors_df["product"].str.strip()

# Combine for consistent label encoding
all_locations = pd.concat([farmers_df["location"], vendors_df["location"]], ignore_index=True)
all_products = pd.concat([farmers_df["product"], vendors_df["product"]], ignore_index=True)

label_encoder_location = LabelEncoder()
label_encoder_product = LabelEncoder()
label_encoder_location.fit(all_locations)
label_encoder_product.fit(all_products)

farmers_df["location_encoded"] = label_encoder_location.transform(farmers_df["location"])
farmers_df["product_encoded"] = label_encoder_product.transform(farmers_df["product"])
vendors_df["location_encoded"] = label_encoder_location.transform(vendors_df["location"])
vendors_df["product_encoded"] = label_encoder_product.transform(vendors_df["product"])

# Scale numerical features for clustering, save scaler for inverse transform
scaler = StandardScaler()
vendors_df[["reliability_score_scaled", "avg_price_quintal_scaled"]] = scaler.fit_transform(
    vendors_df[["reliability_score", "avg_price_quintal"]]
)

# KMeans clustering
farmer_features = farmers_df[["location_encoded", "product_encoded"]]
vendor_features = vendors_df[["location_encoded", "product_encoded", "reliability_score_scaled", "avg_price_quintal_scaled"]]

kmeans_farmers = KMeans(n_clusters=4, init='k-means++', random_state=42)
y_predict_farmers = kmeans_farmers.fit_predict(farmer_features)

kmeans_vendors = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_predict_vendors = kmeans_vendors.fit_predict(vendor_features)

# Streamlit UI
st.set_page_config(page_title="Farmers & Vendors Recommendation System", layout="centered")
st.title("Farmers and Vendors Recommendation System")
st.markdown("Use this tool to find the best vendors and farmers based on location and product.")

location_input = st.text_input("Enter the location (e.g., Haryana, Punjab):")
product_input = st.text_input("Enter the product (e.g., Rice, Wheat):")

def predict_best_vendor(location, product):
    try:
        loc_encoded = label_encoder_location.transform([location.strip()])[0]
        prod_encoded = label_encoder_product.transform([product.strip()])[0]
    except ValueError:
        return "Invalid location or product: not found in training data."

    matching_vendors = vendors_df[
        (vendors_df["location_encoded"] == loc_encoded) &
        (vendors_df["product_encoded"] == prod_encoded)
    ]

    if matching_vendors.empty:
        return "No matching vendors found for this location and product."

    top_vendors = matching_vendors.copy()
    # Inverse scale for user-friendly display
    top_vendors[["reliability_score", "avg_price_quintal"]] = scaler.inverse_transform(
        top_vendors[["reliability_score_scaled", "avg_price_quintal_scaled"]]
    )

    top_vendors = top_vendors.sort_values(
        by=["reliability_score", "avg_price_quintal"],
        ascending=[False, True]
    ).head(5)

    return top_vendors[["vendor_id", "name", "location", "product", "reliability_score", "avg_price_quintal"]]

def predict_best_farmer(location, product):
    try:
        loc_encoded = label_encoder_location.transform([location.strip()])[0]
        prod_encoded = label_encoder_product.transform([product.strip()])[0]
    except ValueError:
        return "Invalid location or product: not found in training data."

    farmer_input = pd.DataFrame([[loc_encoded, prod_encoded]], columns=["location_encoded", "product_encoded"])
    farmer_cluster = kmeans_farmers.predict(farmer_input)[0]

    farmers_df["kmeans_cluster"] = y_predict_farmers
    matching_farmers = farmers_df[
        (farmers_df["kmeans_cluster"] == farmer_cluster) &
        (farmers_df["location_encoded"] == loc_encoded) &
        (farmers_df["product_encoded"] == prod_encoded)
    ]

    if matching_farmers.empty:
        return "No suitable farmers found."

    return matching_farmers[["farmer_id", "name", "location", "product"]].head(5)

# Display results
if location_input and product_input:
    if st.button("Find Best Vendors"):
        vendor_result = predict_best_vendor(location_input, product_input)
        st.markdown("### Best Vendors:")
        if isinstance(vendor_result, pd.DataFrame):
            st.dataframe(vendor_result)
        else:
            st.error(vendor_result)

    if st.button("Find Best Farmers"):
        farmer_result = predict_best_farmer(location_input, product_input)
        st.markdown("### Best Farmers:")
        if isinstance(farmer_result, pd.DataFrame):
            st.dataframe(farmer_result)
        else:
            st.error(farmer_result)
else:
    st.info("Please enter both location and product to get results.")
