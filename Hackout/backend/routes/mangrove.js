import express from 'express';
import { body } from 'express-validator';
import { 
  getMangroveData, 
  createMangroveData, 
  updateMangroveData, 
  deleteMangroveData,
  getConservationProjects,
  createConservationProject,
  updateConservationProject,
  deleteConservationProject
} from '../controllers/mangroveController.js';
import { validateRequest } from '../middleware/validation.js';
import { authenticateToken, requireRole } from '../middleware/auth.js';

const router = express.Router();

// All routes require authentication
router.use(authenticateToken);

// Mangrove data routes
router.get('/data', getMangroveData);
router.post('/data', [
  body('location').notEmpty().withMessage('Location is required'),
  body('area').isFloat({ min: 0 }).withMessage('Valid area is required'),
  body('healthStatus').isIn(['excellent', 'good', 'fair', 'poor']).withMessage('Valid health status is required'),
  body('notes').optional().trim(),
  validateRequest
], createMangroveData);

router.put('/data/:id', [
  body('location').optional().notEmpty().withMessage('Location cannot be empty'),
  body('area').optional().isFloat({ min: 0 }).withMessage('Valid area is required'),
  body('healthStatus').optional().isIn(['excellent', 'good', 'fair', 'poor']).withMessage('Valid health status is required'),
  validateRequest
], updateMangroveData);

router.delete('/data/:id', requireRole(['authority', 'ngo']), deleteMangroveData);

// Conservation project routes
router.get('/projects', getConservationProjects);
router.post('/projects', [
  body('name').trim().isLength({ min: 5 }).withMessage('Project name must be at least 5 characters'),
  body('description').trim().isLength({ min: 10 }).withMessage('Description must be at least 10 characters'),
  body('location').notEmpty().withMessage('Location is required'),
  body('status').isIn(['planned', 'active', 'completed', 'on-hold']).withMessage('Valid status is required'),
  validateRequest
], createConservationProject);

router.put('/projects/:id', [
  body('name').optional().trim().isLength({ min: 5 }).withMessage('Project name must be at least 5 characters'),
  body('description').optional().trim().isLength({ min: 10 }).withMessage('Description must be at least 10 characters'),
  body('status').optional().isIn(['planned', 'active', 'completed', 'on-hold']).withMessage('Valid status is required'),
  validateRequest
], updateConservationProject);

router.delete('/projects/:id', requireRole(['authority', 'ngo']), deleteConservationProject);

export default router;
