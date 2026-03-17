import streamlit as st
import pandas as pd
import datetime

# --- APP CONFIG & DESIGN ---
st.set_page_config(page_title="PoultryIntel Pro", page_icon="🐔", layout="wide")

# Custom CSS for a "Real App" feel
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🐔 Poultry Intelligence System")
st.info("Tracking Day 1 to Day 32 Performance")

# --- SIDEBAR INPUTS ---
st.sidebar.header("📝 Daily Entry")
with st.sidebar.form("daily_entry"):
    date = st.date_input("Select Date", datetime.date.today())
    age = st.number_input("Bird Age (Days)", 1, 35, 1)
    chicks_started = st.number_input("Total Chicks Started", 100, 50000, 1000)
    mortality_today = st.number_input("Mortality (Today)", 0, 500, 0)
    feed_used = st.number_input("Feed Used (kg Today)", 0.0, 5000.0, 0.0)
    current_avg_weight = st.number_input("Avg Bird Weight (kg)", 0.0, 4.0, 0.04)
    med_used = st.text_input("Medicine Administered", "None")
    
    submitted = st.form_submit_button("Save & Analyze")

# --- CALCULATIONS & ALGORITHM ---
# Logic: Cumulative Feed & Mortality (In a real app, these pull from a database)
total_mortality = mortality_today # Placeholder for sum of database
live_birds = chicks_started - total_mortality
total_feed = feed_used # Placeholder for sum of database

# FCR Algorithm
total_biomass = live_birds * current_avg_weight
fcr = total_feed / total_biomass if total_biomass > 0 else 0

# 32-Day Prediction Algorithm (Gompertz-style linear approximation)
days_to_go = 32 - age
growth_rate = 0.065 # Standard 65g/day for modern broilers
predicted_weight_32 = current_avg_weight + (growth_rate * days_to_go)

# --- DASHBOARD DISPLAY ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Live Bird Count", f"{live_birds:,}")
with col2:
    color = "normal" if fcr <= 1.6 else "inverse"
    st.metric("Current FCR", f"{fcr:.2f}", delta="-0.02", delta_color=color)
with col3:
    st.metric("Avg Weight", f"{current_avg_weight} kg")
with col4:
    st.metric("Target (Day 32)", f"{predicted_weight_32:.2f} kg")

# --- VISUAL ANALYSIS ---
st.divider()
st.subheader("📊 Production Analysis")
tab1, tab2 = st.tabs(["Growth Forecast", "Medicine Log"])

with tab1:
    # Create a simple trend line
    chart_data = pd.DataFrame({
        'Day': [age, 32],
        'Weight (kg)': [current_avg_weight, predicted_weight_32]
    }).set_index('Day')
    st.line_chart(chart_data)
    st.write(f"**Insight:** At current FCR of {fcr:.2f}, you will need approximately {predicted_weight_32 * live_birds * fcr:.0f} kg of feed to reach harvest.")

with tab2:
    st.write(f"**Last Medicine:** {med_used} on Day {age}")
    st.write("Schedule: Day 1-5 (Glucose/Vitamins), Day 14 (Gumboro), Day 21 (Lasota)")
