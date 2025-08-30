import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta
import numpy as np

# Try to import folium, but handle gracefully if not available
try:
    import folium
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

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
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .alert-critical { background-color: #ffebee; border-left: 4px solid #d32f2f; }
    .alert-high { background-color: #fff3e0; border-left: 4px solid #f57c00; }
    .alert-moderate { background-color: #fff8e1; border-left: 4px solid #ffa000; }
    .alert-low { background-color: #f1f8e9; border-left: 4px solid #689f38; }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    .role-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .role-authority { background-color: #e3f2fd; color: #1976d2; }
    .role-ngo { background-color: #f3e5f5; color: #7b1fa2; }
    .role-community { background-color: #e8f5e8; color: #388e3c; }
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

# Sidebar - Authentication & Navigation
st.sidebar.title("🌊 Coastal Guardian")
st.sidebar.markdown("---")

# Authentication
if 'user' not in st.session_state:
    st.session_state.user = None

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
    
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["🏠 Dashboard", "🚨 Threats & Alerts", "📊 Reports", "📈 Trends", "🏆 Leaderboard", "⚙️ Settings"]
    )

# Main content based on authentication
if st.session_state.user is None:
    # Landing page
    st.markdown('<h1 class="main-header">🌊 Coastal Guardian</h1>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Coastal Monitoring & Community Engagement Platform")
    
    # Login call-to-action
    st.markdown("---")
    st.markdown("### 🔐 Get Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🚀 Quick Demo
        Experience the platform instantly with pre-loaded data and mock scenarios.
        
        **Perfect for:**
        - Hackathon demos
        - First-time users
        - Quick exploration
        """)
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
    
    with col2:
        st.markdown("""
        #### 🔐 Full Login
        Access role-based features with proper authentication.
        
        **Demo Accounts:**
        - **Authority**: `admin@coastalguardian.com` / `password123`
        - **NGO**: `ngo@coastalguardian.com` / `password123`
        - **Community**: `community@coastalguardian.com` / `password123`
        """)
        st.info("💡 Use the sidebar to login with these credentials!")
    
    st.markdown("---")
    
    # Features overview
    st.markdown("### 🌟 Platform Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🚨 Real-time Threat Detection
        - AI-powered anomaly detection
        - Multi-source data integration
        - Instant alert generation
        - Severity scoring (0-100)
        """)
    
    with col2:
        st.markdown("""
        #### 👥 Community Engagement
        - Citizen science reporting
        - Gamified participation
        - Location-based alerts
        - Leaderboard system
        """)
    
    with col3:
        st.markdown("""
        #### 📊 Comprehensive Analytics
        - Interactive dashboards
        - Trend analysis
        - Export capabilities
        - Real-time maps
        """)

else:
    # Authenticated user interface
    user = st.session_state.user
    
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
                st_folium(m, width=800, height=400)
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
