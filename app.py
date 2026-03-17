import streamlit as st
import pandas as pd
import datetime

# --- SETTINGS & THEME ---
st.set_page_config(page_title="Poultry Pro Manager", layout="wide")

# Navigation Menu
menu = st.sidebar.radio("Navigation", ["Profiles", "Daily Entry", "Farm Info & History"])

# --- 1. PROFILES PAGE ---
if menu == "Profiles":
    st.title("👥 Farm Profiles")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("View Farm: Green Valley"):
            st.session_state['farm_name'] = "Green Valley Poultry"
            st.session_state['address'] = "123 Farm Lane, Sector 4"
            st.success(f"Selected: {st.session_state['farm_name']}")
    
    if 'farm_name' in st.session_state:
        st.write(f"**Farm Name:** {st.session_state['farm_name']}")
        st.write(f"**Address:** {st.session_state['address']}")

# --- 2. DAILY ENTRY (The Logic Center) ---
elif menu == "Daily Entry":
    st.title("📝 Daily Analysis")
    
    with st.form("entry_form"):
        st.subheader("Today's Inputs")
        age = st.number_input("Bird Age (Days)", 1, 35, 1)
        birds = st.number_input("Total Birds", value=1000)
        mortality = st.number_input("Mortality Today", 0)
        bags = st.number_input("Bags Received Today", 0)
        feed_kg = st.number_input("Feed Consumed Today (kg)", 0.0)
        weight = st.number_input("Current Avg Weight (kg)", 0.0)
        
        st.divider()
        st.subheader("Standards (Target)")
        target_gain = st.number_input("Target Weight Gain/Day (kg)", value=0.065)
        target_feed = st.number_input("Target Feed/Bird/Day (kg)", value=0.150)
        
        st.divider()
        st.subheader("Production Costs (PC)")
        chick_cost = st.number_input("Chick Cost (per bird)", value=0.50)
        feed_price = st.number_input("Feed Price (per kg)", value=0.80)
        med_cost = st.number_input("Medicine/Other Costs Today", value=0.0)
        
        submit = st.form_submit_button("Analyze Performance")

    if submit:
        # FCR & Prediction
        fcr = feed_kg / (birds * weight) if weight > 0 else 0
        pred_weight = weight + (target_gain * (32 - age))
        
        # PC Calculation
        total_cost = (chick_cost * birds) + (feed_kg * feed_price) + med_cost
        cost_per_kg = total_cost / (birds * weight) if weight > 0 else 0
        
        st.header("📊 Result Analysis")
        
        # Status Check
        if weight >= (age * target_gain):
            st.success("✅ STATUS: UP TO DATE (Growth is on target)")
        else:
            st.warning("⚠️ STATUS: BEHIND TARGET (Growth is slow)")
            
        st.metric("Predicted 32-Day Weight", f"{pred_weight:.2f} kg")
        st.metric("Current Production Cost/kg", f"${cost_per_kg:.2f}")

# --- 3. INFO BUTTON (History) ---
elif menu == "Farm Info & History":
    st.title("ℹ️ Farm Information")
    st.write("Current Status Summary:")
    # This section would pull from your saved data
    st.info("Daily History Log and detailed mortality tracking would appear here.")
