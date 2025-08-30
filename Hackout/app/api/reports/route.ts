import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import Report from "@/models/Report";

export async function POST(req: Request) {
  try {
    await connectDB();
    const data = await req.json();
    const report = new Report(data);
    await report.save();
    return NextResponse.json({ success: true, report });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function GET() {
  await connectDB();
  const reports = await Report.find();
  return NextResponse.json(reports);
}
