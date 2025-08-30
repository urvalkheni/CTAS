import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Mock reports data
    const reports = [
      {
        id: '1',
        type: 'erosion',
        title: 'Beach Erosion Report',
        description: 'Significant erosion observed at North Beach',
        location: 'North Beach',
        submittedBy: 'John Doe',
        timestamp: new Date().toISOString(),
        status: 'active'
      },
      {
        id: '2',
        type: 'water_quality',
        title: 'Water Quality Report',
        description: 'Water clarity improved at South Bay',
        location: 'South Bay',
        submittedBy: 'Jane Smith',
        timestamp: new Date().toISOString(),
        status: 'active'
      },
      {
        id: '3',
        type: 'wildlife',
        title: 'Wildlife Sighting',
        description: 'Sea turtle nesting activity observed',
        location: 'East Coast',
        submittedBy: 'Mike Johnson',
        timestamp: new Date().toISOString(),
        status: 'active'
      }
    ];
    
    return NextResponse.json({ 
      success: true, 
      reports 
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
    const { type, title, description, location } = await request.json();
    
    // Create new report logic here
    
    return NextResponse.json({ 
      success: true, 
      message: 'Report submitted successfully',
      report: { id: 'new123', type, title, description, location }
    });
    
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      message: 'Internal server error' 
    }, { status: 500 });
  }
}
