import { NextResponse } from "next/server";
import { connectDB } from "../../../lib/mongodb";
import User from "../../../models/User";

export async function GET() {
  try {
    await connectDB();
    const users = await User.find().sort({ points: -1 }).limit(10);
    return NextResponse.json(users);
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
