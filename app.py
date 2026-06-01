# =====================================================
# AI AIRCRAFT EMERGENCY EVACUATION SYSTEM
# CORE OPTIMIZATION & FUSELAGE PATHFINDING ENGINE
# =====================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import time
import pandas as pd
import heapq

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

import streamlit as st

# 1. 🛠️ Assign your own voice detector's output here
# Replace the default string below with the variable your actual voice detector updates.
if "current_voice_command" not in st.session_state:
    st.session_state.current_voice_command = "nominal"  # Default safe green state

# 2. 🚨 Main Logic Engine (Trips to True if 'fire' or 'smoke' is detected)
detected_text = st.session_state.current_voice_command.lower()
is_crisis = "fire" in detected_text or "smoke" in detected_text

# Dynamic Theme Variables Setup
accent_color = "#ff3366" if is_crisis else "#00ffcc"
status_text = "CRITICAL HAZARD DETECTED" if is_crisis else "NOMINAL"
progress_value = 35 if is_crisis else 100


# =========================================================================
# 📦 3. Sidebar UI Layout (Keeps elements structurally locked to the side)
# =========================================================================

with st.sidebar:
    
    # Radar System Header Title
    st.markdown(f"""
        <h3 style='color: {accent_color}; font-size: 1.15rem; margin-bottom: 2px; font-family: sans-serif; font-weight: 700;'>
            📡 Fleet Telemetry Radar System
        </h3>
    """, unsafe_allow_html=True)

    # Dynamic CSS-Animated Radar Matrix
    radar_html = f"""
    <div class="radar-container">
        <div class="radar-sweep"></div>
        <div class="radar-circle c1"></div>
        <div class="radar-circle c2"></div>
        <div class="radar-cross-h"></div>
        <div class="radar-cross-v"></div>
        <div class="fleet-dot f1"></div>
        <div class="fleet-dot f2"></div>
        <div class="fleet-dot f3"></div>
    </div>
    <style>
    .radar-container {{ 
        position: relative; 
        width: 160px; 
        height: 160px; 
        background: radial-gradient(circle, rgba(10,17,32,1) 0%, rgba(2,6,18,1) 100%); 
        border: 2px solid {accent_color}; 
        border-radius: 50%; 
        margin: 15px auto; 
        overflow: hidden; 
        box-shadow: 0 0 15px {accent_color}33; 
    }}
    .radar-sweep {{ 
        position: absolute; 
        width: 100%; 
        height: 100%; 
        background: conic-gradient(from 0deg, {accent_color}00 40%, {accent_color}cc 100%); 
        border-radius: 50%; 
        animation: sweep 2.5s linear infinite; 
        transform-origin: center; 
    }}
    .radar-circle {{ position: absolute; border: 1px dashed {accent_color}44; border-radius: 50%; top: 50%; left: 50%; transform: translate(-50%, -50%); }}
    .c1 {{ width: 50px; height: 50px; }} 
    .c2 {{ width: 100px; height: 100px; }}
    .radar-cross-h {{ position: absolute; top: 50%; width: 100%; height: 1px; background: {accent_color}22; }}
    .radar-cross-v {{ position: absolute; left: 50%; width: 1px; height: 100%; background: {accent_color}22; }}
    .fleet-dot {{ position: absolute; width: 6px; height: 6px; background: #ffffff; border-radius: 50%; box-shadow: 0 0 8px #ffffff; animation: blink 1.2s infinite; }}
    .f1 {{ top: 45px; left: 55px; background: {accent_color}; box-shadow: 0 0 10px {accent_color}; }} 
    .f2 {{ top: 105px; left: 115px; background: #ffffff; }} 
    .f3 {{ top: 125px; left: 45px; background: #f59e0b; }}
    @keyframes sweep {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    @keyframes blink {{ 0%, 100% {{ opacity: 0.3; }} 50% {{ opacity: 1; }} }}
    </style>
    """
    st.markdown(radar_html, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Dynamic Progress Status Component
    st.markdown("<p style='margin-bottom:4px; font-size:0.85rem; color:#94a3b8; font-family:sans-serif;'>📊 Evacuation Progress</p>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="width: 100%; background-color: #1e293b; border-radius: 6px; height: 12px; margin-bottom: 12px; border: 1px solid #334155; overflow: hidden;">
            <div style="width: {progress_value}%; background: {accent_color}; height: 100%; border-radius: 5px; transition: width 0.6s ease-in-out;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-top: -6px; font-family: monospace; color: #cbd5e1;">
            <span>Status: <b style="color: {accent_color};">{status_text}</b></span>
            <b style="color: #ffffff;">{progress_value}% Saved</b>
        </div>
    """, unsafe_allow_html=True)

    # 🎛️ Manual Simulation Controls (For testing purposes only)
    st.markdown("---")
    if st.button("🚨 Simulate: 'Fire' / 'Smoke' Command"):
        st.session_state.current_voice_command = "fire"
        st.rerun()
    if st.button("🔄 Simulate: 'Clear' / Nominal State"):
        st.session_state.current_voice_command = "nominal"
        st.rerun()
#ADD THIS BLOCK RIGHT HERE BEFORE PAGE CONFIGURATION 
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "🚨 Flight Safety Copilot Online. Ask me anything about cabin bottlenecks, hazard vectors, or emergency routing."}
    ]
# =========================================================
# 1. PAGE CONFIGURATION & EMERGENCY HIGH-VISIBILITY STYLES
# =========================================================
st.set_page_config(
    page_title="Flight Safety Evac Station",
    page_icon="🚨",
    layout="wide"
)

# Premium Aerospace High-Glow UI Overlays
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(1, 4, 10, 0.92), rgba(2, 8, 18, 0.96)), 
                    url('https://images.unsplash.com/photo-1540962351504-03099e0a754b?q=80&w=2000&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(0, 255, 204, 0.02) 50%, transparent 50%),
                    linear-gradient(90deg, rgba(0, 255, 204, 0.02) 50%, transparent 50%);
        background-size: 5px 5px; pointer-events: none; z-index: 0;
    }
    .stApp::after {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(to bottom, transparent, rgba(0, 255, 204, 0.05) 50%, transparent);
        animation: radarSweep 5s infinite linear; pointer-events: none; z-index: 0;
    }
    @keyframes radarSweep {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    @keyframes structuralShine {
        0% { transform: translateX(-160%) rotate(45deg); }
        100% { transform: translateX(160%) rotate(45deg); }
    }
    @keyframes buttonNeonPulse {
        0% { box-shadow: 0 0 25px rgba(0, 255, 204, 0.5), inset 0 0 12px rgba(0, 255, 204, 0.3); }
        50% { box-shadow: 0 0 60px rgba(57, 255, 20, 1), inset 0 0 25px rgba(57, 255, 20, 0.5); }
        100% { box-shadow: 0 0 25px rgba(0, 255, 204, 0.5), inset 0 0 12px rgba(0, 255, 204, 0.3); }
    }
    .premium-glass-hero {
        background: rgba(4, 20, 40, 0.75); border: 2px solid rgba(0, 255, 204, 0.8);
        border-radius: 20px; padding: 35px; margin-bottom: 30px;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.95), 0 0 50px rgba(0, 255, 204, 0.45);
        backdrop-filter: blur(35px); -webkit-backdrop-filter: blur(35px); position: relative; overflow: hidden;
    }
    .shine-key {
        position: relative; overflow: hidden; backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
        padding: 18px 24px; border-radius: 14px; font-size: 1rem; color: #ffffff; font-weight: 800;
        letter-spacing: 1px; text-shadow: 0 0 15px rgba(255, 255, 255, 0.6);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); display: flex; align-items: center; gap: 12px;
    }
    .shine-key::after {
        content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.4) 50%, rgba(255,255,255,0) 100%);
        transform: rotate(45deg); animation: structuralShine 3s infinite ease-in-out;
    }
    .shine-key:hover { transform: translateY(-5px) scale(1.02); filter: brightness(1.3); }
    .key-route { background: rgba(0, 255, 204, 0.12); border: 2px solid #00ffcc; box-shadow: 0 0 30px rgba(0, 255, 204, 0.4); }
    .key-fire { background: rgba(255, 51, 102, 0.12); border: 2px solid #ff3366; box-shadow: 0 0 30px rgba(255, 51, 102, 0.4); }
    .key-panic { background: rgba(250, 192, 21, 0.12); border: 2px solid #fac015; box-shadow: 0 0 30px rgba(250, 192, 21, 0.4); }
    .key-hull { background: rgba(57, 255, 20, 0.12); border: 2px solid #39ff14; box-shadow: 0 0 30px rgba(57, 255, 20, 0.4); }

    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00ffcc 0%, #39ff14 50%, #10b981 100%);
        background-size: 200% auto; color: #010408 !important; font-weight: 900; font-size: 18px;
        text-transform: uppercase; letter-spacing: 4px; border: 2px solid rgba(255, 255, 255, 0.7);
        border-radius: 16px; padding: 1.4rem 3rem; animation: buttonNeonPulse 2.5s infinite ease-in-out;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); width: 100%; margin-top: 20px;
    }
    div.stButton > button:first-child:hover { background-position: right center; transform: scale(1.04); text-shadow: 0 0 20px rgba(255,255,255,0.9); }
    section[data-testid="stSidebar"] { background-color: rgba(2, 8, 18, 0.98) !important; border-right: 3px solid rgba(0, 255, 204, 0.7); box-shadow: 15px 0 50px rgba(0, 255, 204, 0.3); }
    div[data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: 800 !important; text-shadow: 0 0 20px rgba(0, 255, 204, 0.6); }
    div[data-testid="stMetricLabel"] { color: #e2e8f0 !important; letter-spacing: 1px; }
    div[data-testid="stMetric"] { background: rgba(4, 16, 32, 0.75); border: 1px solid rgba(0, 255, 204, 0.35); border-radius: 12px; padding: 12px; box-shadow: 0 0 20px rgba(0, 255, 204, 0.15); }
    .stSelectbox, .stSlider, .stCheckbox, .stTextInput { background: rgba(4, 16, 32, 0.4); padding: 8px; border-radius: 8px; margin-bottom: 8px; }
    .telemetry-card { background: rgba(4, 20, 42, 0.85); border: 1px solid rgba(0, 255, 204, 0.4); padding: 20px; border-radius: 14px; box-shadow: 0 0 25px rgba(0, 255, 204, 0.15); }
    .telemetry-label { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }
    .telemetry-value { font-size: 1.15rem; color: #ffffff; font-weight: 700; margin-bottom: 15px; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
    </style>
""", unsafe_allow_html=True)

# Top Banner Header Build
st.markdown("""
<div class="premium-glass-hero">
    <h1 style='color: #00ffcc; margin-top:0; margin-bottom: 10px; font-weight:900; text-shadow: 0 0 35px rgba(0,255,204,0.9); font-size: 2.8rem; letter-spacing: 1px;'>🚨 Flight Safety Evac Station</h1>
    <p style='color: #cbd5e1; font-size: 1.25rem; margin-bottom: 28px; font-weight: 500; text-shadow: 0 0 10px rgba(0,0,0,0.5);'>Next-generation pathfinding architecture and interactive fuselage topology matrix.</p>
    <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px;'>
        <div class="shine-key key-route">⚡ Dynamic Cost A* Routing</div>
        <div class="shine-key key-fire">🔥 Adaptive Thermal Mitigation</div>
        <div class="shine-key key-panic">⚠️ Crew Influence Smoothing</div>
        <div class="shine-key key-hull">🛩️ Interactive 3D Hull Matrix</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 2. GLOBAL ENVIRONMENTAL TUNING & DIMENSIONS
# =========================================================
# This section allows flight crew to customize the physical deck 
# layout depending on the active aircraft model being simulated.

st.markdown("<h3 style='color: #f97316;'>✈️ Aircraft Deck Layout Configurator</h3>", unsafe_allow_html=True)


# 2.1 Preset Aircraft Templates for Quick Initialization
aircraft_type = st.selectbox(
    "Select Active Aircraft Fleet Model:",
    ["Standard Narrowbody (737/A320 Style)", "Regional Commuter Jet", "Custom Grid Layout"],
    help="Select a preset layout configuration or choose 'Custom Grid Layout' to manually adjust rows and aisles."
)

# 2.2 Dynamic Geometry Adjustments based on Selection
if aircraft_type == "Standard Narrowbody (737/A320 Style)":
    ROWS = 25
    COLS = 7       # 3 seats | 1 aisle | 3 seats
    aisle_index = 3
elif aircraft_type == "Regional Commuter Jet":
    ROWS = 15
    COLS = 5       # 2 seats | 1 aisle | 2 seats
    aisle_index = 2
else:
    # Custom adjustments for flexibility
    col1, col2 = st.columns(2)
    with col1:
        ROWS = st.number_input("Total Cabin Rows (Length)", min_value=5, max_value=40, value=20, step=1)
    with col2:
        COLS = st.number_input("Total Structural Columns (Width)", min_value=3, max_value=11, value=7, step=2)
    aisle_index = COLS // 2


# 2.3 User-Friendly Emergency Exit Valve Configuration
st.markdown("---")
st.markdown("#### 🚪 Active Egress Door Assignments")
st.info("💡 Exits are mapped to the forward cabin boundary by default. Adjust which doors are armed below.")

exit_col1, exit_col2 = st.columns(2)

with exit_col1:
    arm_left_door = st.toggle("Arm Forward Left Exit (Door 1L)", value=True)
    # Map coordinates safely: Forward-most row on the far left column
    LEFT_EXIT = (ROWS - 1, 0) if arm_left_door else None
    
    if LEFT_EXIT:
        st.caption(f"🟢 Door 1L Armed at Grid Coordinate: [Row {ROWS}, Col 1]")
    else:
        st.caption("🔴 Door 1L disarmed/blocked by operational failure.")

with exit_col2:
    # The right exit option provides an easy override for the "blocked_exit" setting
    arm_right_door = st.toggle("Arm Forward Right Exit (Door 1R)", value=not st.session_state.get('blocked_exit', False))
    # Map coordinates safely: Forward-most row on the far right column
    RIGHT_EXIT = (ROWS - 1, COLS - 1) if arm_right_door else None
    
    if RIGHT_EXIT:
        st.caption(f"🟢 Door 1R Armed at Grid Coordinate: [Row {ROWS}, Col {COLS}]")
    else:
        st.caption("🔴 Door 1R disarmed/blocked by operational failure.")

# Safety Fallback: Ensure at least one exit pathway remains active to avoid algorithm crashes
if LEFT_EXIT is None and RIGHT_EXIT is None:
    st.error("🚨 CRITICAL SAFETY RISK: All main emergency exit doors have been closed! Defaulting to Door 1L as an emergency backup path.")
    LEFT_EXIT = (ROWS - 1, 0)

# =========================================================
# 3. SIDEBAR PARAMETER SELECTION (CREW QUICK-CONTROL SIDEBAR)
# =========================================================
st.sidebar.markdown("<h2 style='color: #f97316; font-size: 1.5rem; font-weight:700;'>📋 EMERGENCY CONTROL PANEL</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #94a3b8; font-size: 0.85rem; margin-top:-10px;'>Adjust flight manifests and real-time cabin hazards below.</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 3.1 Onboard Manifest Settings
with st.sidebar.expander("👤 Passenger Load & Behavior", expanded=True):
    num_passengers = st.slider(
        "Total Passengers Onboard", 
        10, 150, 70,
        help="Set the active passenger count currently seated inside the aircraft cabin layout."
    )
    panic_ratio = st.slider(
        "Highly Anxious/Panicked PAX (%)", 
        0, 100, 30,
        help="The percentage of passengers experiencing severe anxiety, which causes erratic movement or bottlenecks."
    )
    simulation_speed = st.slider(
        "Simulation Playback Speed", 
        1, 10, 5,
        help="Accelerate or decelerate the layout visual clock tracker (Higher = Faster execution)."
    )

# 3.2 Environmental Threat Matrix
with st.sidebar.expander("🔥 Cabin Hazards & Fire Conditions", expanded=False):
    visibility_condition = st.selectbox(
        "Cabin Visibility Index", 
        ["Clear", "Smoke", "Heavy Smoke"],
        help="Simulates smoke buildup inside the cabin fuselage, reducing overall walking speeds."
    )
    
    # Clean linking toggle to match our updated interactive doors from Section 2
    blocked_exit = st.checkbox(
        "Simulate Blocked Right Exit (Door 1R)", 
        value=st.session_state.get('blocked_exit', False),
        help="Forcibly seal Door 1R to test single-exit congestion and pipeline stress."
    )
    
    st.markdown("---")
    enable_fire = st.checkbox(
        "Simulate Active Fire Outbreak", 
        value=False,
        help="Turn on a spreading thermal hazard that blocks seat lanes dynamically over time."
    )
    
    # Conditional visibility: Only show fire positioning adjustments if fire is active
    if enable_fire:
        st.warning("🔥 Fire Hazard Active: Choose starting cabin coordinates.")
        fire_start_row = st.slider(
            "Fire Origin (Seat Row Position)", 
            1, ROWS, min(5, ROWS),
            help="Select the row where the structural fire scenario breaks out."
        ) - 1 # Adjusted internally for 0-indexed arrays
        
        fire_start_col = st.slider(
            "Fire Origin (Cabin Column Position)", 
            1, COLS, min(3, COLS),
            help="Select the cross-section column position where the fire starts."
        ) - 1 # Adjusted internally for 0-indexed arrays
        
        fire_spread_rate = st.slider(
            "Fire Spreading Velocity Factor", 
            0.05, 0.50, 0.15,
            help="How quickly the thermal fire zone expands into adjacent cabin seats every simulation frame."
        )
    else:
        # Default fallbacks if box is unchecked to keep background threads safe
        fire_start_row = 0
        fire_start_col = 0
        fire_spread_rate = 0.0

# 3.3 Physical Structural Impedance
with st.sidebar.expander("🧳 Cabin Aisle Obstructions", expanded=False):
    spawn_debris = st.checkbox(
        "Simulate Fallen Overhead Luggage", 
        value=False,
        help="Scatter dropped bags or loose galley debris across the main central aisle to mimic realistic crash conditions."
    )
    if spawn_debris:
        debris_count = st.slider(
            "Number of Blocked Aisle Grid Points", 
            1, 15, 4,
            help="The total number of central aisle floor coordinates completely sealed by debris mounds."
        )
    else:
        debris_count = 0

# 3.4 Crew Safety Countermeasures
with st.sidebar.expander("🧑‍✈️ Aviation Crew Assets", expanded=False):
    num_crew = st.slider(
        "Active Flight Attendants Deployed", 
        0, 5, 2,
        help="Number of crew marshals guiding passengers to safe doors and reducing localized panic vectors."
    )
    crew_influence_radius = st.slider(
        "Crew Command Range (Radius Grid)", 
        1, 5, 2,
        help="The physical distance a flight attendant's commands reach to settle anxiety and speed up local movement."
    )

st.sidebar.markdown("<br>", unsafe_allow_html=True)


# =========================================================================
# 👇 COPY AND PASTE THIS VOICE RADAR PANEL CODE RIGHT HERE 👇
# =========================================================================
import streamlit as st
import streamlit.components.v1 as components

# কাস্টম কম্পোনেন্ট ফাংশন (যা সঠিক নিয়মে জাভাস্ক্রিপ্ট থেকে ডেটা রিসিভ করবে)
def custom_voice_input(html_code, key=None):
    st.session_state[key] = st.session_state.get(key, "")
    components.html(html_code, height=110, scrolling=False)

with st.sidebar.expander("🎙️ AI Safety Voice Assistant", expanded=False):
    st.markdown("<p style='color: #cbd5e1; font-size: 0.85rem; margin-bottom: 12px;'>🗣️ Speak into your mic to input instructions (e.g., 'Fire', 'Smoke', 'Clear').</p>", unsafe_allow_html=True)
    
    # Session state variable initialization
    if "voice_command_state" not in st.session_state:
        st.session_state.voice_command_state = ""

    # HTML5 Web Speech API + Professional Dual-Tone Siren System
    voice_component_html = """
    <div style="background: rgba(15, 23, 42, 0.6); padding: 10px; border-radius: 8px; border: 1px solid rgba(0, 255, 204, 0.4); text-align: center;">
        <button id="mic_btn" style="background: linear-gradient(135deg, #00ffcc 0%, #10b981 100%); border: none; color: #010408; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; transition: 0.3s;">
            🔴 Activate Voice Command
        </button>
        <p id="status_log" style="color: #94a3b8; font-size: 0.8rem; margin-top: 8px; margin-bottom: 0;">Microphone status: Idle</p>
    </div>

    <script>
        const micBtn = document.getElementById('mic_btn');
        const statusLog = document.getElementById('status_log');
        let audioCtx = null;
        let osc1 = null;
        let osc2 = null;
        let gainNode = null;
        let modulator = null;
        let isSirenPlaying = false;
        
        // 🔊 প্রফেশনাল ডুয়াল-টোন সাইরেন জেনারেটর (Industrial Air-Raid Siren Effect)
        function startProfessionalSiren() {
            if (isSirenPlaying) return;
            
            try {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                
                // মেইন ২ টি অসিলেটর (ডুয়াল টোনের জন্য)
                osc1 = audioCtx.createOscillator();
                osc2 = audioCtx.createOscillator();
                gainNode = audioCtx.createGain();
                
                // সাইরেনের ওঠানামা (Wailing Effect) তৈরি করার জন্য মডুলেটর
                modulator = audioCtx.createOscillator();
                let modulatorGain = audioCtx.createGain();
                
                // কনফিগারেশন
                osc1.type = 'sawtooth';  // তীক্ষ্ণ সাইরেন টোন
                osc2.type = 'triangle';  // গম্ভীর বেস টোন
                
                osc1.frequency.setValueAtTime(440, audioCtx.currentTime); // Base Freq 1
                osc2.frequency.setValueAtTime(444, audioCtx.currentTime); // Base Freq 2 (Slightly detuned for thickness)
                
                modulator.frequency.value = 1.5; // প্রতি সেকেন্ডে ১.৫ বার সাউন্ড আপ-ডাউন করবে
                modulatorGain.gain.value = 150;  // সাউন্ড কতটা উঁচুতে উঠবে (Pitch variation range)
                
                // কানেকশনস
                modulator.connect(modulatorGain);
                modulatorGain.connect(osc1.frequency);
                modulatorGain.connect(osc2.frequency);
                
                osc1.connect(gainNode);
                osc2.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                
                // ভলিউম সেটআপ (যাতে কান ফেটে না যায়)
                gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime);
                
                // স্টার্ট সাইরেন
                osc1.start();
                osc2.start();
                modulator.start();
                isSirenPlaying = true;
                
            } catch(e) {
                console.log("Audio block bypass error: ", e);
            }
        }

        // সাইরেন সম্পূর্ণ বন্ধ করার ফাংশন
        function stopProfessionalSiren() {
            if (!isSirenPlaying) return;
            try {
                osc1.stop();
                osc2.stop();
                modulator.stop();
                
                osc1.disconnect();
                osc2.disconnect();
                modulator.disconnect();
                gainNode.disconnect();
            } catch(e) {
                console.log(e);
            }
            isSirenPlaying = false;
        }
        
        // Safety Fallback Check for Browser Speech Support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            statusLog.innerText = "❌ Browser does not support speech recognition.";
            micBtn.style.opacity = 0.5;
            micBtn.disabled = true;
        } else {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.lang = 'en-US';
            recognition.interimResults = false;

            micBtn.addEventListener('click', () => {
                recognition.start();
                statusLog.innerText = "🎙️ Listening to cabin vectors...";
                micBtn.style.background = "#ff3366";
                micBtn.innerText = "🛑 Recording Active...";
            });

            recognition.onresult = (event) => {
                const speechToText = event.results[0][0].transcript;
                statusLog.innerText = "✅ Parsed: " + speechToText;
                
                const lowerText = speechToText.toLowerCase();
                
                // 🚨 জাদুকরী লজিক: "Fire" অথবা "Smoke" সনাক্ত হলে রিয়েল সাইরেন বাজবে
                if (lowerText.includes('fire') || lowerText.includes('smoke')) {
                    startProfessionalSiren();
                } 
                // 🟢 "Clear" বললে সাথে সাথে সাইরেন অফ হবে
                else if (lowerText.includes('clear')) {
                    stopProfessionalSiren();
                }
                
                // Return text safely back to Streamlit data layer
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: speechToText
                }, '*');
            };

            recognition.onspeechend = () => {
                recognition.stop();
                resetButton();
            };

            recognition.onerror = (event) => {
                statusLog.innerText = "⚠️ Signal Error: " + event.error;
                resetButton();
            };

            function resetButton() {
                micBtn.style.background = "linear-gradient(135deg, #00ffcc 0%, #10b981 100%)";
                micBtn.innerText = "🔴 Activate Voice Command";
            }
        }
    </script>
    """
    
    # কাস্টম ফাংশন কল
    custom_voice_input(voice_component_html, key="voice_radar_component")
    
    # সেশন স্টেট ট্র্যাকিং
    if hasattr(st, "session_state") and "voice_radar_component" in st.session_state:
        val = st.session_state["voice_radar_component"]
        if val and "DeltaGenerator" not in str(val):
            st.session_state.voice_command_state = str(val).strip()

    # স্ক্রিনে রেসপন্স এবং কার্ডের ডিজাইন
    if st.session_state.voice_command_state:
        st.markdown(f"""
            <div style="background: rgba(0, 255, 204, 0.08); border: 1px solid #00ffcc; padding: 10px; border-radius: 8px; margin-top: 10px;">
                <b style="color: #00ffcc; font-size: 0.85rem;">🛰️ Voice Telemetry Synced:</b><br>
                <span style="color: #ffffff; font-size: 0.85rem; font-family: monospace;">"{st.session_state.voice_command_state}"</span>
            </div>
        """, unsafe_allow_html=True)

        cmd_lower = st.session_state.voice_command_state.lower()
        if "fire" in cmd_lower or "smoke" in cmd_lower:
            st.error("🚨 **CRITICAL HAZARD DETECTED! AIR-RAID EVACUATION SIREN IS ACTIVE.**")
        elif "clear" in cmd_lower:
            st.success("✅ **Status Nominal: Emergency Alarm Silenced.**")

# =========================================================================
# 👆 VOICE RADAR PANEL CODE ENDS HERE 👆
# =========================================================================# 

# High-visibility warning-red color handled automatically by primary app theme definitions
start_simulation = st.sidebar.button("🚨 RUN EMERGENCY ESCAPE PATHS")
st.sidebar.markdown("---")

# 3.5 Cross-Scenario Testing Model Panel
with st.sidebar.expander("📊 Predictive Analytics Scenario Sandbox", expanded=False):
    enable_comparison = st.checkbox(
        "Activate Dual Configuration Testing",
        help="Compare two different flight profiles side-by-side using the integrated Machine Learning classifier."
    )
    if enable_comparison:
        st.caption("🔬 Compare baseline profiles to calculate bottleneck differences:")
        scenario_1 = st.selectbox("Flight Scenario Alpha Profile", ["Normal", "Fire", "Smoke", "Blocked Exit"], index=0)
        scenario_2 = st.selectbox("Flight Scenario Beta Profile", ["Normal", "Fire", "Smoke", "Blocked Exit"], index=2)

# =========================================================
# 4. LIVE SAFETY PREDICTION MACHINE LEARNING ENGINE
# =========================================================
# This section initializes the predictive AI core using random forest
# regression to analyze passenger clearance constraints in real-time.

@st.cache_resource
def train_capstone_ml_engine():
    """
    Trains the predictive safety engine using a Random Forest Regressor 
    to map physical and psychological passenger features to evacuation times.
    """
    # 4.1 Create a balanced synthetic training set representing typical flight manifests
    np.random.seed(42)
    N_samples = 1000
    
    df = pd.DataFrame({
        "Age": np.random.randint(18, 80, N_samples),
        "Walking_Speed": np.random.uniform(0.5, 2.0, N_samples), # Speed in meters per second
        "Panic_Level": np.random.randint(1, 10, N_samples),     # 1 = Calm, 10 = Severe Panic
        "Seat_Row": np.random.randint(1, 30, N_samples),        # Location relative to exits
        "Exit_Distance": np.random.randint(1, 25, N_samples)    # Total grid steps to nearest exit
    })
    
    # Mathematical baseline tracking realistic evacuation behavior constraints
    df["Evacuation_Time"] = (df["Exit_Distance"] * 2) + (df["Panic_Level"] * 3) + (80 - df["Walking_Speed"] * 20)
    
    X = df[["Age", "Walking_Speed", "Panic_Level", "Seat_Row", "Exit_Distance"]]
    y = df["Evacuation_Time"]
    
    # Split data into training and validation sets
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4.2 Initialize and fit the Ensemble Random Forest Network
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    regressor.fit(X_train, y_train)
    return regressor

# 4.3 User-Friendly Boot Status Loader
with st.spinner("🤖 Loading AI Prediction Models & Scanning Manifest Metrics..."):
    capstone_rf_model = train_capstone_ml_engine()
    # Artificial pause for visual fluid transition in the UI
    time.sleep(0.5)

# 4.4 Crew Visual Analytics Card
st.markdown("""
<div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); padding: 18px; border-radius: 8px; margin-bottom: 20px;">
    <h4 style="color: #38bdf8; margin-top: 0; margin-bottom: 8px;">🧠 Predictive AI Core Operational</h4>
    <p style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 12px;">
        The machine learning system has mapped the flight cabin profile. The evacuation times are dynamically calculated based on the following weighted passenger constraints:
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; font-size: 0.82rem; color: #94a3b8;">
        <div>🚶‍♂️ <b>Physical Mobility:</b> Walking pace vs age brackets</div>
        <div>🧠 <b>Anxiety Load:</b> Behavioral delays due to panic</div>
        <div>📐 <b>Spatial Distance:</b> Physical tile separation from armed doors</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 5. STATE ISOLATION & PASSENGER MANIFEST GENERATOR
# =========================================================
# This section isolates the memory state of the app, ensuring that 
# changes to settings cleanly re-populate the aircraft environment.

# 5.1 Initialize fundamental structural memory states inside Streamlit
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

def initialize_scenario_state():
    """
    Clears out old data and populates a new cabin state containing 
    aisle obstructions, fire origins, crew spots, and passenger traits.
    """
    # --- AISLE OBSTRUCTION PLACEMENT (DEBRIS) ---
    st.session_state.debris_positions = set()
    if spawn_debris and debris_count > 0:
        # Use a fixed seed for debris to remain consistent unless altered
        random.seed(42)
        # Place debris along the main central aisle (Aisle Column index = aisle_index)
        current_aisle = aisle_index if 'aisle_index' in locals() else 3
        while len(st.session_state.debris_positions) < debris_count:
            # Drop pieces away from exits to ensure mathematical validity
            random_row = random.randint(2, max(2, ROWS - 3))
            st.session_state.debris_positions.add((random_row, current_aisle))
        random.seed() # Release the seed back to random distribution

    # --- FIRE ENVIRONMENT INITIALIZATION ---
    st.session_state.fire_positions = set()
    if enable_fire:
        st.session_state.fire_positions.add((fire_start_row, fire_start_col))

    # --- FLIGHT ATTENDANT MARSHAL ROUTING ---
    st.session_state.crew_members = []
    current_aisle = aisle_index if 'aisle_index' in locals() else 3
    for i in range(num_crew):
        # Space out cabin crew evenly along the length of the central aisle walkway
        st.session_state.crew_members.append({
            "id": i, 
            "x": current_aisle, 
            "y": int((ROWS / (num_crew + 1)) * (i + 1))
        })

    # --- PASSENGER MANIFEST VECTOR GENERATION ---
    st.session_state.passengers = []
    for i in range(num_passengers):
        # Pick random rows away from immediate emergency doors
        row = random.randint(0, max(1, ROWS - 3))
        
        # Place passengers in valid window or middle seat columns (avoiding the exact aisle)
        valid_seating_cols = [c for c in range(COLS) if c != (aisle_index if 'aisle_index' in locals() else 3)]
        col = random.choice(valid_seating_cols) if valid_seating_cols else 0
        
        # Calculate behavioral anxiety distribution
        rand_percentage = random.randint(1, 100)
        if rand_percentage <= panic_ratio:
            panic_type = "HIGH"
        elif rand_percentage <= 70:
            panic_type = "MEDIUM"
        else:
            panic_type = "LOW"

        # Categorize physical mobility types based on aviation metrics
        accessibility = random.choices(
            ["Normal", "Elderly", "Disabled", "Wheelchair", "Injured"],
            weights=[60, 15, 10, 8, 7]
        )[0]

        # Append complete diagnostic data profile to background thread state
        st.session_state.passengers.append({
            "id": i, "x": col, "y": row, "panic": panic_type,
            "accessibility": accessibility, "evacuated": False, "delay": 0
        })
        
    st.session_state.initialized = True

# 5.2 Dynamic Triggers: Rebuild the space if not setup or if settings change
if not st.session_state.initialized or not start_simulation:
    initialize_scenario_state()

# 5.3 User-Friendly Manifest Summary Card
st.markdown("---")
st.markdown("#### 🗂️ Current Cabin Manifest Isolation Status")

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.success(f"✔️ {len(st.session_state.passengers)} Passengers Loaded into Memory Matrix")
with m_col2:
    st.info(f"🧑‍✈️ {len(st.session_state.crew_members)} Flight Attendants Stationed along Aisle")
with m_col3:
    # Manual override button allows operators to force-reset profiles instantly
    if st.button("🔄 Clear Cabin Memory & Recalibrate Manifest"):
        initialize_scenario_state()
        st.rerun()

# =========================================================
# 6. INTELLIGENT ROUTING & PATHFINDING MATRIX
# =========================================================
# This section contains the spatial mathematics used to steer passengers 
# dynamically around obstacles, smoke layers, and expanding fire zones.

def get_dynamic_cost_grid():
    """
    Constructs a structural cost map where safe paths equal 1.0, 
    congested paths cost more, and hazards approach infinite impedance.
    """
    # Create an empty map matching current aircraft cabin bounds
    cost_grid = np.ones((ROWS, COLS))
    
    # Blockages completely seal cells
    for (r, c) in st.session_state.debris_positions:
        cost_grid[r, c] = float('inf')
        
    # Fire threats block cells and radiating smoke layers penalize neighboring zones
    for (fr, fc) in st.session_state.fire_positions:
        cost_grid[fr, fc] = float('inf')
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = fr + dr, fc + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if cost_grid[nr, nc] != float('inf'):
                        cost_grid[nr, nc] += 15.0 # Thermal heat proximity cost addition

    # Multi-agent crowd friction: Seated or slowing passengers add weight to an aisle tile
    for p in st.session_state.passengers:
        if not p["evacuated"]:
            if cost_grid[p["y"], p["x"]] != float('inf'):
                cost_grid[p["y"], p["x"]] += 2.5
                
    return cost_grid

def cost_aware_astar(start, goal, cost_grid):
    """
    A* Shortest-Path algorithm adjusted to balance grid distance against hazard costs.
    """
    # Safety Check: If target door is blocked or missing, stand fast
    if goal is None:
        return []
        
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0.0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            y, x = neighbor
            
            if not (0 <= x < COLS and 0 <= y < ROWS):
                continue
                
            edge_cost = cost_grid[y, x]
            if edge_cost == float('inf'):
                continue

            temp_g = g_score[current] + edge_cost
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                # Diagonal heuristic calculation
                f_score = temp_g + (abs(y - goal[0]) + abs(x - goal[1]))
                heapq.heappush(open_set, (f_score, neighbor))
                
    return []

def get_optimal_target_exit(x, accessibility):
    """
    Steers passengers toward the closest operational exit gate based on physical traits.
    """
    # Fetch fallback global configurations safely
    left_door = globals().get('LEFT_EXIT', (ROWS - 1, 0))
    right_door = globals().get('RIGHT_EXIT', (ROWS - 1, COLS - 1))
    
    # Priority steering: Elderly or injured travelers are funneled cleanly away from hazards
    if accessibility in ["Disabled", "Wheelchair", "Elderly"] or right_door is None:
        return left_door
    if left_door is None:
        return right_door
        
    # Split routing: Otherwise, divide flow down the main aisle index splits
    current_aisle = globals().get('aisle_index', 3)
    return left_door if x <= current_aisle else right_door

def update_evacuation_step(cost_grid):
    """
    Advances every onboard passenger one grid tile along their calculated A* escape route.
    """
    occupied_positions = set()
    congestion_count = 0

    for passenger in st.session_state.passengers:
        if passenger["evacuated"]:
            continue

        cx, cy = passenger["x"], passenger["y"]
        
        # Crew Calm Radius: Flight attendants drop stress levels of nearby passengers
        for crew in st.session_state.crew_members:
            if abs(cx - crew["x"]) + abs(cy - crew["y"]) <= crew_influence_radius:
                passenger["panic"] = "LOW"

        # Chart the trajectory window
        target_exit = get_optimal_target_exit(cx, passenger["accessibility"])
        computed_path = cost_aware_astar((cy, cx), target_exit, cost_grid)

        if computed_path:
            next_step = computed_path[0]
            ny, nx = next_step[0], next_step[1]
        else:
            nx, ny = cx, cy

        # Panic Perturbation: Highly anxious passengers occasionally run off-course
        if passenger["panic"] == "HIGH" and random.random() < 0.25:
            nx = max(0, min(COLS - 1, nx + random.choice([-1, 1])))
            ny = max(0, min(ROWS - 1, ny + random.choice([-1, 1])))

        # Mobility Delays: Wheelchairs and injured passengers move on a staggered cycle
        if passenger["accessibility"] in ["Wheelchair", "Disabled", "Elderly"] and random.random() < 0.45:
            occupied_positions.add((cx, cy))
            continue

        # Physical collision avoidance: Only advance if the upcoming seat tile is clear
        if (nx, ny) not in occupied_positions and cost_grid[ny, nx] != float('inf'):
            passenger["x"], passenger["y"] = nx, ny
            occupied_positions.add((nx, ny))
        else:
            congestion_count += 1
            occupied_positions.add((cx, cy))

        # Check if the passenger crossed the threshold of the exit gate
        if target_exit and passenger["x"] == target_exit[1] and passenger["y"] == target_exit[0]:
            passenger["evacuated"] = True

    return congestion_count

def calculate_safety_score(step, congestion, high_panic_count):
    """Calculates an overall safety score out of 100 based on cabin risks."""
    score = 100
    if step > 85: score -= 25
    score -= congestion * 1.5
    score -= high_panic_count * 0.8
    if getattr(st.sidebar, 'blocked_exit', False) or globals().get('RIGHT_EXIT') is None: 
        score -= 20
    if len(st.session_state.fire_positions) > 1: 
        score -= min(30, len(st.session_state.fire_positions) * 1.8)
    if visibility_condition == "Heavy Smoke": score -= 15
    return max(0, min(int(score), 100))

def scenario_analysis_ml(scenario):
    """Evaluates arbitrary testing scenarios using the fitted Machine Learning core."""
    if scenario == "Normal":
         speed, panic, dist = 1.6, 2, 8
    elif scenario == "Fire":
         speed, panic, dist = 1.1, 8, 16
    elif scenario == "Smoke":
         speed, panic, dist = 0.9, 6, 12
    else: 
         speed, panic, dist = 1.2, 7, 22
         
    profile = pd.DataFrame([[45, speed, panic, 15, dist]], columns=["Age", "Walking_Speed", "Panic_Level", "Seat_Row", "Exit_Distance"])
    
    # Safe prediction interface block
    if 'capstone_rf_model' in globals():
        predicted_time = capstone_rf_model.predict(profile)[0]
    else:
        predicted_time = dist * 2.5
    
    congestion = int(panic * 1.8 + dist * 0.4)
    safety_index = max(10, int(100 - (panic * 5 + dist * 1.5)))
    
    return {
        "Scenario": scenario, 
        "Evacuation Time (s)": round(predicted_time, 2), 
        "Expected Bottleneck Density": congestion, 
        "Structural Safety Index": safety_index
    }

# =========================================================
# OPERATOR SYSTEM ALGORITHM EXPLANATION CARD (SIMPLIFIED)
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)

with st.expander("ℹ️ How does the Evacuation AI work? (Simple Guide)", expanded=False):
    
    # 1. Introduction
    st.markdown("### 🤖 How the AI Finds the Safest Path")
    st.markdown(
        "Think of the AI as a smart GPS for every passenger. Instead of just looking for the "
        "shortest route, it constantly checks the cabin floor for **crowds**, **smoke**, and **fire** "
        "to guide passengers along the fastest and safest path to an exit."
    )
    
    st.markdown("---")
    
    # 2. Simple Math Breakdown
    st.markdown("#### 🧭 The Safety Formula")
    st.markdown("To score a path, the AI adds up simple values for each step:")
    
    st.markdown(
        """
        * **Distance Traveled** (Steps taken from the seat)
        * **Distance to Exit** (Steps left until the door)
        * **Crowd Penalty** (Extra time added if stuck behind people)
        * **Danger Penalty** (Extra time added if walking near heat or smoke)
        """
    )
    st.caption("💡 **Rule of Thumb:** The AI always picks the path with the **lowest total score**.")

    st.markdown("---")
    
    # 3. Visual Grid Card Row (Cleaned Markdown/HTML mix for maximum readability)
    st.markdown("#### 📐 Path Difficulty Levels")
    st.markdown("Different areas of the aircraft are given different 'scores' or 'costs':")
    
    grid_html = """
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 10px; font-family: sans-serif;">
        <div style="background: rgba(34, 197, 94, 0.05); border: 1px solid #22c55e; padding: 12px; border-radius: 8px;">
            <b style="color: #4ade80;">🟢 Clear Path (Score: 1)</b><br>
            <span style="color: #cbd5e1; font-size: 0.85rem;">Empty aisles or rows. Easiest and fastest way to move.</span>
        </div>
        <div style="background: rgba(234, 179, 8, 0.05); border: 1px solid #eab308; padding: 12px; border-radius: 8px;">
            <b style="color: #facc15;">🟡 Crowded (+2.5 Penalty)</b><br>
            <span style="color: #cbd5e1; font-size: 0.85rem;">Traffic jams. Slows passengers down based on the crowd size.</span>
        </div>
        <div style="background: rgba(249, 115, 22, 0.05); border: 1px solid #ea580c; padding: 12px; border-radius: 8px;">
            <b style="color: #fb923c;">🟠 Smoke Area (+15 Penalty)</b><br>
            <span style="color: #cbd5e1; font-size: 0.85rem;">Thick smoke or heat. Passengers actively avoid these spots.</span>
        </div>
        <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid #ef4444; padding: 12px; border-radius: 8px;">
            <b style="color: #f87171;">🔴 Blocked (Infinite Penalty)</b><br>
            <span style="color: #cbd5e1; font-size: 0.85rem;">Active fire or locked exit doors. Completely impassable.</span>
        </div>
    </div>
    """
    st.markdown(grid_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 4. Crew Influence
    st.markdown("#### 🧑‍✈️ The Flight Attendant Effect")
    st.markdown(
        "When a panicking passenger gets close to a **Flight Attendant**, their status instantly "
        "changes to **Low Panic**. "
    )
    st.success(
        "✨ **What this does:** It stops the passenger from running around erratically, eliminates "
        "confusion, and helps them walk in a straight, orderly line directly toward the nearest safe exit."
    )

# =========================================================
# 7. REAL-TIME PLATFORM GEOMETRY & VISUALIZATION RENDERER
# =========================================================
# This section converts backend mathematical grid values into responsive, 
# clear 2D and 3D visual monitors for aircraft crew and coordinators.

def generate_2d_mapping_network():
    """
    Renders the live flat-grid cabin tracker displaying passengers, 
    deployed safety crew, luggage roadblocks, and fire boundaries.
    """
    fig = go.Figure()
    
    # Fetch safe structural variables dynamically from active environment setup
    current_rows = globals().get('ROWS', 20)
    current_cols = globals().get('COLS', 7)
    current_aisle = globals().get('aisle_index', 3)
    
    # 7.1 Map Out Structural Seats (Omitting the center aisle lane cleanly)
    sx, sy = [], []
    for r in range(current_rows):
        for c in range(current_cols):
            if c != current_aisle:
                sx.append(c)
                sy.append(r)
                
    fig.add_trace(go.Scatter(
        x=sx, y=sy, mode='markers', 
        marker=dict(size=14, color='#1e293b', symbol='square', line=dict(width=1.5, color='#475569')), 
        name='Passenger Seats'
    ))

    # 7.2 Overlay Aisle Obstructions (Dropped Baggage)
    if st.session_state.debris_positions:
        fig.add_trace(go.Scatter(
            x=[p[1] for p in st.session_state.debris_positions], 
            y=[p[0] for p in st.session_state.debris_positions], 
            mode='markers', 
            marker=dict(size=15, color='#f43f5e', symbol='x'), 
            name='Luggage Obstruction'
        ))

    # 7.3 Overlay Stationed Flight Attendants
    if st.session_state.crew_members:
        fig.add_trace(go.Scatter(
            x=[c["x"] for c in st.session_state.crew_members], 
            y=[c["y"] for c in st.session_state.crew_members], 
            mode='markers', 
            marker=dict(size=16, color='#38bdf8', symbol='diamond', line=dict(width=1.5, color='#ffffff')), 
            name='Crew Resource'
        ))

    # 7.4 Overlay Active Fire Thermal Boundaries
    if st.session_state.fire_positions:
        fig.add_trace(go.Scatter(
            x=[p[1] for p in st.session_state.fire_positions], 
            y=[p[0] for p in st.session_state.fire_positions], 
            mode='markers', 
            marker=dict(size=23, color='#ef4444', symbol='triangle-up', line=dict(width=1.5, color='#f97316')), 
            name='Thermal Fire Zone'
        ))

    # 7.5 Map Onboard Passengers Categorized by Real-Time Anxiety Loads
    px, py, pc = [], [], []
    for p in st.session_state.passengers:
        if not p["evacuated"]:
            px.append(p["x"])
            py.append(p["y"])
            # Green = Low Stress, Yellow = Modest Delay Risk, Red = Severe Panic Loop
            pc.append("#22c55e" if p["panic"] == "LOW" else ("#eab308" if p["panic"] == "MEDIUM" else "#ef4444"))
            
    if px:
        fig.add_trace(go.Scatter(
            x=px, y=py, mode='markers', 
            marker=dict(size=13, color=pc, line=dict(width=1, color='#ffffff')), 
            name='Onboard Passengers'
        ))

    # 7.6 Simulate Particulate Smoke Diffusion Layers
    if visibility_condition != "Clear":
        np.random.seed(101) # Locked seed prevents flickering between execution steps
        sm_x = np.random.randint(0, current_cols, 30)
        sm_y = np.random.randint(0, current_rows, 30)
        fig.add_trace(go.Scatter(
            x=sm_x, y=sm_y, mode='markers', 
            marker=dict(size=35, color='#94a3b8', opacity=0.35 if visibility_condition == "Smoke" else 0.70), 
            name='Smoke Diffusion'
        ))

    # 7.7 Dynamic Exit Indicator Placements (Recalculates based on dynamic row settings)
    left_door_active = globals().get('LEFT_EXIT') is not None
    right_door_active = globals().get('RIGHT_EXIT') is not None
    
    exit_x_coords = [0, current_cols - 1]
    exit_y_coords = [current_rows - 1, current_rows - 1]
    exit_colors = [
        "#22c55e" if left_door_active else "#ef4444", 
        "#22c55e" if right_door_active else "#ef4444"
    ]
    exit_labels = [
        "DOOR 1L (OPEN)" if left_door_active else "DOOR 1L (BLOCKED)",
        "DOOR 1R (OPEN)" if right_door_active else "DOOR 1R (BLOCKED)"
    ]

    fig.add_trace(go.Scatter(
        x=exit_x_coords, y=exit_y_coords, mode='markers+text',
        marker=dict(size=26, color=exit_colors, line=dict(width=2, color='#ffffff')),
        text=exit_labels, textposition="top center",
        textfont=dict(color="#ffffff", size=10, family="sans-serif"), showlegend=False
    ))

    fig.update_layout(
        title="📋 Live 2D Cabin Grid Monitor Feed", height=600, template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.9)',
        xaxis=dict(range=[-1, current_cols], fixedrange=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
        yaxis=dict(range=[current_rows, -1], fixedrange=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    )
    return fig


def generate_3d_fuselage_matrix():
    """
    Builds an interactive 3D spatial cylinder layout representing 
    the aircraft's actual hull geometry for advanced bottleneck visualization.
    """
    fig = go.Figure()
    current_rows = globals().get('ROWS', 20)
    current_cols = globals().get('COLS', 7)
    
    steps, segments = 35, 20
    y_range = np.linspace(-3, current_rows + 2, steps)
    t_range = np.linspace(0, 2 * np.pi, segments)
    
    Y_m, T_m = np.meshgrid(y_range, t_range)
    X_h, Z_h = np.zeros_like(Y_m), np.zeros_like(Y_m)
    
    # Model the curvature of the aircraft fuselage
    for idx, y_val in enumerate(y_range):
        scale_factor = (y_val + 3) / 3.0 if y_val < 0 else (1.0 - ((y_val - current_rows) / 2.5) if y_val > current_rows else 1.0)
        r_x, r_z = 3.6 * scale_factor, 2.2 * scale_factor
        X_h[:, idx] = (current_cols / 2) + r_x * np.cos(t_range)
        Z_h[:, idx] = 0.6 + r_z * np.sin(t_range)

    # 3D Semi-transparent Fuselage Hull
    fig.add_trace(go.Surface(
        x=X_h, y=Y_m, z=Z_h, 
        colorscale=[[0, 'rgba(249, 115, 22, 0.1)'], [1, 'rgba(30, 41, 59, 0.25)']], 
        opacity=0.25, showscale=False, hoverinfo='skip'
    ))
    
    # Extract live 3D coordinate matrices for moving passengers
    px, py, pz, colors = [], [], [], []
    for p in st.session_state.passengers:
        if not p["evacuated"]:
            px.append(p["x"])
            py.append(p["y"])
            pz.append(0.3) # Fixed height alignment near the cabin floor line
            colors.append("#22c55e" if p["panic"] == "LOW" else ("#eab308" if p["panic"] == "MEDIUM" else "#ef4444"))

    if px:
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz, mode='markers', 
            marker=dict(size=6, color=colors, line=dict(width=0.5, color='#ffffff')), 
            name='Passengers'
        ))

    fig.update_layout(
        template="plotly_dark", height=600, paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            xaxis=dict(title="Width", range=[-6, current_cols + 6], gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Row Axis", range=[-4, current_rows + 3], gridcolor='rgba(255,255,255,0.05)'),
            zaxis=dict(title="Height", range=[-3, 5], gridcolor='rgba(255,255,255,0.05)')
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig

# =========================================================
# 8. LAYOUT ARRANGEMENT & PLACEHOLDER FRAMEWORK
# =========================================================
# This section constructs the main dashboard framework, organizing 2D/3D charts,
# live metric feeds, and safety warnings into a clean, scannable interface.

# --- 1. MATHEMATICAL GENERATION FOR THE DIGITAL-TWIN AIRPLANE ---
def generate_digital_twin_airplane():
    traces = []
    
    # A. Fuselage (Main Body Cylinder)
    z_fuse = np.linspace(0, 22, 60)
    theta = np.linspace(0, 2 * np.pi, 30)
    theta_g, z_fuse_g = np.meshgrid(theta, z_fuse)
    r_fuse = 1.8 * (1 - (z_fuse_g - 11)**4 / 11**4)**0.25  # Sleek aerodynamic curve
    x_fuse_g = r_fuse * np.cos(theta_g)
    y_fuse_g = r_fuse * np.sin(theta_g)
    
    traces.append(go.Surface(
        x=x_fuse_g, y=y_fuse_g, z=z_fuse_g,
        opacity=0.18,
        colorscale=[[0, '#00f2fe'], [1, '#4facfe']], # Neon Cyan-Blue Glow
        showscale=False, hoverinfo='skip'
    ))
    
    # B. Wings (Left & Right Swept-back Wings)
    wing_span = np.linspace(1.5, 9, 20)
    wing_chord = np.linspace(0, 1, 10)
    span_g, chord_g = np.meshgrid(wing_span, wing_chord)
    
    # Right Wing calculation
    z_wing_r = 8 + 1.2 * (span_g - 1.5) + chord_g * (3 - 0.2 * span_g)
    x_wing_r = span_g
    y_wing_r = -0.2 - 0.05 * span_g + 0.1 * (1 - chord_g)
    
    # Add Right Wing
    traces.append(go.Surface(
        x=x_wing_r, y=y_wing_r, z=z_wing_r,
        opacity=0.25, colorscale=[[0, '#ff0844'], [1, '#ffb199']], # Warm Engine/Wing Glow Accent
        showscale=False, hoverinfo='skip'
    ))
    # Add Left Wing (Mirrored)
    traces.append(go.Surface(
        x=-x_wing_r, y=y_wing_r, z=z_wing_r,
        opacity=0.25, colorscale=[[0, '#ff0844'], [1, '#ffb199']],
        showscale=False, hoverinfo='skip'
    ))
    
    # C. Jet Engines (Glowing Cylinders under the wings)
    z_eng = np.linspace(8, 11, 15)
    theta_e = np.linspace(0, 2 * np.pi, 20)
    te_g, z_eng_g = np.meshgrid(theta_e, z_eng)
    r_eng = 0.6
    
    # Position engines out on the wings
    traces.append(go.Surface(
        x=3.5 + r_eng * np.cos(te_g), y=-1.0 + r_eng * np.sin(te_g), z=z_eng_g,
        opacity=0.4, colorscale=[[0, '#f12711'], [1, '#f5af19']], # Intense Engine Combustion Glow
        showscale=False, hoverinfo='skip'
    ))
    traces.append(go.Surface(
        x=-3.5 + r_eng * np.cos(te_g), y=-1.0 + r_eng * np.sin(te_g), z=z_eng_g,
        opacity=0.4, colorscale=[[0, '#f12711'], [1, '#f5af19']],
        showscale=False, hoverinfo='skip'
    ))
    
    return traces

# --- 2. STREAMLIT APP LAYOUT ---
st.set_page_config(layout="wide")

# 8.1 Primary Visual Monitor Split (Side-by-Side Viewport)
ui_col1, ui_col2 = st.columns(2)

with ui_col1:
    st.markdown("### 🗺️ Tactical Visual Feeds")
    # Isolated block container for the 2D flat layout map
    map_2d_container = st.empty()
    
    st.markdown("---")
    st.markdown("### 📊 Live Evacuation Telemetry")
    # Multi-row placeholders for key performance indicators and statistics
    metric_grid_row1 = st.empty()
    metric_grid_row2 = st.empty()  

with ui_col2:
    st.markdown("### ✈️ Spatial Cabin Geometry")
    # Isolated block container for the interactive 3D fuselage layout
    hull_3d_container = st.empty()
    
    # --- Generating Holographic Dashboard Visuals ---
    fig = go.Figure()
    
    # Add all calculated components of the airplane wireframe mesh
    airplane_traces = generate_digital_twin_airplane()
    for trace in airplane_traces:
        fig.add_trace(trace)
        
    # Generate mock passenger scatter points (spatial coordinates inside cabin)
    np.random.seed(10)
    points_count = 65
    p_z = np.random.uniform(3, 19, points_count)      # Distribution along Row Axis
    p_x = np.random.uniform(-1.1, 1.1, points_count)  # Distribution along Width Axis
    p_y = np.random.uniform(-0.8, 0.8, points_count)  # Distribution along Height Axis
    status_colors = np.random.choice(['#00ff66', '#ffaa00', '#ff0055'], points_count) # Cyberpunk palette
    
    # Plotting passenger nodes inside the mesh hull
    fig.add_trace(go.Scatter3d(
        x=p_x, y=p_y, z=p_z,
        mode='markers',
        marker=dict(
            size=5,
            color=status_colors,
            opacity=0.9,
            line=dict(width=1, color='white')
        ),
        name='Telemetry Nodes'
    ))
    
    # Layout configuration setting matching the dark HUD background
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(10,15,30,1)', # Deep cyber-navy background matching the image UI
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, b=10, t=10),
        scene=dict(
            xaxis=dict(title='Width Axis', range=[-10, 10], gridcolor='#1e293b', showbackground=False),
            yaxis=dict(title='Height Axis', range=[-5, 5], gridcolor='#1e293b', showbackground=False),
            zaxis=dict(title='Row Axis (Length)', range=[0, 24], gridcolor='#1e293b', showbackground=False),
            aspectmode='manual',
            aspectratio=dict(x=1, y=0.5, z=1.8) # Elongates layout dynamically like an actual aircraft
        ),
        showlegend=False
    )
    
    # Push the final interactive visual into its designated layout container
    hull_3d_container.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📈 Crowd Density Metrics")
    # Dedicated placeholder for bottlenecks, heatmaps, or machine learning comparisons
    density_heatmap_container = st.empty()

# 8.2 Full-Width Emergency Alert System (Placed at the bottom for high visibility)
st.markdown("<br>", unsafe_allow_html=True)
system_alert_container = st.empty()

# =========================================================
# 8.3 INITIAL CANVAS SEEDING & PRE-FLIGHT RENDERING
# =========================================================
# Populates the dashboard placeholders with base cabin networks 
# immediately upon load so the screen doesn't appear empty.

with map_2d_container:
    st.plotly_chart(
        generate_2d_mapping_network(), 
        use_container_width=True, 
        key="base_2d_static_canvas"
    )

with hull_3d_container:
    st.plotly_chart(
        generate_3d_fuselage_matrix(), 
        use_container_width=True, 
        key="base_3d_static_canvas"
    )

# Seed an initial standby notification into the dispatch alert panel
with system_alert_container:
    st.info("📌 System Standby: Adjust parameters in the left control sidebar and press 'RUN EMERGENCY ESCAPE PATHS' to begin simulation pipeline.")

# =========================================================
# 9. LIVE SIMULATION CORE FEEDBACK LOOP & ML DATA PIPELINE
# =========================================================
# This section executes the frame-by-frame cellular automata pipeline, 
# updating passenger states, fire vectors, metrics, and visual layout charts.

if start_simulation:
    max_execution_cycles = 120
    
    # 9.1 PRE-ALLOCATE METRIC COLUMNS (CRITICAL FOR VISUAL FLUIDITY)
    # Creating layout frames once outside the loop eliminates flickering and layout shifting.
    m_row1_c1, m_row1_c2, m_row1_c3, m_row1_c4 = metric_grid_row1.columns(4)
    m_row2_c1, m_row2_c2, m_row2_c3, m_row2_c4 = metric_grid_row2.columns(4)
    
    # Pre-configure unchanging structural layouts for the crowd density map
    density_heatmap_layout = dict(
        title="🔥 Dynamic Structural Density Vector Matrix", 
        template="plotly_dark", 
        height=280, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(fixedrange=True, showgrid=False),
        yaxis=dict(fixedrange=True, showgrid=False)
    )

    # 9.2 CORE TIME-STEP ANIMATION LOOP
    for tick_step in range(max_execution_cycles):
        
        # --- PHASE A: STOCHASTIC FIRE FLUID DYNAMICS ---
        if enable_fire and random.random() < fire_spread_rate:
            active_fires = list(st.session_state.fire_positions)
            for (fr, fc) in active_fires:
                # Fire wanders stochastically into adjacent structural grid slots
                tr = fr + random.choice([-1, 0, 1])
                tc = fc + random.choice([-1, 0, 1])
                if 0 <= tr < ROWS and 0 <= tc < COLS:
                    st.session_state.fire_positions.add((tr, tc))

        # --- PHASE B: PATH COST COMPUTATION & RE-ROUTING ---
        dynamic_costs = get_dynamic_cost_grid()
        total_congestion = update_evacuation_step(dynamic_costs)
        
        # --- PHASE C: METRIC TELEMETRY COLLECTION ---
        evac_count = len([p for p in st.session_state.passengers if p["evacuated"]])
        remaining_count = num_passengers - evac_count
        high_panic_count = len([p for p in st.session_state.passengers if p["panic"] == "HIGH"])
        current_safety_index = calculate_safety_score(tick_step, total_congestion, high_panic_count)

        # --- PHASE D: LIVE PANEL TELEMETRY PIPELINE ---
        m_row1_c1.metric("Evacuated Clear", f"🚶‍♂️ {evac_count}")
        m_row1_c2.metric("Trapped Onboard", f"❌ {remaining_count}")
        m_row1_c3.metric("Congestion Strain", f"⚠️ {total_congestion}")
        m_row1_c4.metric("Safety Core Index", f"🛡️ {current_safety_index}/100")

        # Calculate secondary rate percentages cleanly
        aisle_sat = min(100, int((total_congestion / max(1, num_passengers)) * 100))
        flow_vel = round(evac_count / max(1, tick_step), 1)
        total_hazards = len(st.session_state.fire_positions) + len(st.session_state.debris_positions)

        m_row2_c1.metric("Aisle Saturation", f"{aisle_sat}%")
        m_row2_c2.metric("Egress Flow Velocity", f"{flow_vel} PAX/s")
        m_row2_c3.metric("Hazard Grid Nodes", f"{total_hazards} Tiles")
        m_row2_c4.metric("Time Elapsed Clock", f"{tick_step}s / {max_execution_cycles}s")

        # --- PHASE E: REAL-TIME FLIGHT DISPATCH SYSTEM STATUS ALERTS ---
        if current_safety_index >= 80:
            system_alert_container.success(
                f"🟢 **STATUS OK (Step {tick_step}s):** Evacuation routing optimization tracking cleanly inside expected bounds."
            )
        elif current_safety_index >= 55:
            system_alert_container.warning(
                f"⚠️ **FLOW WARNING (Step {tick_step}s):** Localized crowd friction rising across central egress corridors."
            )
        else:
            system_alert_container.error(
                f"🚨 **CRITICAL COCKPIT ALERT (Step {tick_step}s):** Structural bottlenecks or hazards completely blocking exits!"
            )

        # --- PHASE F: HIGH-FIDELITY RENDER COMPOSITION ---
        map_2d_container.plotly_chart(
            generate_2d_mapping_network(), 
            use_container_width=True, 
            key=f"loop_2d_chart_step_{tick_step}"
        )
        hull_3d_container.plotly_chart(
            generate_3d_fuselage_matrix(), 
            use_container_width=True, 
            key=f"loop_3d_chart_step_{tick_step}"
        )

        # --- PHASE G: REAL-TIME HEATMAP VECTOR TRANSLATION ---
        density_matrix = np.zeros((ROWS, COLS))
        for p in st.session_state.passengers:
            if not p["evacuated"]:
                # Fast array lookup validation constraints
                if 0 <= p["y"] < ROWS and 0 <= p["x"] < COLS:
                    density_matrix[p["y"]][p["x"]] += 1
                
        h_map = go.Figure(data=go.Heatmap(z=density_matrix, colorscale="YlOrRd", showscale=False))
        h_map.update_layout(**density_heatmap_layout)
        density_heatmap_container.plotly_chart(
            h_map, 
            use_container_width=True, 
            key=f"loop_heatmap_step_{tick_step}"
        )

        # --- PHASE H: BREAK CONSTRAINTS TERMINATION OVERRIDES ---
        if evac_count == num_passengers:
            st.balloons()
            system_alert_container.success(
                f"🎉 **MISSION SUCCESS:** Safe cabin egress achieved. Total time taken: **{tick_step} seconds**."
            )
            break

        # Dynamically adjust the frame clock throttle according to user settings
        time.sleep(0.25 / max(1, simulation_speed))

# =========================================================
# 9.3 ENSEMBLE MACHINE LEARNING SCENARIO SANDBOX
# =========================================================
if enable_comparison:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("### 📊 Predictive Machine Learning Configuration Sandbox")
    st.caption("🤖 Comparative data below represents statistical inferences compiled by your Random Forest ensemble regressor.")
    
    # Run the machine learning predictions
    sc1_res = scenario_analysis_ml(scenario_1)
    sc2_res = scenario_analysis_ml(scenario_2)
    
    # Frame and render results inside a polished dataframe presentation window
    comparison_df = pd.DataFrame([sc1_res, sc2_res]).set_index("Scenario")
    st.dataframe(comparison_df, use_container_width=True)

# =========================================================
# 10. CAPSTONE PROJECT PROFILE INFERENCE SYSTEM
# =========================================================
# This section provides a localized manual test bench for operators 
# to run single-passenger predictive stress tests through the AI engine.

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #f97316; font-weight: 700;'>🧠 Individual Passenger Profile Inference Engine</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; margin-top:-10px;'>Simulate and test individual passenger profiles using the Random Forest Regressor trained on the model architecture specifications.</p>", unsafe_allow_html=True)

# 10.1 Structured Input Control Dashboard Grid
inf_c1, inf_c2, inf_c3, inf_c4, inf_c5 = st.columns(5)

with inf_c1: 
    inf_age = st.number_input(
        "Passenger Age", 
        min_value=18, max_value=90, value=65, step=1,
        help="Age of the passenger being evaluated."
    )

with inf_c2: 
    inf_speed = st.slider(
        "Walking Velocity (m/s)", 
        0.4, 2.5, 0.7, step=0.1,
        help="Clear aisle walking velocity. Typical pace is ~1.2 m/s. Lower values model restricted mobility."
    )
    # Human-readable velocity diagnostic badge
    if inf_speed < 0.8:   st.caption("⚠️ *Impaired / Slow*")
    elif inf_speed < 1.6: st.caption("🟢 *Standard Pace*")
    else:                 st.caption("⚡ *Rapid Sprint*")

with inf_c3: 
    inf_panic = st.slider(
        "Psychological Panic Value", 
        1, 10, 8, step=1,
        help="1 = Calm/Compliant, 10 = Severe shock/disorientation causing immediate path delay loops."
    )
    # Human-readable behavior diagnostic badge
    if inf_panic <= 3:   st.caption("🟢 *Calm / Orderly*")
    elif inf_panic <= 7: st.caption("🟡 *Anxious / Stressed*")
    else:                st.caption("🔴 *Severe Panic Loops*")

with inf_c4: 
    inf_row = st.number_input(
        "Seating Row Location", 
        min_value=1, max_value=max(30, ROWS), value=min(25, ROWS), step=1,
        help="The specific seat row location within the aircraft fuselage."
    )

with inf_c5: 
    inf_dist = st.number_input(
        "Grid Distance to Exit", 
        min_value=1, max_value=max(30, ROWS), value=min(20, ROWS), step=1,
        help="Total steps along the aisle needed to cross the threshold of an armed emergency door."
    )

st.markdown("<br>", unsafe_allow_html=True)

# 10.2 Predictive Analytics Frame Invocation Pipeline
if st.button("🔮 RUN TARGET INDIVIDUAL INFERENCE RISK PROFILE", use_container_width=True):
    # Pack parameters into a clean dataframe format matching notebook scaling columns exactly
    sample_passenger = pd.DataFrame(
        [[inf_age, inf_speed, inf_panic, inf_row, inf_dist]], 
        columns=["Age", "Walking_Speed", "Panic_Level", "Seat_Row", "Exit_Distance"]
    )
    
    # Safe model inference call with structural algorithm fallback protection
    if 'capstone_rf_model' in globals():
        predicted_clearance = capstone_rf_model.predict(sample_passenger)[0]
    else:
        # Fallback approximation function if model has not completed background training threads
        predicted_clearance = (inf_dist * 2) + (inf_panic * 3) + (80 - inf_speed * 20)
        
    rounded_time = round(predicted_clearance, 2)
    
    # Dynamic classification logic based on aviation clearance limits
    if rounded_time > 75.0:
        card_border = "#ef4444"    # Alert Red
        badge_text = "🚨 HIGH EFFLUX RISK"
        badge_desc = "This profile exceeds nominal safety threshold limits. Likely to trigger minor bottlenecks at the exit threshold lane."
    elif rounded_time > 45.0:
        card_border = "#eab308"    # Warning Yellow
        badge_text = "⚠️ MODERATE DELAY PROBABILITY"
        badge_desc = "Elevated escape window timeframe. Congestion profile remains manageable under normal deployment routing."
    else:
        card_border = "#22c55e"    # Optimal Green
        badge_text = "✅ OPTIMAL EVACUATION EFFICIENCY"
        badge_desc = "Excellent exit rate index. Profile meets standard civil aviation clearance targets safely."

    # 10.3 High-Visibility Prediction Layout Card
    st.markdown(f"""
        <div style="border: 2px solid {card_border}; background-color: rgba(15, 23, 42, 0.6); padding: 22px; border-radius: 8px; margin-top: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <span style="font-weight: 700; color: #ffffff; font-size: 1.05rem;">🎯 ML Engine Profile Assessment Results</span>
                <span style="background-color: {card_border}22; color: {card_border}; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: 700; border: 1px solid {card_border}44;">
                    {badge_text}
                </span>
            </div>
            <div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 8px;">
                <span style="font-size: 2.2rem; font-weight: 800; color: #ffffff; line-height: 1;">{rounded_time}</span>
                <span style="font-size: 1.1rem; color: #94a3b8; font-weight: 500;">Seconds to Egress Door</span>
            </div>
            <p style="color: #cbd5e1; font-size: 0.88rem; margin: 0; line-height: 1.4;">
                {badge_desc}
            </p>
        </div>
    """, unsafe_allow_html=True)

# =========================================================
# 11. REAL-TIME GEO-FENCING RADAR CONTROL (OPTIMIZED)
# =========================================================
# This section provides global tracking coordinates to check weather and 
# airspace parameters before routing fleet resource layouts to distinct hubs.

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #f97316; font-weight: 700; margin-bottom: 5px;'>🌐 Fleet Route Telemetry & GIS Radar Link</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Cross-reference regional airspace safety constraints and weather disruptions prior to launching emergency operations.</p>", unsafe_allow_html=True)

# 11.1 Enhanced CSS Inject Matrix (Locks vertical aspect ratios to prevent UI shifting)
st.markdown("""
<style>
    .telemetry-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 10px;
        min-height: 310px; /* Forces equal height match with map column */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .telemetry-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 12px;
        font-weight: 700;
    }
    .telemetry-value {
        font-size: 0.95rem;
        color: #f8fafc;
        font-weight: 500;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
</style>
""", unsafe_allow_html=True)

import streamlit.components.v1 as components

# Layout Structural Definitions
st.set_page_config(layout="wide", page_title="Fleet Telemetry Radar")
st.title("🛰️ Real-Time Fleet Telemetry Radar")

city_db = {
    "London": [51.5074, -0.1278, "Sector LHR Alpha - Active Corridor", "35,000 ft", "🌧️ Heavy Rain & Fog", True],
    "New York": [40.7128, -74.0060, "JFK Hub Main Base - Operational", "38,000 ft", "☀️ Clear Sky", True],
    "Tokyo": [35.6762, 139.6503, "HND Gate East - Holding Pattern", "31,000 ft", "⛅ Scattered Clouds", True],
    "Paris": [48.8566, 2.3522, "CDG Sector Airspace - Clear Path", "36,500 ft", "💨 Mild Wind", True],
    "Dhaka": [23.8103, 90.4125, "DAC International Hub - Ground Check", "33,000 ft", "⛈️ Thunderstorm Activity", True],
    "Kolkata": [22.5726, 88.3639, "CCU Terminal Zone - Route Active", "34,000 ft", "☀️ High Temperature / Clear", True]
}

forbidden_zones = ["pakistan", "pakisthan", "islamabad", "lahore", "karachi", "conflict zone", "restricted airspace"]

# Single Search Input Field
selected_city = st.text_input(
    "Enter Target Sector or Deployment Station (e.g., Paris, Dhaka, Pakistan):", 
    value="",
    placeholder="Type station name here and press Enter...",
    key="unified_radar_input"
)

parsed_query = selected_city.strip().title() if selected_city.strip() != "" else None

geofence_banner = st.empty()
audio_placeholder = st.empty()  
map_layout_col1, map_layout_col2 = st.columns([2, 3], gap="medium")

# Re-engineered Heavy Air-Raid / Nuclear Facility Mechanical Siren Engine
def get_heavy_military_siren_html(header_text):
    return f"""
    <div style="background-color: #ef4444; color: white; padding: 14px; font-weight: bold; font-size: 1.1rem; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.2); animation: blinker 1s linear infinite; font-family: sans-serif; letter-spacing: 0.5px;">
        🚨 {header_text} 🚨
    </div>
    <div style="text-align: center; color: #f87171; font-size: 0.85rem; margin-top: 6px; font-weight: bold;">⚠️ Move mouse or click screen to engage alert audio ⚠️</div>
    <style>@keyframes blinker {{ 50% {{ opacity: 0.4; }} }}</style>

    <script>
        var audioCtx = null;
        var osc = null;
        var gainNode = null;
        var lfo = null;

        function playHeavySiren() {{
            if (audioCtx) return; // Prevent multiple audio instances from stacking
            
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            
            osc = audioCtx.createOscillator();
            gainNode = audioCtx.createGain();
            lfo = audioCtx.createOscillator();
            var lfoGain = audioCtx.createGain();
            
            // Using a raw 'sawtooth' wave mixed with modulation for that gritty, alarming "Whaa-Whaa" tone
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(400, audioCtx.currentTime); // Base heavy frequency
            
            // Low-Frequency Oscillator (LFO) to control the up-and-down wailing cycle
            lfo.frequency.setValueAtTime(1.2, audioCtx.currentTime); // Speed of the wave modulation (1.2 times per second)
            lfoGain.gain.setValueAtTime(180, audioCtx.currentTime);  // Depth/Pitch range of the siren pitch rise and fall
            
            lfo.connect(lfoGain);
            lfoGain.connect(osc.frequency);
            
            // Set smooth Master Volume balance
            gainNode.gain.setValueAtTime(0.18, audioCtx.currentTime);
            
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            // Trigger both hardware layers instantly
            lfo.start();
            osc.start();
        }}

        // Broad-spectrum interaction handlers to immediately bypass browser security filters
        window.addEventListener('click', playHeavySiren);
        window.addEventListener('mouseenter', playHeavySiren);
        window.addEventListener('keydown', playHeavySiren);
        document.body.addEventListener('mousemove', playHeavySiren);
        
        // Immediate background execution attempt
        setTimeout(playHeavySiren, 100);
    </script>
    """

if parsed_query is not None:
    query_lower = selected_city.strip().lower()
    is_forbidden = query_lower in forbidden_zones
    is_registered = parsed_query in city_db

    with map_layout_col1:
        if is_forbidden:
            airspace_status = "🚨 CRITICAL VIOLATION - HOSTILE AIRSPACE"
            flight_alt = "❌ EMERGENCY DESCENT REQUIRED (0 ft)"
            weather_profile = "⚠️ WAR ZONE / NO-FLY RESTRICTION ACTIVE"
            safe_flag = False
            header_name = f"{selected_city.strip()} (🛑 FORBIDDEN ZONE)"
            
            geofence_banner.error(f"🛑 **GEOFENCE VIOLATION:** Restricted Airspace Detected: '{selected_city.strip()}'!")
            
            with audio_placeholder:
                components.html(get_heavy_military_siren_html("CRITICAL DANGER: DEFENSE SIREN ENGAGED"), height=95)
            
        elif is_registered:
            latitude, longitude, airspace_status, flight_alt, weather_profile, safe_flag = city_db[parsed_query]
            header_name = parsed_query
            geofence_banner.success(f"✅ **SAFE SPACE ENTRY:** Flight corridor cleared for '{parsed_query}'.")
            audio_placeholder.empty() 
            
        else:
            airspace_status = "🚨 UNREGISTERED AIRSPACE - RED ALERT"
            flight_alt = "⚠️ FLIGHT PROFILE BLOCKED (0 ft)"
            weather_profile = "🚨 SECURITY HAZARD / UNVERIFIED COORDINATES"
            safe_flag = False
            header_name = f"{selected_city.strip()} (🚨 INVALID SECTOR)"
            
            geofence_banner.error(f"🚨 **RED ALERT:** Transgression into unregistered coordinates: '{selected_city.strip()}'")
            
            with audio_placeholder:
                components.html(get_heavy_military_siren_html("ALERT: SECURE BOUNDARY BREACH DETECTED"), height=95)

        # Telemetry UI Panel
        html_content = f"""
        <div style="background-color: #1e293b; border: 1px solid {'#38bdf8' if safe_flag else '#ef4444'}; border-radius: 12px; padding: 20px; font-family: sans-serif; color: #f1f5f9; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <h5 style="color: {'#38bdf8' if safe_flag else '#f87171'}; margin-top:0; margin-bottom:14px; font-weight:700; font-size:1rem;">🛰️ Real-Time Sector Diagnostics</h5>
            <div style="color: {'#4ade80' if safe_flag else '#f87171'}; font-weight:700; font-size:1.1rem; margin-bottom: 12px;">App UI Active Grid: {header_name}</div>
            <div style="font-size: 0.85rem; margin-bottom: 6px; color:#94a3b8;">📡 Status Matrix: {airspace_status}</div>
            <div style="font-size: 0.85rem; margin-bottom: 6px; color:#94a3b8;">✈️ Altitude Data: {flight_alt}</div>
            <div style="font-size: 0.85rem; color:#94a3b8;">⛅ Meteorological Scan: {weather_profile}</div>
        </div>
        """
        components.html(html_content, height=220)

    with map_layout_col2:
        if safe_flag:
            st.map(pd.DataFrame({'lat': [latitude], 'lon': [longitude]}), size=40, zoom=10)
        else:
            st.markdown(f"""
                <div style="border: 2px dashed rgba(239, 68, 68, 0.8); background: rgba(239, 68, 68, 0.08); height: 220px; border-radius: 10px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px;">
                    <div><h2 style="margin: 0;">🛑</h2><h5 style="color: #f87171; margin-top: 10px;">🚨 DETECTED RESTRICTION SECTOR LOCK</h5></div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("💡 Please enter a Sector name (e.g., Pakistan or Paris) to check.")
    
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


st.set_page_config(layout="wide")

# ==========================================
# 🛠️ 
# ==========================================
if "current_voice_command" not in st.session_state:
    st.session_state.current_voice_command = "nominal"

detected_text = st.session_state.current_voice_command.lower()
is_crisis = "fire" in detected_text or "smoke" in detected_text

# কালার এবং স্ট্যাটাস নির্ধারণ
accent_color = "#ff3366" if is_crisis else "#00ffcc"
status_text = "CRITICAL HAZARD DETECTED" if is_crisis else "NOMINAL"
progress_value = 35 if is_crisis else 100



# ==========================================
# 📊(Plotly)
# ==========================================
st.title("🛰️ Core Environmental Telemetry Mainframe")
st.markdown(f"System State Status: <b style='color:{accent_color}; font-size: 1.2rem;'>{status_text}</b>", unsafe_allow_html=True)
st.markdown("---")


chart_rows = 50
np.random.seed(42)
timeline = np.arange(1, chart_rows + 1)

if is_crisis:
   
    temp_data = np.linspace(24, 92, chart_rows) + np.random.normal(0, 4, chart_rows)
    gas_levels = np.linspace(12, 340, chart_rows) + np.random.normal(0, 8, chart_rows)
else:
    
    temp_data = np.ones(chart_rows) * 24 + np.random.normal(0, 0.5, chart_rows)
    gas_levels = np.ones(chart_rows) * 14 + np.random.normal(0, 0.6, chart_rows)


fig = go.Figure()

#line1
fig.add_trace(go.Scatter(
    x=timeline, 
    y=temp_data,
    mode='lines',
    name='Thermal Core (°C)',
    line=dict(color=accent_color, width=3),
    hovertemplate='Time: %{x}<br>Temp: %{y:.2f}°C<extra></extra>'
))

#line2
fig.add_trace(go.Scatter(
    x=timeline, 
    y=gas_levels,
    mode='lines',
    name='Toxin Level (PPM)',
    line=dict(color='#f59e0b', width=3, dash='dash'),
    hovertemplate='Time: %{x}<br>Gas: %{y:.2f} PPM<extra></extra>'
))


fig.update_layout(
    title=dict(
        text="📈 Real-Time Environmental Grid Analytics Vector",
        font=dict(color="#ffffff", size=16, family="sans-serif")
    ),
    paper_bgcolor="#0b0f19",  
    plot_bgcolor="#0e1322",   
    xaxis=dict(
        title="Timeline Vector (Seconds)",
        title_font=dict(color="#94a3b8"),
        tickfont=dict(color="#94a3b8"),
        gridcolor="#1e293b",
        zeroline=False
    ),
    yaxis=dict(
        title="Sensor Values Matrix",
        title_font=dict(color="#94a3b8"),
        tickfont=dict(color="#94a3b8"),
        gridcolor="#1e293b",
        zeroline=False
    ),
    legend=dict(
        font=dict(color="#ffffff"),
        bgcolor="rgba(0,0,0,0)"
    ),
    margin=dict(l=40, r=40, t=50, b=40),
    hovermode="x unified"
)


st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div style="background: #0f172a; padding: 14px; border-radius: 6px; border: 1px solid #1e293b; font-size:0.85rem; color:#94a3b8; font-family: monospace; margin-top: 15px;">
    ⚡ <b>Grid Status Feed:</b> Telemetry analytics are directly synced with browser audio capture triggers. Speaking safety clearance codes modifies data vectors dynamically.
</div>
""", unsafe_allow_html=True)
    
# =========================================================
# 12. FLIGHT SAFETY AI COPILOT CHATBOX TERMINAL
# =========================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #00ffcc; font-weight: 700;'>💬 AI Safety Copilot Tactical Chatbox</h3>", unsafe_allow_html=True)

# Container wrapped in glassmorphism styling matching your layout
with st.container():
    st.markdown("""
        <div style="background: rgba(4, 20, 42, 0.4); border: 1px solid rgba(0, 255, 204, 0.3); padding: 15px; border-radius: 12px; max-height: 400px; overflow-y: auto; margin-bottom: 15px;">
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0;">📟 Secure Crew-to-AI Chat Link Active</p>
        </div>
    """, unsafe_allow_html=True)

    # Render persistent conversation elements seamlessly from session memory
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept manual operational prompts from the user
    if chat_input := st.chat_input("Ask Flight AI (e.g., 'What is our current safety index strategy?')"):
        # Append crew message to state isolation matrix
        st.session_state.chat_messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)

        # Generate a situational-aware contextual feedback layer
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Simple algorithmic keyword matrix reading live code variable trends
            query = chat_input.lower()
            if "fire" in query or "hazard" in query:
                reply = "🔥 **AI Hazard Analysis:** Thermal spread is being calculated via dynamic edge weight updates on the A* mesh grid. Evacuate passengers away from structural columns."
            elif "panic" in query or "anxious" in query:
                reply = "🧠 **Crew-Influence Directive:** Panicked PAX profiles invoke random-walk path variations. Move your Flight Attendants inside their grid radii to enforce calmer states."
            elif "clear" in query or "time" in query:
                reply = f"⏱️ **Egress Metrics:** Current manifest contains {len(st.session_state.passengers)} profiles. Run the escape script to map the total exit timeline."
            else:
                reply = "🤖 **Tactical Assist:** Message processed. I am continuously monitoring fuselage flow vectors and active geofencing boundaries."

            response_placeholder.markdown(reply)
            
            # Save response to history matrix so it doesn't disappear when the app refreshes
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})