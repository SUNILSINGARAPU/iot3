import streamlit as st
import time
import requests

# Optional: ThingSpeak Integration (you can disable if not needed)
THINGSPEAK_API_KEY = "YOUR_WRITE_API_KEY"  # Optional
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Streamlit Page Config
st.set_page_config(page_title="🏠 IoT Home Automation Simulator", layout="wide")
st.title("🏠 IoT Home Automation Dashboard")
st.markdown("Simulate and control smart home devices in real time!")

# -------------------------------
# DEVICE STATES (simulated)
# -------------------------------
if "devices" not in st.session_state:
    st.session_state.devices = {
        "Living Room Light": False,
        "Ceiling Fan": False,
        "Air Conditioner": False,
        "Main Door Lock": False,
        "Garden Sprinkler": False,
        "Water Pump": False,
    }

# -------------------------------
# FUNCTION TO SEND DATA TO THINGSPEAK (OPTIONAL)
# -------------------------------
def send_to_thingspeak(devices):
    try:
        params = {"api_key": THINGSPEAK_API_KEY}
        for i, (name, state) in enumerate(devices.items(), start=1):
            params[f"field{i}"] = int(state)
        response = requests.get(THINGSPEAK_URL, params=params)
        if response.status_code == 200 and response.text.strip() != "0":
            st.toast("✅ Data sent to ThingSpeak!")
        else:
            st.warning("⚠️ Failed to send to ThingSpeak.")
    except Exception as e:
        st.error(f"Error sending data: {e}")

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
st.sidebar.header("🔘 Device Controls")

for device_name in st.session_state.devices:
    st.session_state.devices[device_name] = st.sidebar.toggle(
        device_name,
        value=st.session_state.devices[device_name]
    )

# -------------------------------
# ROOM LAYOUT DISPLAY
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💡 Living Room")
    st.image(
        "https://img.icons8.com/fluency/96/light-on.png"
        if st.session_state.devices["Living Room Light"]
        else "https://img.icons8.com/fluency/96/light-off.png",
        caption=f"Light: {'ON' if st.session_state.devices['Living Room Light'] else 'OFF'}"
    )

    st.image(
        "https://img.icons8.com/fluency/96/fan.png"
        if st.session_state.devices["Ceiling Fan"]
        else "https://img.icons8.com/color/96/no-fan.png",
        caption=f"Fan: {'ON' if st.session_state.devices['Ceiling Fan'] else 'OFF'}"
    )

with col2:
    st.subheader("❄️ Bedroom")
    st.image(
        "https://img.icons8.com/fluency/96/air-conditioner.png"
        if st.session_state.devices["Air Conditioner"]
        else "https://img.icons8.com/color/96/air-conditioner-off.png",
        caption=f"AC: {'ON' if st.session_state.devices['Air Conditioner'] else 'OFF'}"
    )

    st.image(
        "https://img.icons8.com/fluency/96/door-opened.png"
        if st.session_state.devices["Main Door Lock"]
        else "https://img.icons8.com/fluency/96/door-closed.png",
        caption=f"Door: {'Unlocked' if st.session_state.devices['Main Door Lock'] else 'Locked'}"
    )

with col3:
    st.subheader("🌿 Garden Area")
    st.image(
        "https://img.icons8.com/fluency/96/sprinkler.png"
        if st.session_state.devices["Garden Sprinkler"]
        else "https://img.icons8.com/color/96/no-water.png",
        caption=f"Sprinkler: {'ON' if st.session_state.devices['Garden Sprinkler'] else 'OFF'}"
    )

    st.image(
        "https://img.icons8.com/fluency/96/water-pump.png"
        if st.session_state.devices["Water Pump"]
        else "https://img.icons8.com/color/96/no-pump.png",
        caption=f"Water Pump: {'ON' if st.session_state.devices['Water Pump'] else 'OFF'}"
    )

# -------------------------------
# STATUS SUMMARY
# -------------------------------
st.markdown("---")
st.subheader("📊 Current Device Status")
status_table = {
    "Device": list(st.session_state.devices.keys()),
    "Status": ["ON ✅" if state else "OFF ❌" for state in st.session_state.devices.values()]
}
st.table(status_table)

# -------------------------------
# SEND TO THINGSPEAK BUTTON
# -------------------------------
if st.button("☁️ Send Status to ThingSpeak (Optional)"):
    send_to_thingspeak(st.session_state.devices)

# -------------------------------
# AUTO REFRESH (optional)
# -------------------------------
time.sleep(1)
