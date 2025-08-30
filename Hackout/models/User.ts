import { Schema, model, models } from "mongoose";

const UserSchema = new Schema({
  name: String,
  email: { type: String, unique: true },
  password: String,
  role: { type: String, enum: ["authority", "ngo", "community"], default: "community" },
  location: String,
  points: { type: Number, default: 0 }
});

export default models.User || model("User", UserSchema);
