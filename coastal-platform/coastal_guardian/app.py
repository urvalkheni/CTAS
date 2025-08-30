import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta
import numpy as np
from utils.data_collector import DataCollector

# Try to import folium, but handle gracefully if not available
try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# Try to import ML components, but handle gracefully if not available
try:
    import ml_anomaly_detection
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Coastal Guardian",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary: #00b894;
        --accent: #00cec9;
        --bg: #ffffff;
        --bg-alt: #f0f8ff;
        --text: #2d3436;
        --muted: #636e72;
        --border: #74b9ff;
        --shadow: 0 10px 30px rgba(0,0,0,0.08);
        --success: #00b894;
        --info: #00cec9;
        --warning: #fdcb6e;
        --danger: #e17055;
    }

    /* Layout container: tighten width and center */
    .block-container {
        max-width: 1200px;
        padding-top: 1rem;
    }

    /* Top header bar for authenticated views */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(120deg, var(--primary), var(--accent));
        color: #fff;
        padding: 1rem 1.25rem;
        border-radius: 0.75rem;
        box-shadow: var(--shadow);
        margin-bottom: 1.5rem;
    }
    .topbar .logo { font-weight: 700; letter-spacing: 0.2px; }
    .topbar .tagline { opacity: 0.9; font-size: 0.95rem; }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    .hero-title {
        font-size: 3.25rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.25);
    }
    .hero-subtitle { font-size: 1.25rem; margin-bottom: 1.25rem; opacity: 0.95; }
    .hero-description { font-size: 1.05rem; max-width: 780px; margin: 0 auto 1.5rem; line-height: 1.65; }

    /* Generic Section/Card */
    .section {
        background: var(--bg);
        border: 2px solid var(--border);
        border-radius: 0.75rem;
        padding: 1.25rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        margin: 1rem 0 1.25rem 0;
    }

    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 1.5rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        border: 2px solid var(--border);
    }
    .feature-card:hover { transform: translateY(-3px); box-shadow: 0 10px 24px rgba(0,0,0,0.12); }
    .feature-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .feature-title { font-size: 1.25rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem; }
    .feature-description { color: var(--muted); line-height: 1.6; }

    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
        color: white;
        padding: 2.25rem 1.5rem;
        border-radius: 1rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: var(--shadow);
    }
    .cta-button { background: white; color: var(--primary); padding: 0.85rem 1.5rem; border: none; border-radius: 0.5rem; font-size: 1.05rem; font-weight: 700; cursor: pointer; transition: all 0.25s ease; margin: 0.4rem; text-decoration: none; display: inline-block; min-width: 200px; }
    .cta-button:hover { background: #f8f9fa; transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,0.15); }
    .cta-button-secondary { background: transparent; color: white; border: 2px solid white; }
    .cta-button-secondary:hover { background: white; color: var(--primary); }

    /* Logout Page */
    .logout-container {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 1rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
    }
    .logout-icon { font-size: 3rem; margin-bottom: 0.5rem; }
    .logout-title { font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem; }
    .logout-message { font-size: 1.05rem; margin-bottom: 1.25rem; opacity: 0.95; }

    /* Alert cards with new theme */
    .alert-critical { background-color: #ffe8e8; border-left: 4px solid var(--danger); }
    .alert-high { background-color: #fff3e0; border-left: 4px solid var(--warning); }
    .alert-moderate { background-color: #e8f5e8; border-left: 4px solid var(--success); }
    .alert-low { background-color: #e8f5e8; border-left: 4px solid var(--info); }

    /* Metric and role badges */
    .metric-card { background-color: var(--bg-alt); padding: 0.85rem; border-radius: 0.5rem; border: 1px solid var(--border); }
    .role-badge { padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 800; }
    .role-authority { background-color: #e8f5e8; color: var(--success); }
    .role-ngo { background-color: #e0f7fa; color: var(--info); }
    .role-community { background-color: #e8f5e8; color: var(--success); }

    /* Stats */
    .stats-container { background: var(--bg-alt); padding: 1.5rem; border-radius: 1rem; margin: 1.25rem 0; border: 2px solid var(--border); }
    .stat-item { text-align: center; padding: 0.75rem; }
    .stat-number { font-size: 2rem; font-weight: 800; color: var(--text); margin-bottom: 0.25rem; }
    .stat-label { color: var(--muted); font-weight: 600; }

    /* Navigation hover */
    .nav-item { padding: 0.5rem; margin: 0.25rem 0; border-radius: 0.5rem; transition: background-color 0.2s ease; }
    .nav-item:hover { background-color: var(--bg-alt); }

    /* Enhanced Typography */
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1, h2, h3, h4, h5, h6 { color: var(--text); font-weight: 700; }
    p { color: var(--text); line-height: 1.6; }
    
    /* Streamlit specific improvements */
    .stApp { background-color: var(--bg-alt); }
    .main .block-container { background-color: var(--bg); border-radius: 1rem; padding: 2rem; box-shadow: var(--shadow); }
    .stButton > button { background-color: var(--primary); color: white; border: none; border-radius: 0.5rem; padding: 0.75rem 1.5rem; font-weight: 600; }
    .stButton > button:hover { background-color: var(--accent); transform: translateY(-2px); }
    
    /* Data tables */
    .stDataFrame { border: 2px solid var(--border); border-radius: 0.5rem; }
    
    /* Charts and visualizations */
    .stPlotlyChart { border: 2px solid var(--border); border-radius: 0.5rem; padding: 1rem; background: white; }
</style>
""", unsafe_allow_html=True)

# Simple authentication system
def check_login(email, password, role):
    """Simple login check for demo purposes"""
    demo_users = {
        'admin@coastalguardian.com': {'password': 'password123', 'role': 'authority', 'name': 'Admin User'},
        'ngo@coastalguardian.com': {'password': 'password123', 'role': 'ngo', 'name': 'NGO Representative'},
        'community@coastalguardian.com': {'password': 'password123', 'role': 'community', 'name': 'Community Member'}
    }
    
    if email in demo_users:
        user = demo_users[email]
        if user['password'] == password and user['role'] == role:
            return {
                '_id': f'user_{email}',
                'name': user['name'],
                'email': email,
                'role': user['role'],
                'location': {'coordinates': [72.8777, 19.0760]},
                'points': 0
            }
    return None

def add_user_to_db(user):
    collector = DataCollector()
    collector.add_user(
        name=user.get('name', 'Unknown'),
        email=user.get('email', ''),
        role=user.get('role', 'community'),
        points=user.get('points', 0)
    )

# Sidebar - Authentication & Navigation
st.sidebar.title("🌊 Coastal Guardian")
st.sidebar.markdown("---")

# Session state initialization
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'logout_confirmed' not in st.session_state:
    st.session_state.logout_confirmed = False

if st.session_state.user is None:
    st.sidebar.subheader("🔐 Authentication")
    
    # Demo mode for hackathon
    if st.sidebar.button("🚀 Quick Demo (No Login)", type="primary"):
        st.session_state.user = {
            '_id': 'demo_user_001',
            'name': 'Demo User',
            'email': 'demo@coastalguardian.com',
            'role': 'authority',
            'location': {'coordinates': [72.8777, 19.0760]},
            'points': 0
        }
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 Login")
    
    # Login form
    with st.sidebar.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        role = st.selectbox("Role", ["authority", "ngo", "community"])
        if st.form_submit_button("🔐 Login", type="primary"):
            if email and password:
                user = check_login(email, password, role)
                if user:
                    st.session_state.user = user
                    add_user_to_db(user)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Try demo accounts:")
                    st.info("""
                    **Demo Accounts:**
                    - Authority: `admin@coastalguardian.com` / `password123`
                    - NGO: `ngo@coastalguardian.com` / `password123`
                    - Community: `community@coastalguardian.com` / `password123`
                    """)
            else:
                st.error("Please enter email and password")

else:
    # User info
    user = st.session_state.user
    st.sidebar.markdown(f"""
    <div class="metric-card">
        <strong>{user['name']}</strong><br>
        <span class="role-badge role-{user['role']}">{user['role'].title()}</span><br>
        📊 {user['points']} points
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced logout with confirmation
    col1, col2 = st.sidebar.columns([1, 1])
    
    with col1:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.page = 'logout_confirm'
            st.rerun()
    
    with col2:
        if st.button("ℹ️ Help", use_container_width=True):
            st.sidebar.info("""
            **Need Help?**
            
            📧 support@coastalguardian.com
            📞 +1-800-COASTAL
            
            **Quick Tips:**
            - Use Quick Demo for instant access
            - Check leaderboard for community impact
            - Submit reports to earn points
            """)
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["🏠 Dashboard", "🚨 Threats & Alerts", "📊 Reports", "📈 Trends", "🏆 Leaderboard", "⚙️ Settings"]
    )

# Handle logout confirmation page
if st.session_state.get('page') == 'logout_confirm' and st.session_state.user is not None:
    user = st.session_state.user
    
    # Logout confirmation page
    st.markdown("""
    <div class="logout-container">
        <div class="logout-icon">🚪</div>
        <div class="logout-title">Logout Confirmation</div>
        <div class="logout-message">
            Thank you for using Coastal Guardian, {user_name}!<br>
            Are you sure you want to logout?
        </div>
    </div>
    """.format(user_name=user['name']), unsafe_allow_html=True)
    
    # Session summary
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 1rem; margin: 2rem 0; text-align: center;">
            <h4 style="color: #2d3436; margin-bottom: 1rem;">📊 Your Session Summary</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #0984e3;">{user_points}</div>
                    <div style="color: #636e72;">Points Earned</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #00b894;">{session_time}</div>
                    <div style="color: #636e72;">Session Time</div>
                </div>
                <div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #fdcb6e;">{user_role}</div>
                    <div style="color: #636e72;">Role</div>
                </div>
            </div>
        </div>
        """.format(
            user_points=user['points'],
            session_time="15 min",  # Demo value
            user_role=user['role'].title()
        ), unsafe_allow_html=True)
        
        # Logout buttons
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚪 Confirm Logout", type="primary", use_container_width=True):
                # Clear session and show logout success
                st.session_state.user = None
                st.session_state.page = 'logout_success'
                st.rerun()
        
        with col_btn2:
            if st.button("⬅️ Cancel", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        
        # Quick actions before logout
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6c757d; margin-top: 2rem;">
            <p><strong>Before you go:</strong></p>
            <p>📧 Check your notifications • 📊 Review your impact • 🌊 Keep protecting our coasts!</p>
        </div>
        """, unsafe_allow_html=True)

# Handle logout success page
elif st.session_state.get('page') == 'logout_success':
    st.markdown("""
    <div class="logout-container">
        <div class="logout-icon">✨</div>
        <div class="logout-title">Successfully Logged Out</div>
        <div class="logout-message">
            Thank you for being a Coastal Guardian!<br>
            Your contributions help protect our precious coastlines.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Return to landing page
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🏠 Return to Home", type="primary", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #6c757d;">Come back anytime to continue protecting our coasts!</p>
            <p style="color: #6c757d; margin-top: 1rem;"><small>Click the button above to return to the home page</small></p>
        </div>
        """, unsafe_allow_html=True)

# Main content based on authentication
elif st.session_state.user is None:
    # Enhanced Landing Page
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🌊 Coastal Guardian</div>
        <div class="hero-subtitle">AI-Powered Coastal Protection</div>
        <div class="hero-description">
            Protecting coastlines through real-time monitoring, community engagement, 
            and AI-powered threat detection. Join thousands of coastal guardians 
            making a difference.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call-to-Action Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 Start Quick Demo", type="primary", use_container_width=True):
                st.session_state.user = {
                    '_id': 'demo_user_001',
                    'name': 'Demo User',
                    'email': 'demo@coastalguardian.com',
                    'role': 'authority',
                    'location': {'coordinates': [72.8777, 19.0760]},
                    'points': 0
                }
                st.rerun()
        
        with col_btn2:
            st.markdown("""
            <div style="text-align: center; margin-top: 0.5rem;">
                <small style="color: #6c757d;">💡 Use sidebar to login with demo credentials</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Statistics Section
    st.markdown("""
    <div class="stats-container">
        <h3 style="text-align: center; margin-bottom: 2rem; color: #2d3436;">📊 Platform Impact</h3>
    </div>
    """, unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">1,247</div>
            <div class="stat-label">Active Monitors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">89</div>
            <div class="stat-label">Threats Detected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">2,156</div>
            <div class="stat-label">Reports Submitted</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">45km</div>
            <div class="stat-label">Coastline Protected</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("<br>", unsafe_allow_html=True)
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚨</div>
            <div class="feature-title">Real-time Threat Detection</div>
            <div class="feature-description">
                AI-powered monitoring system that detects coastal threats like storm surges, 
                abnormal tide levels, and pollution incidents in real-time.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <div class="feature-title">Community Engagement</div>
            <div class="feature-description">
                Empowering local communities through citizen science, gamified reporting, 
                and collaborative coastal conservation efforts.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Comprehensive Analytics</div>
            <div class="feature-description">
                Interactive dashboards, trend analysis, and data visualization tools 
                for informed decision-making and coastal management.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Demo Accounts Info
    st.markdown("""
    <div class="cta-section">
        <h3 style="margin-bottom: 1rem;">🔐 Demo Accounts Available</h3>
        <p style="margin-bottom: 2rem; opacity: 0.9;">Try different user roles to experience the full platform</p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 2rem;">
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 0.5rem; backdrop-filter: blur(10px);">
                <h4>🏛️ Authority User</h4>
                <p><strong>Email:</strong> admin@coastalguardian.com<br>
                <strong>Password:</strong> password123</p>
                <small>Access: Full system control, alert management, settings</small>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 0.5rem; backdrop-filter: blur(10px);">
                <h4>🏢 NGO Representative</h4>
                <p><strong>Email:</strong> ngo@coastalguardian.com<br>
                <strong>Password:</strong> password123</p>
                <small>Access: Reporting, analytics, community coordination</small>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 0.5rem; backdrop-filter: blur(10px);">
                <h4>👨‍👩‍👧‍👦 Community Member</h4>
                <p><strong>Email:</strong> community@coastalguardian.com<br>
                <strong>Password:</strong> password123</p>
                <small>Access: Report submission, leaderboard, local alerts</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Authenticated user interface
    user = st.session_state.user

    # Top header bar for authenticated sections
    st.markdown(
        f"""
        <div class="topbar">
            <div class="logo">🌊 Coastal Guardian</div>
            <div class="tagline">Real-time coastal intelligence • Signed in as <strong>{user['name']}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    if page == "🏠 Dashboard":
        st.header("📊 Dashboard")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🚨 Critical/High Alerts", 3)
        
        with col2:
            st.metric("📋 Pending Reports", 5)
        
        with col3:
            st.metric("📊 Avg Alert Severity", "45.2")
        
        with col4:
            st.metric("🏆 Top Contributor", "Demo User (150 pts)")
        
        # Map
        st.subheader("🗺️ Live Monitoring Map")
        if FOLIUM_AVAILABLE:
            try:
                m = folium.Map(location=[20.59, 78.96], zoom_start=5)
                folium.Marker([19.0760, 72.8777], popup="Mumbai - Demo Alert", 
                            icon=folium.Icon(color='red', icon='warning-sign')).add_to(m)
                folium.Marker([13.0827, 80.2707], popup="Chennai - Storm Warning", 
                            icon=folium.Icon(color='orange', icon='warning-sign')).add_to(m)
                # Full-width map aligned to container
                st_folium(m, width=1200, height=420)
            except Exception as e:
                st.error(f"Map error: {e}")
                st.info("Showing demo map data instead")
        else:
            st.info("🗺️ Map visualization not available. Showing demo data instead.")
        
        st.markdown("""
        **Demo Map Data:**
        - 🚨 **Mumbai**: High tide alert (Score: 85)
        - 🚨 **Chennai**: Storm surge warning (Score: 92)
        - 📊 **Kolkata**: Community report pending
        """)
        
        # Recent alerts
        st.subheader("🚨 Recent Alerts")
        demo_alerts = [
            {"type": "storm_surge", "message": "High storm surge detected in Mumbai", "severity": "high", "score": 85.0, "createdAt": "2025-08-30 10:30:00"},
            {"type": "tide_level", "message": "Unusually high tide levels", "severity": "moderate", "score": 65.0, "createdAt": "2025-08-30 09:15:00"},
            {"type": "pollution", "message": "Water quality alert in Chennai", "severity": "critical", "score": 92.0, "createdAt": "2025-08-30 08:45:00"}
        ]
        
        for alert in demo_alerts:
            alert_class = f"alert-{alert['severity']}"
            st.markdown(f"""
            <div class="{alert_class}" style="padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                <strong>{alert['type'].replace('_', ' ').title()}</strong><br>
                {alert['message']}<br>
                <small>Score: {alert['score']:.1f} | {alert['createdAt']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "🚨 Threats & Alerts":
        st.header("🚨 Threats & Alerts")
        
        # Data upload
        st.subheader("📊 Upload Sensor Data")
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ Loaded {len(df)} records")
                
                # Display data
                st.dataframe(df.head())
                
                # Process data and generate alerts
                if st.button("🔍 Analyze Data"):
                    with st.spinner("Processing data and detecting threats..."):
                        # Demo alerts
                        alerts = [
                            {
                                'type': 'storm_surge',
                                'message': 'High storm surge detected in uploaded data',
                                'severity': 'high',
                                'score': 78.5,
                                'createdAt': datetime.now().isoformat()
                            }
                        ]
                        
                        st.subheader("🚨 Generated Alerts")
                        for alert in alerts:
                            alert_class = f"alert-{alert['severity']}"
                            st.markdown(f"""
                            <div class="{alert_class}" style="padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                                <strong>{alert['type'].replace('_', ' ').title()}</strong><br>
                                {alert['message']}<br>
                                <small>Score: {alert['score']:.1f} | Severity: {alert['severity']}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.success(f"✅ {len(alerts)} alerts generated and saved")
                
                # Charts
                if 'timestamp' in df.columns:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    
                    # Time series chart
                    st.subheader("📈 Data Trends")
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    
                    if len(numeric_cols) > 0:
                        selected_col = st.selectbox("Select metric", numeric_cols)
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=df['timestamp'],
                            y=df[selected_col],
                            mode='lines+markers',
                            name=selected_col
                        ))
                        fig.update_layout(
                            title=f"{selected_col.replace('_', ' ').title()} Over Time",
                            xaxis_title="Time",
                            yaxis_title=selected_col,
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error processing file: {e}")
        
        # Alert management
        st.subheader("📋 Alert Management")
        demo_alerts = [
            {
                '_id': 'demo_1',
                'type': 'storm_surge',
                'message': 'High storm surge detected in Mumbai',
                'severity': 'high',
                'score': 85.0,
                'createdAt': '2025-08-30 10:30:00'
            },
            {
                '_id': 'demo_2',
                'type': 'tide_level',
                'message': 'Unusually high tide levels',
                'severity': 'moderate',
                'score': 65.0,
                'createdAt': '2025-08-30 09:15:00'
            }
        ]
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            severity_filter = st.selectbox("Severity", ["All"] + list(set(a['severity'] for a in demo_alerts)))
        with col2:
            type_filter = st.selectbox("Type", ["All"] + list(set(a['type'] for a in demo_alerts)))
        with col3:
            date_filter = st.date_input("From Date", value=datetime.now().date() - timedelta(days=7))
        
        # Filter alerts
        filtered_alerts = demo_alerts
        if severity_filter != "All":
            filtered_alerts = [a for a in filtered_alerts if a['severity'] == severity_filter]
        if type_filter != "All":
            filtered_alerts = [a for a in filtered_alerts if a['type'] == type_filter]
        
        # Display alerts
        for alert in filtered_alerts:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                alert_class = f"alert-{alert['severity']}"
                st.markdown(f"""
                <div class="{alert_class}" style="padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                    <strong>{alert['type'].replace('_', ' ').title()}</strong><br>
                    {alert['message']}<br>
                    <small>Score: {alert['score']:.1f} | {alert['createdAt']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"📱 Notify", key=f"notify_{alert['_id']}"):
                    st.success("Notification sent!")
            
            with col3:
                if st.button(f"✅ Acknowledge", key=f"ack_{alert['_id']}"):
                    st.success("Alert acknowledged!")
                    st.rerun()
    
    elif page == "📊 Reports":
        st.header("📊 Community Reports")
        
        # Report submission
        st.subheader("📝 Submit Report")
        
        with st.form("report_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                report_type = st.selectbox("Report Type", [
                    "mangrove_cut", "dumping", "pollution", "illegal_activity"
                ])
                description = st.text_area("Description")
            
            with col2:
                lat = st.number_input("Latitude", value=19.0760, format="%.4f")
                lng = st.number_input("Longitude", value=72.8777, format="%.4f")
                photo = st.file_uploader("Upload Photo", type=['jpg', 'jpeg', 'png'])
            
            if st.form_submit_button("Submit Report"):
                if photo is not None:
                    try:
                        # Save photo
                        photo_path = f"reports/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.name}"
                        os.makedirs("reports", exist_ok=True)
                        with open(photo_path, "wb") as f:
                            f.write(photo.getbuffer())
                        
                        st.success("✅ Report submitted successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error saving report: {e}")
                else:
                    st.error("Please upload a photo")
        
        # Reports management (for authorities)
        if user['role'] == 'authority':
            st.subheader("🔍 Pending Reports")
            demo_reports = [
                {
                    '_id': 'demo_report_1',
                    'type': 'mangrove_cut',
                    'description': 'Mangrove cutting observed in Mumbai',
                    'score': 85.0,
                    'createdAt': '2025-08-30 10:30:00'
                }
            ]
            
            for report in demo_reports:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    **{report['type'].replace('_', ' ').title()}** - {report['description']}<br>
                    <small>Confidence: {report['score']:.1f}% | {report['createdAt']}</small>
                    """)
                
                with col2:
                    if st.button(f"✅ Verify", key=f"verify_{report['_id']}"):
                        st.success("Report verified!")
                        st.rerun()
                
                with col3:
                    if st.button(f"❌ Reject", key=f"reject_{report['_id']}"):
                        st.success("Report rejected!")
                        st.rerun()
        
        # All reports
        st.subheader("📋 All Reports")
        demo_all_reports = [
            {
                'type': 'mangrove_cut',
                'description': 'Mangrove cutting observed in Mumbai',
                'status': 'verified',
                'score': 85.0,
                'createdAt': '2025-08-30 10:30:00'
            },
            {
                'type': 'pollution',
                'description': 'Water pollution detected',
                'status': 'pending',
                'score': 72.0,
                'createdAt': '2025-08-30 09:15:00'
            }
        ]
        
        for report in demo_all_reports:
            status_icon = "✅" if report['status'] == 'verified' else "❌" if report['status'] == 'rejected' else "⏳"
            st.markdown(f"""
            {status_icon} **{report['type'].replace('_', ' ').title()}** - {report['description']}<br>
            <small>Status: {report['status']} | Score: {report['score']:.1f}% | {report['createdAt']}</small>
            """)
    
    elif page == "📈 Trends":
        st.header("📈 Trends & Analytics")
        
        # Time range selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now().date())
        
        # Metrics selection
        metrics = st.multiselect(
            "Select Metrics",
            ["sea_level", "tide_level", "wave_height", "wind_speed", "turbidity"],
            default=["sea_level", "tide_level"]
        )
        
        if metrics:
            # Demo trend data
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            trend_data = pd.DataFrame({
                'timestamp': dates,
                'sea_level': np.random.normal(1.2, 0.3, len(dates)),
                'tide_level': np.random.normal(2.5, 0.5, len(dates))
            })
            
            # Time series chart
            fig = go.Figure()
            
            for metric in metrics:
                if metric in trend_data.columns:
                    fig.add_trace(go.Scatter(
                        x=trend_data['timestamp'],
                        y=trend_data[metric],
                        mode='lines+markers',
                        name=metric.replace('_', ' ').title()
                    ))
            
            fig.update_layout(
                title="Coastal Metrics Trends",
                xaxis_title="Time",
                yaxis_title="Value",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            st.subheader("📊 Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'sea_level' in trend_data.columns:
                    st.metric("Average Sea Level", f"{trend_data['sea_level'].mean():.2f}m")
                else:
                    st.metric("Average Sea Level", "1.25m")
            with col2:
                if 'tide_level' in trend_data.columns:
                    st.metric("Max Tide Level", f"{trend_data['tide_level'].max():.2f}m")
                else:
                    st.metric("Max Tide Level", "3.45m")
            with col3:
                st.metric("Alert Count", 12)
            
            # Export
            if st.button("📤 Export Data"):
                csv = trend_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"coastal_trends_{start_date}_{end_date}.csv",
                    mime="text/csv"
                )
    
    elif page == "🏆 Leaderboard":
        st.header("🏆 Community Leaderboard")
        
        # Demo contributors
        contributors = [
            {'name': 'Demo User', 'role': 'authority', 'points': 150},
            {'name': 'Community Member', 'role': 'community', 'points': 120},
            {'name': 'NGO Representative', 'role': 'ngo', 'points': 95},
            {'name': 'Local Fisher', 'role': 'community', 'points': 80},
            {'name': 'Research Team', 'role': 'authority', 'points': 65}
        ]
        
        # Top 3 with special styling
        if len(contributors) >= 3:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #FFD700, #FFA500); border-radius: 1rem;">
                    <h3>🥇 1st Place</h3>
                    <h2>{contributors[0]['name']}</h2>
                    <h1>{contributors[0]['points']} pts</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #C0C0C0, #A9A9A9); border-radius: 1rem;">
                    <h3>🥈 2nd Place</h3>
                    <h2>{contributors[1]['name']}</h2>
                    <h1>{contributors[1]['points']} pts</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: linear-gradient(45deg, #CD7F32, #B8860B); border-radius: 1rem;">
                    <h3>🥉 3rd Place</h3>
                    <h2>{contributors[2]['name']}</h2>
                    <h1>{contributors[2]['points']} pts</h1>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Full leaderboard
        st.subheader("📊 Full Leaderboard")
        
        for i, contributor in enumerate(contributors, 1):
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                st.markdown(f"**#{i}**")
            
            with col2:
                progress = contributor['points'] / max(c['points'] for c in contributors) if contributors else 0
                st.progress(progress)
                st.markdown(f"**{contributor['name']}** - {contributor['role'].title()}")
            
            with col3:
                st.markdown(f"**{contributor['points']} pts**")
            
            st.markdown("---")
    
    elif page == "⚙️ Settings":
        st.header("⚙️ Settings")
        
        # User preferences
        st.subheader("👤 User Preferences")
        
        with st.form("preferences_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Name", value=user['name'], key="pref_name")
                st.text_input("Email", value=user['email'], key="pref_email")
            
            with col2:
                st.checkbox("SMS Notifications", value=True, key="pref_sms")
                st.checkbox("Email Notifications", value=True, key="pref_email_notif")
                st.checkbox("Push Notifications", value=False, key="pref_push")
            
            if st.form_submit_button("Save Preferences"):
                st.success("✅ Preferences saved!")
        
        # Authority settings
        if user['role'] == 'authority':
            st.subheader("🔧 System Settings")
            
            with st.form("system_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    tide_threshold = st.number_input("Tide Level Threshold (m)", value=3.5, step=0.1)
                    sea_level_threshold = st.number_input("Sea Level Threshold (m)", value=1.5, step=0.1)
                
                with col2:
                    wave_threshold = st.number_input("Wave Height Threshold (m)", value=2.5, step=0.1)
                    wind_threshold = st.number_input("Wind Speed Threshold (km/h)", value=25.0, step=1.0)
                
                if st.form_submit_button("Update Thresholds"):
                    st.success("✅ Thresholds updated!")
        
        # API Keys (for demo)
        st.subheader("🔑 API Access")
        st.info("API keys for sensor data ingestion and external integrations")
        
        if st.button("Generate New API Key"):
            st.success("✅ New API key generated: `demo_api_key_12345`")
        
        # System info
        st.subheader("ℹ️ System Information")
        st.markdown(f"""
        - **Version**: 1.0.0 (Demo Mode)
        - **Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - **Active Users**: 5 (Demo)
        - **Total Reports**: 12 (Demo)
        - **Active Alerts**: 3 (Demo)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌊 Coastal Guardian - AI-Powered Coastal Monitoring & Community Engagement</p>
    <p>Built with ❤️ for coastal conservation | MVP Version 1.0.0</p>
</div>
""", unsafe_allow_html=True)

# Main entry point for running the application
def main():
    """Main entry point for the Coastal Guardian application"""
    print("🌊 Starting Coastal Guardian Application...")
    print("=" * 60)
    
    try:
        # Check if ML components are available
        if ML_AVAILABLE:
            print("✅ ML Anomaly Detection System: Available")
        else:
            print("⚠️ ML Anomaly Detection System: Not Available")
        
        # Check if Streamlit is available
        try:
            import streamlit
            print("✅ Streamlit Web Interface: Available")
        except ImportError:
            print("❌ Streamlit Web Interface: Not Available")
            return
        
        # Start the Streamlit application
        print("🚀 Starting Streamlit web interface...")
        print("📱 Open your browser and navigate to the displayed URL")
        print("🌐 The application will automatically open in your default browser")
        
        # Note: In a real deployment, you would use:
        # subprocess.run(["streamlit", "run", "app.py"])
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
