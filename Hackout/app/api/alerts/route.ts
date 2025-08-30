import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Mock alerts data
    const alerts = [
      {
        id: '1',
        type: 'high_tide',
        severity: 'warning',
        title: 'High Tide Warning',
        message: 'Expected high tide at 2:30 PM today. Coastal flooding possible.',
        location: 'Main Beach',
        timestamp: new Date().toISOString(),
        active: true
      },
      {
        id: '2',
        type: 'storm',
        severity: 'watch',
        title: 'Storm Watch',
        message: 'Strong winds expected tomorrow. Secure loose objects.',
        location: 'Coastal Area',
        timestamp: new Date().toISOString(),
        active: true
      },
      {
        id: '3',
        type: 'water_quality',
        severity: 'alert',
        title: 'Water Quality Alert',
        message: 'Elevated bacteria levels detected at Main Beach.',
        location: 'Main Beach',
        timestamp: new Date().toISOString(),
        active: true
      }
    ];
    
    return NextResponse.json({ 
      success: true, 
      alerts 
    });
    
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      message: 'Internal server error' 
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const { type, severity, title, message, location } = await request.json();
    
    // Create new alert logic here
    
    return NextResponse.json({ 
      success: true, 
      message: 'Alert created successfully',
      alert: { id: 'new123', type, severity, title, message, location }
    });
    
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      message: 'Internal server error' 
    }, { status: 500 });
  }
}
