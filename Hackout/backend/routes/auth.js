import express from 'express';
import { body } from 'express-validator';
import { register, login, logout, getProfile, updateProfile } from '../controllers/authController.js';
import { validateRequest } from '../middleware/validation.js';
import { authenticateToken } from '../middleware/auth.js';

const router = express.Router();

// Register route
router.post('/register', [
  body('name').trim().isLength({ min: 2 }).withMessage('Name must be at least 2 characters'),
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  body('role').isIn(['authority', 'ngo', 'community']).withMessage('Valid role is required'),
  validateRequest
], register);

// Login route
router.post('/login', [
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('password').notEmpty().withMessage('Password is required'),
  validateRequest
], login);

// Logout route
router.post('/logout', logout);

// Get user profile (protected)
router.get('/profile', authenticateToken, getProfile);

// Update user profile (protected)
router.put('/profile', [
  authenticateToken,
  body('name').optional().trim().isLength({ min: 2 }).withMessage('Name must be at least 2 characters'),
  body('email').optional().isEmail().normalizeEmail().withMessage('Valid email is required'),
  validateRequest
], updateProfile);

export default router;
