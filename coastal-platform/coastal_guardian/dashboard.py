import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import json
import numpy as np
from datetime import datetime, timedelta
import altair as alt
import os

# Page configuration
st.set_page_config(
    page_title="Coastal Guardian Platform",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "Professional Dark"
if 'animation_mode' not in st.session_state:
    st.session_state.animation_mode = "on"
if 'notifications' not in st.session_state:
    st.session_state.notifications = {"SMS": True, "Email": True}

# Custom CSS for professional themes with animations
def get_css(theme, animation_mode="on"):
    base_animations = """
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(0,0,0,0.1); }
        50% { box-shadow: 0 0 20px rgba(0,0,0,0.3); }
        100% { box-shadow: 0 0 5px rgba(0,0,0,0.1); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    """
    
    animation_class = "animate" if animation_mode == "on" else ""
    
    if theme == "Professional Dark":
        return f"""
        <style>
        {base_animations}
        
        .stApp {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .stPlotlyChart {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        .metric-container {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin: 0.5rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .metric-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
            border-color: rgba(255, 255, 255, 0.3);
        }}
        
        .alert-critical {{
            background: linear-gradient(135deg, rgba(244, 67, 54, 0.2) 0%, rgba(244, 67, 54, 0.1) 100%);
            border-left: 6px solid #f44336;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 8px 32px rgba(244, 67, 54, 0.3);
            backdrop-filter: blur(10px);
            {f'animation: pulse 2s infinite;' if animation_mode == "on" else ''}
        }}
        
        .alert-high {{
            background: linear-gradient(135deg, rgba(255, 152, 0, 0.2) 0%, rgba(255, 152, 0, 0.1) 100%);
            border-left: 6px solid #ff9800;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 8px 32px rgba(255, 152, 0, 0.3);
            backdrop-filter: blur(10px);
            {f'animation: slideInLeft 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .alert-moderate {{
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0.1) 100%);
            border-left: 6px solid #4caf50;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
            backdrop-filter: blur(10px);
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .stDataFrame {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 10px;
            backdrop-filter: blur(10px);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            transition: all 0.3s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 34px;
            transition: 0.4s;
            cursor: pointer;
        }}
        
        .toggle-switch.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .toggle-slider {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            border-radius: 50%;
            transition: 0.4s;
        }}
        
        .toggle-switch.active .toggle-slider {{
            transform: translateX(26px);
        }}
        
        .header-animation {{
            {f'animation: float 3s ease-in-out infinite;' if animation_mode == "on" else ''}
        }}
        </style>
        """
    
    elif theme == "Modern Light":
        return f"""
        <style>
        {base_animations}
        
        .stApp {{
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
            color: #1e293b;
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .stPlotlyChart {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-container {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .metric-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            border-color: #3b82f6;
        }}
        
        .alert-critical {{
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border-left: 6px solid #ef4444;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.2);
            {f'animation: pulse 2s infinite;' if animation_mode == "on" else ''}
        }}
        
        .alert-high {{
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border-left: 6px solid #f59e0b;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
            {f'animation: slideInLeft 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .alert-moderate {{
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-left: 6px solid #22c55e;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(34, 197, 94, 0.2);
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .stDataFrame {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            color: #1e293b;
            transition: all 0.3s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }}
        
        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            background-color: #e5e7eb;
            border-radius: 34px;
            transition: 0.4s;
            cursor: pointer;
        }}
        
        .toggle-switch.active {{
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        }}
        
        .toggle-slider {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            border-radius: 50%;
            transition: 0.4s;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .toggle-switch.active .toggle-slider {{
            transform: translateX(26px);
        }}
        
        .header-animation {{
            {f'animation: float 3s ease-in-out infinite;' if animation_mode == "on" else ''}
        }}
        </style>
        """
    
    elif theme == "Ocean Professional":
        return f"""
        <style>
        {base_animations}
        
        .stApp {{
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .stPlotlyChart {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        }}
        
        .metric-container {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .metric-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
        }}
        
        .alert-critical {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
            border-left: 6px solid #ef4444;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
            backdrop-filter: blur(10px);
            {f'animation: pulse 2s infinite;' if animation_mode == "on" else ''}
        }}
        
        .alert-high {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
            border-left: 6px solid #f59e0b;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
            backdrop-filter: blur(10px);
            {f'animation: slideInLeft 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .alert-moderate {{
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
            border-left: 6px solid #22c55e;
            padding: 2rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            box-shadow: 0 10px 30px rgba(34, 197, 94, 0.3);
            backdrop-filter: blur(10px);
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .stDataFrame {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 10px;
            backdrop-filter: blur(10px);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            transition: all 0.3s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
        }}
        
        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 34px;
            transition: 0.4s;
            cursor: pointer;
        }}
        
        .toggle-switch.active {{
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        }}
        
        .toggle-slider {{
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            border-radius: 50%;
            transition: 0.4s;
        }}
        
        .toggle-switch.active .toggle-slider {{
            transform: translateX(26px);
        }}
        
        .header-animation {{
            {f'animation: float 3s ease-in-out infinite;' if animation_mode == "on" else ''}
        }}
        </style>
        """
    
    else:  # Minimal Clean
        return f"""
        <style>
        {base_animations}
        
        .stApp {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
            color: #334155;
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        .stPlotlyChart {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        
        .metric-container {{
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .metric-container:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
            border-color: #cbd5e1;
        }}
        
        .alert-critical {{
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border-left: 4px solid #ef4444;
            padding: 1.5rem;
            border-radius: 16px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(239, 68, 68, 0.1);
            {f'animation: pulse 2s infinite;' if animation_mode == "on" else ''}
        }}
        
        .alert-high {{
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border-left: 4px solid #f59e0b;
            padding: 1.5rem;
            border-radius: 16px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(245, 158, 11, 0.1);
            {f'animation: slideInLeft 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .alert-moderate {{
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-left: 4px solid #22c55e;
            padding: 1.5rem;
            border-radius: 16px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(34, 197, 94, 0.1);
            {f'animation: fadeInUp 0.6s ease-out;' if animation_mode == "on" else ''}
        }}
        
        .stDataFrame {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            color: #334155;
            transition: all 0.3s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #64748b 0%, #475569 100%);
            color: white;
            box-shadow: 0 2px 4px rgba(100, 116, 139, 0.3);
        }}
        
        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 50px;
            height: 28px;
            background-color: #e2e8f0;
            border-radius: 28px;
            transition: 0.4s;
            cursor: pointer;
        }}
        
        .toggle-switch.active {{
            background: linear-gradient(135deg, #64748b 0%, #475569 100%);
        }}
        
        .toggle-slider {{
            position: absolute;
            content: "";
            height: 20px;
            width: 20px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            border-radius: 50%;
            transition: 0.4s;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }}
        
        .toggle-switch.active .toggle-slider {{
            transform: translateX(22px);
        }}
        
        .header-animation {{
            {f'animation: float 3s ease-in-out infinite;' if animation_mode == "on" else ''}
        }}
        </style>
        """

# Navigation sidebar
def create_navigation():
    st.sidebar.title("🌊 Coastal Guardian")
    st.sidebar.markdown("---")
    
    # Navigation menu
    pages = {
        "🏠 Dashboard": "Dashboard",
        "🚨 Live Alerts": "Live Alerts", 
        "📋 Incident Reports": "Incident Reports",
        "🏆 Mangrove Leaderboard": "Leaderboard",
        "📈 Sea-Level Trends": "Trends",
        "⚙️ Settings": "Settings"
    }
    
    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name, key=page_key):
            st.session_state.current_page = page_key
    
    # Theme toggle
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Theme Settings")
    
    theme = st.sidebar.selectbox(
        "Theme:",
        ["Professional Dark", "Modern Light", "Ocean Professional", "Minimal Clean"],
        index=["Professional Dark", "Modern Light", "Ocean Professional", "Minimal Clean"].index(st.session_state.theme_mode)
    )
    st.session_state.theme_mode = theme
    
    # Animation toggle
    animation = st.sidebar.selectbox(
        "Animations:",
        ["on", "off"],
        index=["on", "off"].index(st.session_state.animation_mode)
    )
    st.session_state.animation_mode = animation
    
    # Quick stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    # Load data for stats
    df, alerts_data = load_data()
    if df is not None:
        predictions_df = create_predictions_df(df)
        if predictions_df is not None:
            alert_count = len(predictions_df[predictions_df['anomaly'] == -1])
            st.sidebar.metric("Active Alerts", alert_count)
            st.sidebar.metric("Data Points", len(predictions_df))
    
    return theme, animation

# Create predictions dataframe with anomaly detection
def create_predictions_df(df):
    if df is None:
        return None
    
    # Pivot the data to get different metrics as columns
    df_pivot = df.pivot_table(
        index='timestamp', 
        columns='type', 
        values='value', 
        aggfunc='mean'
    ).reset_index()
    
    # Add anomaly detection (simplified)
    df_pivot['anomaly'] = 0
    df_pivot.loc[df_pivot['tide'] > 4.0, 'anomaly'] = -1  # High tide alert
    df_pivot.loc[df_pivot['wave_height'] > 2.5, 'anomaly'] = -1  # High wave alert
    df_pivot.loc[df_pivot['wind_speed'] > 20.0, 'anomaly'] = -1  # High wind alert
    
    return df_pivot

# Create interactive map
def create_map(df, alerts_data):
    if df is None:
        return None
    
    # Get unique locations
    locations = df[['lat', 'lng']].drop_duplicates()
    
    # Create map centered on Mumbai
    m = folium.Map(
        location=[19.0760, 72.8777],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add sensor markers
    for idx, row in locations.iterrows():
        folium.Marker(
            [row['lat'], row['lng']],
            popup=f"Sensor Location<br>Lat: {row['lat']}<br>Lng: {row['lng']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    
    # Add alert markers if any
    if alerts_data and 'alerts' in alerts_data:
        for alert in alerts_data['alerts']:
            folium.Marker(
                [alert.get('lat', 19.0760), alert.get('lng', 72.8777)],
                popup=f"Alert: {alert.get('message', 'Coastal Threat')}",
                icon=folium.Icon(color='red', icon='warning-sign')
            ).add_to(m)
    
    return m

# Dashboard page
def dashboard_page():
    # Header
    st.markdown(
        """
        <div class="header-animation" style='text-align: center; padding: 3rem 0;'>
            <h1 style='color: inherit; font-size: 3.5rem; margin-bottom: 0.5rem; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                🌊 Coastal Guardian Dashboard
            </h1>
            <h3 style='color: inherit; font-weight: 400; margin-top: 0; font-size: 1.5rem; opacity: 0.9;'>
                Real-time Monitoring & Early Warnings
            </h3>
            <p style='font-style: italic; margin-top: 1.5rem; font-size: 1.1rem; opacity: 0.8;'>
                Protecting our coastlines through intelligent monitoring and community engagement
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load data
    df, alerts_data = load_data()
    if df is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    predictions_df = create_predictions_df(df)
    if predictions_df is None:
        st.error("Failed to process data.")
        return
    
    # Metrics section
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; margin: 2rem 0;'>
            <h2 style='color: inherit; font-size: 2rem; margin-bottom: 1rem;'>
                📊 Real-time Coastal Metrics
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-container">
                <h3 style='text-align: center; margin-bottom: 1rem;'>🌊 Max Tide Level</h3>
                <div style='text-align: center; font-size: 2rem; font-weight: bold;'>
                    {predictions_df['tide'].max():.1f}m
                </div>
                <div style='text-align: center; font-size: 0.9rem; color: #666;'>
                    Avg: {predictions_df['tide'].mean():.1f}m
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-container">
                <h3 style='text-align: center; margin-bottom: 1rem;'>🌊 Max Wave Height</h3>
                <div style='text-align: center; font-size: 2rem; font-weight: bold;'>
                    {predictions_df['wave_height'].max():.1f}m
                </div>
                <div style='text-align: center; font-size: 0.9rem; color: #666;'>
                    Avg: {predictions_df['wave_height'].mean():.1f}m
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-container">
                <h3 style='text-align: center; margin-bottom: 1rem;'>💨 Max Wind Speed</h3>
                <div style='text-align: center; font-size: 2rem; font-weight: bold;'>
                    {predictions_df['wind_speed'].max():.1f} km/h
                </div>
                <div style='text-align: center; font-size: 0.9rem; color: #666;'>
                    Avg: {predictions_df['wind_speed'].mean():.1f} km/h
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        alert_count = len(predictions_df[predictions_df['anomaly'] == -1])
        st.markdown(
            f"""
            <div class="metric-container">
                <h3 style='text-align: center; margin-bottom: 1rem;'>⚠️ Active Alerts</h3>
                <div style='text-align: center; font-size: 2rem; font-weight: bold; color: #f44336;'>
                    {alert_count}
                </div>
                <div style='text-align: center; font-size: 0.9rem; color: #666;'>
                    Critical Threats
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Charts section
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; margin: 2rem 0;'>
            <h2 style='color: inherit; font-size: 2rem; margin-bottom: 1rem;'>
                📈 Real-time Monitoring Charts
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🌊 Tide Levels", "🌊 Wave Heights", "💨 Wind Speed", "📊 Combined View"])
    
    with tab1:
        # Tide Levels with Anomaly Detection
        fig_tide = px.line(
            predictions_df, 
            x="timestamp", 
            y="tide", 
            title="Tide Levels with Anomaly Detection",
            color_discrete_sequence=['#1f77b4']
        )
        
        # Add anomaly points
        anomalies = predictions_df[predictions_df['anomaly'] == -1]
        if not anomalies.empty:
            fig_tide.add_scatter(
                x=anomalies['timestamp'],
                y=anomalies['tide'],
                mode='markers',
                marker=dict(color='red', size=10, symbol='x'),
                name='Anomalies'
            )
        
        fig_tide.update_layout(
            xaxis_title="Time",
            yaxis_title="Tide Level (m)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_tide, use_container_width=True)
    
    with tab2:
        # Wave Heights
        fig_wave = px.line(
            predictions_df, 
            x="timestamp", 
            y="wave_height", 
            title="Wave Heights Over Time",
            color_discrete_sequence=['#ff7f0e']
        )
        
        # Add threshold line
        fig_wave.add_hline(
            y=2.5, 
            line_dash="dash", 
            line_color="red",
            annotation_text="High Wave Threshold (2.5m)"
        )
        
        fig_wave.update_layout(
            xaxis_title="Time",
            yaxis_title="Wave Height (m)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_wave, use_container_width=True)
    
    with tab3:
        # Wind Speed
        fig_wind = px.line(
            predictions_df, 
            x="timestamp", 
            y="wind_speed", 
            title="Wind Speed Over Time",
            color_discrete_sequence=['#2ca02c']
        )
        
        # Add threshold line
        fig_wind.add_hline(
            y=20.0, 
            line_dash="dash", 
            line_color="orange",
            annotation_text="High Wind Threshold (20 km/h)"
        )
        
        fig_wind.update_layout(
            xaxis_title="Time",
            yaxis_title="Wind Speed (km/h)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_wind, use_container_width=True)
    
    with tab4:
        # Combined view using Altair
        if 'tide' in predictions_df.columns and 'wave_height' in predictions_df.columns and 'wind_speed' in predictions_df.columns:
            # Prepare data for Altair
            chart_data = predictions_df[['timestamp', 'tide', 'wave_height', 'wind_speed']].melt(
                id_vars=['timestamp'], 
                var_name='metric', 
                value_name='value'
            )
            
            # Create Altair chart
            chart = alt.Chart(chart_data).mark_line().encode(
                x=alt.X('timestamp:T', title='Time'),
                y=alt.Y('value:Q', title='Value'),
                color=alt.Color('metric:N', title='Metric'),
                tooltip=['timestamp', 'metric', 'value']
            ).properties(
                title='Combined Coastal Metrics',
                width='container',
                height=400
            )
            
            st.altair_chart(chart, use_container_width=True)

# Live Alerts page
def alerts_page():
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: inherit; font-size: 3rem; margin-bottom: 0.5rem;'>
                🚨 Live Alerts
            </h1>
            <p style='font-style: italic; color: #666;'>
                Real-time coastal threat alerts and warnings
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load data
    df, alerts_data = load_data()
    if df is None:
        st.error("Failed to load data.")
        return
    
    predictions_df = create_predictions_df(df)
    if predictions_df is None:
        st.error("Failed to process data.")
        return
    
    # Current alerts
    alerts = predictions_df[predictions_df['anomaly'] == -1]
    
    if not alerts.empty:
        st.markdown("### ⚠️ Active Coastal Alerts")
        
        for idx, alert in alerts.iterrows():
            if alert['tide'] > 4.0:
                st.markdown(
                    f"""
                    <div class="alert-critical">
                    <strong>🚨 High Tide Alert</strong><br>
                    Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}<br>
                    Tide Level: {alert['tide']:.1f}m (Threshold: 4.0m)<br>
                    Location: Mumbai Gateway
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            if alert['wave_height'] > 2.5:
                st.markdown(
                    f"""
                    <div class="alert-high">
                    <strong>🌊 High Wave Alert</strong><br>
                    Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}<br>
                    Wave Height: {alert['wave_height']:.1f}m (Threshold: 2.5m)<br>
                    Location: Mumbai Gateway
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            if alert['wind_speed'] > 20.0:
                st.markdown(
                    f"""
                    <div class="alert-moderate">
                    <strong>💨 High Wind Alert</strong><br>
                    Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}<br>
                    Wind Speed: {alert['wind_speed']:.1f} km/h (Threshold: 20 km/h)<br>
                    Location: Mumbai Gateway
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.success("✅ No active alerts at this time.")
    
    # Map view
    st.markdown("---")
    st.markdown("### 🗺️ Alert Locations")
    
    map_obj = create_map(df, alerts_data)
    if map_obj:
        st_folium(map_obj, width=800, height=400)

# Incident Reports page
def reports_page():
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: inherit; font-size: 3rem; margin-bottom: 0.5rem;'>
                📋 Community Reports
            </h1>
            <p style='font-style: italic; color: #666;'>
                Mangrove Watch - Community-driven incident reporting
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load reports
    reports_data = load_reports()
    if reports_data is None:
        st.error("Failed to load reports.")
        return
    
    # Filter options
    col1, col2 = st.columns([1, 2])
    with col1:
        incident_type = st.selectbox(
            "Filter by Incident Type:",
            ["All", "Dumping", "Cutting", "Pollution"]
        )
    
    # Filter reports
    reports = reports_data.get('reports', [])
    if incident_type != "All":
        reports = [r for r in reports if r['type'] == incident_type]
    
    # Display reports
    for report in reports:
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if report.get('photo_url') and os.path.exists(report['photo_url']):
                    st.image(report['photo_url'], width=150)
                else:
                    st.markdown("📷 No photo")
            
            with col2:
                severity_color = {
                    'critical': '#f44336',
                    'high': '#ff9800', 
                    'moderate': '#4caf50'
                }.get(report['severity'], '#666')
                
                st.markdown(
                    f"""
                    <div style='border-left: 4px solid {severity_color}; padding-left: 1rem; margin: 1rem 0;'>
                        <h3>{report['type']} - {report['location']}</h3>
                        <p><strong>Reported by:</strong> {report['user']}</p>
                        <p><strong>Time:</strong> {report['timestamp']}</p>
                        <p><strong>Description:</strong> {report['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Map view
    st.markdown("---")
    st.markdown("### 🗺️ Incident Locations")
    
    if reports:
        # Create map for reports
        m = folium.Map(
            location=[20.5937, 78.9629],  # Center of India
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        for report in reports:
            folium.Marker(
                [report['lat'], report['lng']],
                popup=f"""
                <b>{report['type']}</b><br>
                {report['location']}<br>
                {report['description']}<br>
                Reported by: {report['user']}
                """,
                icon=folium.Icon(
                    color='red' if report['severity'] == 'critical' else 'orange' if report['severity'] == 'high' else 'green',
                    icon='warning-sign'
                )
            ).add_to(m)
        
        st_folium(m, width=800, height=400)

# Leaderboard page
def leaderboard_page():
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: inherit; font-size: 3rem; margin-bottom: 0.5rem;'>
                🏆 Mangrove Leaderboard
            </h1>
            <p style='font-style: italic; color: #666;'>
                Top contributors in coastal protection
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Get leaderboard data
    leaderboard_df = create_leaderboard()
    
    if not leaderboard_df.empty:
        # Top 3 with special styling
        st.markdown("### 🥇 Top Contributors")
        
        for idx, row in leaderboard_df.head(3).iterrows():
            badge = "🥇" if row['Rank'] == 1 else "🥈" if row['Rank'] == 2 else "🥉"
            st.markdown(
                f"""
                <div class="metric-container" style='text-align: center;'>
                    <h2>{badge} {row['User']}</h2>
                    <p><strong>{row['Reports']}</strong> reports submitted</p>
                    <p>Rank #{row['Rank']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Full leaderboard
        st.markdown("---")
        st.markdown("### 📊 Complete Leaderboard")
        
        # Create bar chart
        fig = px.bar(
            leaderboard_df,
            x='User',
            y='Reports',
            title='Reports by User',
            color='Reports',
            color_continuous_scale='viridis'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Table view
        st.dataframe(leaderboard_df, use_container_width=True)
    else:
        st.info("No reports data available yet.")

# Trends page
def trends_page():
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: inherit; font-size: 3rem; margin-bottom: 0.5rem;'>
                📈 Sea-Level Trends
            </h1>
            <p style='font-style: italic; color: #666;'>
                Historical analysis and forecasting
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load data
    df, alerts_data = load_data()
    if df is None:
        st.error("Failed to load data.")
        return
    
    predictions_df = create_predictions_df(df)
    if predictions_df is None:
        st.error("Failed to process data.")
        return
    
    # Monthly trends
    predictions_df['month'] = predictions_df['timestamp'].dt.to_period('M')
    monthly_data = predictions_df.groupby('month').agg({
        'tide': 'mean',
        'wave_height': 'mean', 
        'wind_speed': 'mean',
        'anomaly': 'sum'
    }).reset_index()
    monthly_data['month'] = monthly_data['month'].astype(str)
    
    # Sea level trends
    st.markdown("### 🌊 Monthly Sea Level Trends")
    fig_trend = px.line(
        monthly_data,
        x='month',
        y='tide',
        title='Average Monthly Tide Levels',
        markers=True
    )
    fig_trend.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Incident trends
    st.markdown("### 📊 Monthly Incident Counts")
    fig_incidents = px.bar(
        monthly_data,
        x='month',
        y='anomaly',
        title='Monthly Anomaly Counts',
        color='anomaly',
        color_continuous_scale='reds'
    )
    fig_incidents.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_incidents, use_container_width=True)
    
    # Correlation analysis
    st.markdown("### 🔍 Correlation Analysis")
    correlation_data = predictions_df[['tide', 'wave_height', 'wind_speed']].corr()
    fig_corr = px.imshow(
        correlation_data,
        title='Correlation Matrix',
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# Settings page
def settings_page():
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: inherit; font-size: 3rem; margin-bottom: 0.5rem;'>
                ⚙️ Settings
            </h1>
            <p style='font-style: italic; color: #666;'>
                Customize your Coastal Guardian experience
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Theme settings
    st.markdown("### 🎨 Appearance")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Theme Mode:**")
        theme = st.selectbox(
            "",
            ["Professional Dark", "Modern Light", "Ocean Professional", "Minimal Clean"],
            index=["Professional Dark", "Modern Light", "Ocean Professional", "Minimal Clean"].index(st.session_state.theme_mode),
            label_visibility="collapsed"
        )
        st.session_state.theme_mode = theme
    
    with col2:
        st.markdown("**Animation Mode:**")
        animation = st.selectbox(
            "",
            ["on", "off"],
            index=["on", "off"].index(st.session_state.animation_mode),
            label_visibility="collapsed"
        )
        st.session_state.animation_mode = animation
    
    # Notification settings
    st.markdown("### 🔔 Notification Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        sms_notifications = st.checkbox(
            "📱 SMS Notifications",
            value=st.session_state.notifications["SMS"]
        )
        st.session_state.notifications["SMS"] = sms_notifications
    
    with col2:
        email_notifications = st.checkbox(
            "📧 Email Notifications", 
            value=st.session_state.notifications["Email"]
        )
        st.session_state.notifications["Email"] = email_notifications
    
    # Alert thresholds
    st.markdown("### ⚠️ Alert Thresholds")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        tide_threshold = st.number_input(
            "Tide Level Threshold (m):",
            min_value=1.0,
            max_value=10.0,
            value=4.0,
            step=0.1
        )
    
    with col2:
        wave_threshold = st.number_input(
            "Wave Height Threshold (m):",
            min_value=0.5,
            max_value=5.0,
            value=2.5,
            step=0.1
        )
    
    with col3:
        wind_threshold = st.number_input(
            "Wind Speed Threshold (km/h):",
            min_value=10.0,
            max_value=50.0,
            value=20.0,
            step=1.0
        )
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
    
    # System info
    st.markdown("---")
    st.markdown("### ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Current Theme:** {st.session_state.theme_mode}")
        st.info(f"**Animations:** {st.session_state.animation_mode}")
    
    with col2:
        st.info(f"**SMS Notifications:** {'Enabled' if st.session_state.notifications['SMS'] else 'Disabled'}")
        st.info(f"**Email Notifications:** {'Enabled' if st.session_state.notifications['Email'] else 'Disabled'}")

# Load reports data
@st.cache_data
def load_reports():
    try:
        if os.path.exists("data/reports.json"):
            with open("data/reports.json", "r") as f:
                return json.load(f)
        else:
            # Create sample reports data
            sample_reports = {
                "reports": [
                    {
                        "id": "report_001",
                        "user": "CoastalGuard_001",
                        "timestamp": "2024-01-15 14:30:00",
                        "type": "Dumping",
                        "location": "Chennai Coast",
                        "lat": 13.0827,
                        "lng": 80.2707,
                        "description": "Plastic waste dumping observed",
                        "photo_url": "reports/20250830_083754_WhatsApp Image 2025-08-30 at 02.58.26_5744a527.jpg",
                        "severity": "high"
                    },
                    {
                        "id": "report_002", 
                        "user": "MangroveWatcher_002",
                        "timestamp": "2024-01-14 09:15:00",
                        "type": "Cutting",
                        "location": "Mumbai Gateway",
                        "lat": 19.0760,
                        "lng": 72.8777,
                        "description": "Unauthorized mangrove cutting",
                        "photo_url": "",
                        "severity": "critical"
                    },
                    {
                        "id": "report_003",
                        "user": "EcoVolunteer_003", 
                        "timestamp": "2024-01-13 16:45:00",
                        "type": "Pollution",
                        "location": "Goa Beach",
                        "lat": 15.2993,
                        "lng": 74.1240,
                        "description": "Oil spill detected",
                        "photo_url": "",
                        "severity": "moderate"
                    }
                ]
            }
            return sample_reports
    except Exception as e:
        st.error(f"Error loading reports: {e}")
        return None

# Create leaderboard data
def create_leaderboard():
    reports_data = load_reports()
    if reports_data and 'reports' in reports_data:
        user_counts = {}
        for report in reports_data['reports']:
            user = report['user']
            user_counts[user] = user_counts.get(user, 0) + 1
        
        # Create leaderboard dataframe
        leaderboard_data = []
        for user, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True):
            leaderboard_data.append({
                'User': user,
                'Reports': count,
                'Rank': len(leaderboard_data) + 1
            })
        
        return pd.DataFrame(leaderboard_data)
    return pd.DataFrame()

# Load and process data
@st.cache_data
def load_data():
    try:
        # Load sensor data
        df = pd.read_csv("data/sample_sensor_data.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Load alerts
        with open("data/alerts.json", "r") as f:
            alerts_data = json.load(f)
        
        return df, alerts_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Main application
def main():
    # Create navigation and get theme settings
    theme, animation = create_navigation()
    
    # Apply CSS with current theme and animation settings
    st.markdown(get_css(st.session_state.theme_mode, st.session_state.animation_mode), unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.current_page == "Dashboard":
        dashboard_page()
    elif st.session_state.current_page == "Live Alerts":
        alerts_page()
    elif st.session_state.current_page == "Incident Reports":
        reports_page()
    elif st.session_state.current_page == "Leaderboard":
        leaderboard_page()
    elif st.session_state.current_page == "Trends":
        trends_page()
    elif st.session_state.current_page == "Settings":
        settings_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
