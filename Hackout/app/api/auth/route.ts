import { NextRequest, NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';

export async function POST(request: NextRequest) {
  try {
    const { email, password, action } = await request.json();
    
    if (action === 'login') {
      // Handle login logic
      return NextResponse.json({ 
        success: true, 
        message: 'Login successful',
        user: { email, id: 'user123' }
      });
    } else if (action === 'register') {
      // Handle registration logic
      const hashedPassword = await bcrypt.hash(password, 12);
      
      return NextResponse.json({ 
        success: true, 
        message: 'Registration successful',
        user: { email, id: 'user123' }
      });
    }
    
    return NextResponse.json({ 
      success: false, 
      message: 'Invalid action' 
    }, { status: 400 });
    
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      message: 'Internal server error' 
    }, { status: 500 });
  }
}
