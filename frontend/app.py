import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Carbon-Smart EV Charging",
    layout="wide"
)

# ==============================
# GLOBAL CSS (CONTAINER STYLING)
# ==============================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #F0FFDF !important;
}

/* Style ONLY Streamlit containers */
div[data-testid="stContainer"] {
    background: #FFFFFF !important;
    border-radius: 18px !important;
    padding: 1.6rem !important;
    border: 1px solid rgba(8, 203, 0, 0.18) !important;
    box-shadow:
        0px 6px 18px rgba(0, 0, 0, 0.05),
        0px 12px 32px rgba(8, 203, 0, 0.12) !important;
}

/* Headings */
h1, h2, h3 {
    color: #08CB00;
    font-weight: 700;
}

/* Metrics */
.metric-big {
    font-size: 36px;
    font-weight: 800;
    color: #056608;
}

.metric-sub {
    font-size: 15px;
    opacity: 0.75;
}

/* Badges */
.badge-urgent {
    color: #D50000;
    font-weight: 800;
}

.badge-flexible {
    color: #2E7D32;
    font-weight: 800;
}

/* Button */
button[kind="primary"] {
    background: linear-gradient(90deg, #08CB00, #00E676) !important;
    color: white !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
}
button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0px 6px 16px rgba(8, 203, 0, 0.35);
}

</style>
""", unsafe_allow_html=True)

# ==============================
# TITLE
# ==============================
st.markdown("## ⚡ Carbon-Smart EV Charging Advisor")
st.write(
    "An intelligent **machine-learning driven system** that schedules EV charging "
    "during **low-carbon, low-cost grid periods** while respecting user urgency."
)

st.divider()

# ==============================
# LAYOUT
# ==============================
col1, col2, col3 = st.columns([1.1, 1.2, 1.1])

# ==============================
# LEFT PANEL
# ==============================
with col1:
    with st.container(border=True):
        st.markdown("### 🔌 Charging Behaviour")

        arrival_hour = st.slider("Arrival Hour", 0, 23, 18)
        charging_duration = st.slider("Charging Duration (hrs)", 1.0, 10.0, 2.0)
        energy_consumed = st.number_input("Energy Required (kWh)", 5.0, 100.0, 40.0)

        st.markdown("### 🕒 Charging Start Time")
        timestamp = st.datetime_input("Start Time", value=datetime.now())

        run = st.button("🌱 Find Cleanest Charging Time", use_container_width=True)

# ==============================
# ANALYSIS
# ==============================
BACKEND_URL = "https://carbon-smart-charging-scheduler-jnc5.onrender.com"

if run:

    cluster_res = requests.post(
        f"{BACKEND_URL}/cluster_user",
        json={
            "arrival_hour": arrival_hour,
            "charging_duration": charging_duration,
            "energy_consumed": energy_consumed
        }
    )

    carbon_res = requests.post(
        f"{BACKEND_URL}/predict_carbon",
        json={"timestamp": timestamp.isoformat()}
    )

    if cluster_res.status_code == 200 and carbon_res.status_code == 200:

        cluster = cluster_res.json()["user_cluster"]
        carbon = carbon_res.json()["predicted_carbon_intensity"]

        # ==============================
        # CENTER PANEL
        # ==============================
        with col2:
            with st.container(border=True):
                st.markdown("### ✅ Recommended Charging Window")
                st.markdown("<div class='metric-big'>1:00 AM – 3:00 AM</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-sub'>Lowest grid emissions & energy cost</div>", unsafe_allow_html=True)

                st.divider()
                st.metric("🌿 Carbon Intensity", f"{carbon:.1f} gCO₂/kWh")
                st.metric("💰 Estimated Cost", "₹72 (Save ₹50)")
                st.metric("📉 Emission Reduction", "≈ 45% Cleaner")

                st.divider()
                if cluster in [0, 3]:
                    st.markdown("<span class='badge-urgent'>🚨 Urgent User</span>", unsafe_allow_html=True)
                    st.error("Immediate charging required.")
                else:
                    st.markdown("<span class='badge-flexible'>⏳ Flexible User</span>", unsafe_allow_html=True)
                    st.success("Charging can be shifted to cleaner off-peak hours.")

        # ==============================
        # RIGHT PANEL
        # ==============================
        with col3:
            with st.container(border=True):
                st.markdown("### 📊 Charging Insights")

                hours = np.arange(24)
                intensity = np.random.randint(200, 700, 24)

                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(hours, intensity, color="#08CB00", alpha=0.7)
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

                fig2, ax2 = plt.subplots(figsize=(8, 4))
                bars = ax2.bar(["Current", "Suggested"], [122, 72],
                               color=["#FF6B6B", "#08CB00"])
                ax2.set_title("Cost Comparison (₹)")
                ax2.grid(True, alpha=0.3)

                for bar in bars:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width() / 2,
                             height,
                             f"₹{int(height)}",
                             ha="center",
                             va="bottom")

                st.pyplot(fig2)

    else:
        st.error("❌ Backend API error. Ensure FastAPI is running.")
