import express from 'express';
import { body } from 'express-validator';
import { 
  getAlerts, 
  createAlert, 
  updateAlert, 
  deleteAlert,
  getReports,
  createReport,
  updateReport,
  deleteReport
} from '../controllers/coastalController.js';
import { validateRequest } from '../middleware/validation.js';
import { authenticateToken, requireRole } from '../middleware/auth.js';

const router = express.Router();

// All routes require authentication
router.use(authenticateToken);

// Alert routes
router.get('/alerts', getAlerts);
router.post('/alerts', [
  body('title').trim().isLength({ min: 5 }).withMessage('Title must be at least 5 characters'),
  body('description').trim().isLength({ min: 10 }).withMessage('Description must be at least 10 characters'),
  body('severity').isIn(['low', 'medium', 'high', 'critical']).withMessage('Valid severity is required'),
  body('location').notEmpty().withMessage('Location is required'),
  validateRequest
], createAlert);

router.put('/alerts/:id', [
  body('title').optional().trim().isLength({ min: 5 }).withMessage('Title must be at least 5 characters'),
  body('description').optional().trim().isLength({ min: 10 }).withMessage('Description must be at least 10 characters'),
  body('severity').optional().isIn(['low', 'medium', 'high', 'critical']).withMessage('Valid severity is required'),
  validateRequest
], updateAlert);

router.delete('/alerts/:id', requireRole(['authority']), deleteAlert);

// Report routes
router.get('/reports', getReports);
router.post('/reports', [
  body('title').trim().isLength({ min: 5 }).withMessage('Title must be at least 5 characters'),
  body('description').trim().isLength({ min: 10 }).withMessage('Description must be at least 10 characters'),
  body('type').isIn(['incident', 'observation', 'suggestion']).withMessage('Valid report type is required'),
  body('location').notEmpty().withMessage('Location is required'),
  validateRequest
], createReport);

router.put('/reports/:id', [
  body('title').optional().trim().isLength({ min: 5 }).withMessage('Title must be at least 5 characters'),
  body('description').optional().trim().isLength({ min: 10 }).withMessage('Description must be at least 10 characters'),
  body('type').optional().isIn(['incident', 'observation', 'suggestion']).withMessage('Valid report type is required'),
  validateRequest
], updateReport);

router.delete('/reports/:id', deleteReport);

export default router;
