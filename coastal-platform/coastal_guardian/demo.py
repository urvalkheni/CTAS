#!/usr/bin/env python3
"""
Coastal Guardian Demo Script
Demonstrates the key features of the Coastal Guardian platform
"""

import pandas as pd
import json
from datetime import datetime
from utils.helpers import (
    load_coastal_data, analyze_threats, load_contributions,
    save_contribution, analyze_mangrove_image, get_leaderboard
)

def demo_coastal_threats():
    """Demonstrate coastal threat analysis"""
    print("🌊 COASTAL THREAT ANALYSIS DEMO")
    print("=" * 50)
    
    # Load sample data
    df = load_coastal_data()
    if df is not None:
        print(f"✅ Loaded {len(df)} coastal data records")
        print(f"📊 Latest tide level: {df['tide_level'].iloc[-1]:.1f}m")
        print(f"📊 Latest sea level: {df['sea_level'].iloc[-1]:.1f}m")
        
        # Analyze threats
        alerts = analyze_threats(df)
        if alerts:
            print("\n🚨 ACTIVE ALERTS:")
            for alert in alerts:
                print(f"  • {alert['type']}: {alert['message']}")
        else:
            print("\n✅ No active threats detected")
    else:
        print("❌ Failed to load coastal data")

def demo_mangrove_watch():
    """Demonstrate mangrove watch features"""
    print("\n🌱 MANGROVE WATCH DEMO")
    print("=" * 50)
    
    # Simulate image analysis
    test_images = ["healthy_mangrove.jpg", "cut_mangrove.png", "unknown.jpg"]
    
    for img in test_images:
        status, confidence = analyze_mangrove_image(img)
        print(f"📸 {img}: {status.upper()} (Confidence: {confidence}%)")
    
    # Show current leaderboard
    leaderboard = get_leaderboard()
    if not leaderboard.empty:
        print("\n🏆 CURRENT LEADERBOARD:")
        print(leaderboard.to_string(index=False))
    else:
        print("\n📋 No contributions yet")

def demo_community_impact():
    """Demonstrate community impact"""
    print("\n👥 COMMUNITY IMPACT DEMO")
    print("=" * 50)
    
    # Load contributions
    contributions = load_contributions()
    
    if contributions["reports"]:
        total_reports = len(contributions["reports"])
        healthy_count = len([r for r in contributions["reports"] if r["status"] == "healthy"])
        total_points = sum(r["points"] for r in contributions["reports"])
        
        print(f"📊 Total Reports: {total_reports}")
        print(f"✅ Healthy Mangroves: {healthy_count}")
        print(f"❌ Cut Mangroves: {total_reports - healthy_count}")
        print(f"🏆 Total Points: {total_points}")
        
        # Show recent reports
        print("\n📋 RECENT REPORTS:")
        for report in contributions["reports"][-3:]:
            status_icon = "✅" if report['status'] == 'healthy' else "❌"
            print(f"  {status_icon} {report['user']} - {report['location']} ({report['points']} pts)")
    else:
        print("📋 No community reports yet")

def demo_data_export():
    """Demonstrate data export functionality"""
    print("\n📤 DATA EXPORT DEMO")
    print("=" * 50)
    
    # Export coastal data
    df = load_coastal_data()
    if df is not None:
        csv_data = df.to_csv(index=False)
        print(f"📊 Coastal data exported: {len(csv_data)} characters")
    
    # Export contributions
    contributions = load_contributions()
    if contributions["reports"]:
        reports_df = pd.DataFrame(contributions["reports"])
        csv_data = reports_df.to_csv(index=False)
        print(f"📋 Reports exported: {len(csv_data)} characters")

def main():
    """Run all demos"""
    print("🌊 COASTAL GUARDIAN - FEATURE DEMONSTRATION")
    print("=" * 60)
    print(f"🕐 Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        demo_coastal_threats()
        demo_mangrove_watch()
        demo_community_impact()
        demo_data_export()
        
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("🌊 Coastal Guardian is ready for coastal conservation!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")

if __name__ == "__main__":
    main()
