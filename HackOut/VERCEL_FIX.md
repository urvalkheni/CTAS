# 🚀 CTAS Vercel Deployment - Quick Fix Guide

## ❌ **Current Issue**: Function Runtime Error
The error `Function Runtimes must have a valid version` occurs when Vercel configuration is incorrect.

## ✅ **Solution**: Deploy Frontend Subdirectory

### **Method 1: Vercel Dashboard (Recommended)**

1. **Go to Vercel Dashboard** → Import Project
2. **Connect your GitHub repository** (urvalkheni/CTAS)
3. **Configure build settings**:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```
4. **Deploy**

### **Method 2: Vercel CLI**

```bash
# Navigate to your project root
cd e:\DAIICT_Unstop_Hackout\HackOut

# Login to Vercel
vercel login

# Deploy with specific directory
vercel --cwd frontend

# For production
vercel --cwd frontend --prod
```

### **Method 3: GitHub Integration Fix**

If using GitHub integration, update your **Project Settings**:

1. Go to your Vercel project settings
2. **Build & Development Settings**:
   - Framework Preset: `Vite`
   - Root Directory: `frontend` ←← **IMPORTANT**
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

## 🔧 **Current File Structure Should Be**:

```
HackOut/                          # ← GitHub repo root
├── frontend/                     # ← Vercel Root Directory
│   ├── package.json             # ✅ Fixed (no mongoose)
│   ├── vercel.json              # ✅ Clean config
│   ├── vite.config.js           # ✅ Optimized
│   ├── .nvmrc                   # ✅ Node 18
│   └── src/...
├── backend/
├── ai-models/
└── package.json                 # ← Not used by Vercel
```

## 🎯 **Fix Steps**:

1. **Set Root Directory** in Vercel Dashboard to `frontend`
2. **Redeploy** - The build should now succeed
3. **Your app will be live** at your Vercel URL

## 📝 **Alternative: Move Files to Root** (if you prefer)

If you want to deploy from root instead of subdirectory:

```bash
# Move frontend files to root (backup first!)
cd e:\DAIICT_Unstop_Hackout\HackOut
mv frontend/* .
mv frontend/.* . 2>/dev/null || true
rmdir frontend
```

**The key fix**: Set **Root Directory** to `frontend` in Vercel settings! 🎯
