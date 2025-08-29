# Shore Guard Connect

**Smart Coastal Protection & Mangrove Watch Platform**

A full-stack web application for real-time coastal threat monitoring and community-driven mangrove conservation.

## 🏗️ Project Structure

```
shore-guard-connect/
├── frontend/                 # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── hooks/           # Custom React hooks
│   │   └── lib/             # Utility functions
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                  # Node.js + Express Backend
│   ├── routes/              # API route handlers
│   ├── controllers/         # Business logic
│   ├── middleware/          # Custom middleware
│   ├── models/              # Data models (future)
│   ├── server.js            # Main server file
│   └── package.json         # Backend dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:8080`

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Start development server
npm run dev
```

Backend will run on: `http://localhost:5000`

## 🎯 Features

### Landing Page
- **Project Name**: Shore Guard Connect
- **Tagline**: Smart Coastal Protection & Mangrove Watch
- **Call-to-Actions**: 
  - Login / Register (for all roles)
  - Learn More (redirects to About page)
- **Hero Section**: Beautiful illustration with project branding
- **Features Grid**: Dynamic features from backend API

### User Roles
- **Authority**: Full access to all features
- **NGO**: Access to monitoring and reporting features
- **Community**: Basic reporting and viewing access

### Core Functionality
- **Authentication**: JWT-based login/register system
- **Coastal Monitoring**: Real-time alerts and threat detection
- **Mangrove Watch**: Conservation data and project management
- **Community Reports**: User-generated incident reports
- **Data Analytics**: Trend analysis and reporting

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Landing Page
- `GET /api/landing` - Get landing page information

### Coastal Monitoring
- `GET /api/coastal/alerts` - Get coastal alerts
- `POST /api/coastal/alerts` - Create new alert
- `PUT /api/coastal/alerts/:id` - Update alert
- `DELETE /api/coastal/alerts/:id` - Delete alert

### Reports
- `GET /api/coastal/reports` - Get community reports
- `POST /api/coastal/reports` - Create new report
- `PUT /api/coastal/reports/:id` - Update report
- `DELETE /api/coastal/reports/:id` - Delete report

### Mangrove Data
- `GET /api/mangrove/data` - Get mangrove monitoring data
- `POST /api/mangrove/data` - Create new mangrove data
- `PUT /api/mangrove/data/:id` - Update mangrove data
- `DELETE /api/mangrove/data/:id` - Delete mangrove data

### Conservation Projects
- `GET /api/mangrove/projects` - Get conservation projects
- `POST /api/mangrove/projects` - Create new project
- `PUT /api/mangrove/projects/:id` - Update project
- `DELETE /api/mangrove/projects/:id` - Delete project

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Different permissions for different user roles
- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: API rate limiting to prevent abuse
- **CORS Protection**: Cross-origin resource sharing configuration
- **Helmet Security**: Security headers middleware

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on all device sizes
- **Dark/Light Mode**: Theme support (future)
- **Loading States**: Smooth loading animations
- **Error Handling**: User-friendly error messages
- **Accessibility**: WCAG compliant components

## 🔄 Perfect Redirects

### Frontend Routes
- `/` → Landing page (Home)
- `/login` → Login page
- `/register` → Registration page
- `/about` → About page
- `/dashboard` → User dashboard (protected)
- `*` → 404 Not Found page

### Backend Redirects
- All API routes properly structured
- Authentication middleware for protected routes
- Role-based access control
- Proper error handling and status codes

## 🚀 Deployment

### Frontend Deployment
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Deployment
```bash
# Start production server
npm start
```

## 📝 Environment Variables

### Backend (.env)
```env
NODE_ENV=development
PORT=5000
JWT_SECRET=your-super-secret-jwt-key
FRONTEND_URL=http://localhost:8080
MONGODB_URI=mongodb://localhost:27017/shore-guard-connect
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please contact the development team.

---

**Built with ❤️ for coastal protection and mangrove conservation**
