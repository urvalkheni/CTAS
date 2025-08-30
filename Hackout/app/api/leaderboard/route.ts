import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Mock leaderboard data
    const leaderboard = [
      {
        rank: 1,
        userId: 'user1',
        name: 'Sarah Wilson',
        reports: 45,
        points: 1250,
        avatar: '/avatars/sarah.jpg'
      },
      {
        rank: 2,
        userId: 'user2',
        name: 'Mike Johnson',
        reports: 38,
        points: 1120,
        avatar: '/avatars/mike.jpg'
      },
      {
        rank: 3,
        userId: 'user3',
        name: 'Emily Davis',
        reports: 32,
        points: 980,
        avatar: '/avatars/emily.jpg'
      },
      {
        rank: 4,
        userId: 'user4',
        name: 'David Brown',
        reports: 28,
        points: 850,
        avatar: '/avatars/david.jpg'
      },
      {
        rank: 5,
        userId: 'user5',
        name: 'Lisa Chen',
        reports: 25,
        points: 720,
        avatar: '/avatars/lisa.jpg'
      }
    ];
    
    return NextResponse.json({ 
      success: true, 
      leaderboard 
    });
    
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      message: 'Internal server error' 
    }, { status: 500 });
  }
}
