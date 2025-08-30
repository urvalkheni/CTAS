import { NextResponse } from "next/server";
import { connectDB } from "../../../lib/mongodb";
import Alert from "../../../models/Alert";

export async function POST(req: Request) {
  try {
    await connectDB();
    const data = await req.json();
    const alert = new Alert(data);
    await alert.save();
    return NextResponse.json({ success: true, alert });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function GET() {
  await connectDB();
  const alerts = await Alert.find();
  return NextResponse.json(alerts);
}
