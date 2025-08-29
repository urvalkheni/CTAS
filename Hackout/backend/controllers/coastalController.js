// Mock data for coastal alerts and reports
let alerts = [
  {
    id: '1',
    title: 'High Tide Alert',
    description: 'Unusually high tide detected in coastal area',
    severity: 'high',
    location: 'Mumbai Coast',
    createdBy: '1',
    createdAt: new Date(),
    status: 'active'
  }
];

let reports = [
  {
    id: '1',
    title: 'Coastal Erosion Report',
    description: 'Significant erosion observed in the northern beach area',
    type: 'incident',
    location: 'Goa Beach',
    createdBy: '1',
    createdAt: new Date(),
    status: 'pending'
  }
];

// Alert Controllers
export const getAlerts = (req, res) => {
  try {
    const { severity, status, location } = req.query;
    let filteredAlerts = [...alerts];

    // Apply filters
    if (severity) {
      filteredAlerts = filteredAlerts.filter(alert => alert.severity === severity);
    }
    if (status) {
      filteredAlerts = filteredAlerts.filter(alert => alert.status === status);
    }
    if (location) {
      filteredAlerts = filteredAlerts.filter(alert => 
        alert.location.toLowerCase().includes(location.toLowerCase())
      );
    }

    res.json({
      alerts: filteredAlerts,
      total: filteredAlerts.length
    });
  } catch (error) {
    console.error('Get alerts error:', error);
    res.status(500).json({ error: 'Failed to get alerts' });
  }
};

export const createAlert = (req, res) => {
  try {
    const { title, description, severity, location } = req.body;
    const createdBy = req.user.userId;

    const newAlert = {
      id: Date.now().toString(),
      title,
      description,
      severity,
      location,
      createdBy,
      createdAt: new Date(),
      status: 'active'
    };

    alerts.push(newAlert);

    res.status(201).json({
      message: 'Alert created successfully',
      alert: newAlert
    });
  } catch (error) {
    console.error('Create alert error:', error);
    res.status(500).json({ error: 'Failed to create alert' });
  }
};

export const updateAlert = (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, severity, status } = req.body;
    const currentUser = req.user;

    const alertIndex = alerts.findIndex(alert => alert.id === id);
    if (alertIndex === -1) {
      return res.status(404).json({ error: 'Alert not found' });
    }

    // Check permissions (only creator or authority can update)
    if (alerts[alertIndex].createdBy !== currentUser.userId && currentUser.role !== 'authority') {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    // Update alert
    if (title) alerts[alertIndex].title = title;
    if (description) alerts[alertIndex].description = description;
    if (severity) alerts[alertIndex].severity = severity;
    if (status) alerts[alertIndex].status = status;

    res.json({
      message: 'Alert updated successfully',
      alert: alerts[alertIndex]
    });
  } catch (error) {
    console.error('Update alert error:', error);
    res.status(500).json({ error: 'Failed to update alert' });
  }
};

export const deleteAlert = (req, res) => {
  try {
    const { id } = req.params;
    const alertIndex = alerts.findIndex(alert => alert.id === id);

    if (alertIndex === -1) {
      return res.status(404).json({ error: 'Alert not found' });
    }

    alerts.splice(alertIndex, 1);
    res.json({ message: 'Alert deleted successfully' });
  } catch (error) {
    console.error('Delete alert error:', error);
    res.status(500).json({ error: 'Failed to delete alert' });
  }
};

// Report Controllers
export const getReports = (req, res) => {
  try {
    const { type, status, location } = req.query;
    let filteredReports = [...reports];

    // Apply filters
    if (type) {
      filteredReports = filteredReports.filter(report => report.type === type);
    }
    if (status) {
      filteredReports = filteredReports.filter(report => report.status === status);
    }
    if (location) {
      filteredReports = filteredReports.filter(report => 
        report.location.toLowerCase().includes(location.toLowerCase())
      );
    }

    res.json({
      reports: filteredReports,
      total: filteredReports.length
    });
  } catch (error) {
    console.error('Get reports error:', error);
    res.status(500).json({ error: 'Failed to get reports' });
  }
};

export const createReport = (req, res) => {
  try {
    const { title, description, type, location } = req.body;
    const createdBy = req.user.userId;

    const newReport = {
      id: Date.now().toString(),
      title,
      description,
      type,
      location,
      createdBy,
      createdAt: new Date(),
      status: 'pending'
    };

    reports.push(newReport);

    res.status(201).json({
      message: 'Report created successfully',
      report: newReport
    });
  } catch (error) {
    console.error('Create report error:', error);
    res.status(500).json({ error: 'Failed to create report' });
  }
};

export const updateReport = (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, type, status } = req.body;
    const currentUser = req.user;

    const reportIndex = reports.findIndex(report => report.id === id);
    if (reportIndex === -1) {
      return res.status(404).json({ error: 'Report not found' });
    }

    // Check permissions (only creator or authority can update)
    if (reports[reportIndex].createdBy !== currentUser.userId && currentUser.role !== 'authority') {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    // Update report
    if (title) reports[reportIndex].title = title;
    if (description) reports[reportIndex].description = description;
    if (type) reports[reportIndex].type = type;
    if (status) reports[reportIndex].status = status;

    res.json({
      message: 'Report updated successfully',
      report: reports[reportIndex]
    });
  } catch (error) {
    console.error('Update report error:', error);
    res.status(500).json({ error: 'Failed to update report' });
  }
};

export const deleteReport = (req, res) => {
  try {
    const { id } = req.params;
    const currentUser = req.user;

    const reportIndex = reports.findIndex(report => report.id === id);
    if (reportIndex === -1) {
      return res.status(404).json({ error: 'Report not found' });
    }

    // Check permissions (only creator or authority can delete)
    if (reports[reportIndex].createdBy !== currentUser.userId && currentUser.role !== 'authority') {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    reports.splice(reportIndex, 1);
    res.json({ message: 'Report deleted successfully' });
  } catch (error) {
    console.error('Delete report error:', error);
    res.status(500).json({ error: 'Failed to delete report' });
  }
};
