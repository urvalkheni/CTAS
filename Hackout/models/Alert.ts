import { Schema, model, models } from "mongoose";

const AlertSchema = new Schema({
  type: String,         // storm, pollution, etc.
  severity: String,
  location: String,
  timestamp: { type: Date, default: Date.now }
});

export default models.Alert || model("Alert", AlertSchema);
