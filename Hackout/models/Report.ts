import { Schema, model, models } from "mongoose";

const ReportSchema = new Schema({
  userId: String,
  type: String,
  description: String,
  photo: String,
  location: String,
  status: { type: String, enum: ["pending", "verified"], default: "pending" },
  createdAt: { type: Date, default: Date.now }
});

export default models.Report || model("Report", ReportSchema);
