// Mock data for mangrove monitoring
let mangroveData = [
  {
    id: '1',
    location: 'Sundarbans',
    area: 10000.5,
    healthStatus: 'good',
    notes: 'Mangrove forest showing healthy growth',
    createdBy: '1',
    createdAt: new Date(),
    lastUpdated: new Date()
  }
];

let conservationProjects = [
  {
    id: '1',
    name: 'Sundarbans Restoration Project',
    description: 'Comprehensive mangrove restoration and conservation initiative',
    location: 'Sundarbans Delta',
    status: 'active',
    startDate: new Date('2024-01-01'),
    endDate: new Date('2026-12-31'),
    createdBy: '1',
    createdAt: new Date()
  }
];

// Mangrove Data Controllers
export const getMangroveData = (req, res) => {
  try {
    const { healthStatus, location } = req.query;
    let filteredData = [...mangroveData];

    // Apply filters
    if (healthStatus) {
      filteredData = filteredData.filter(data => data.healthStatus === healthStatus);
    }
    if (location) {
      filteredData = filteredData.filter(data => 
        data.location.toLowerCase().includes(location.toLowerCase())
      );
    }

    res.json({
      mangroveData: filteredData,
      total: filteredData.length
    });
  } catch (error) {
    console.error('Get mangrove data error:', error);
    res.status(500).json({ error: 'Failed to get mangrove data' });
  }
};

export const createMangroveData = (req, res) => {
  try {
    const { location, area, healthStatus, notes } = req.body;
    const createdBy = req.user.userId;

    const newData = {
      id: Date.now().toString(),
      location,
      area: parseFloat(area),
      healthStatus,
      notes: notes || '',
      createdBy,
      createdAt: new Date(),
      lastUpdated: new Date()
    };

    mangroveData.push(newData);

    res.status(201).json({
      message: 'Mangrove data created successfully',
      data: newData
    });
  } catch (error) {
    console.error('Create mangrove data error:', error);
    res.status(500).json({ error: 'Failed to create mangrove data' });
  }
};

export const updateMangroveData = (req, res) => {
  try {
    const { id } = req.params;
    const { location, area, healthStatus, notes } = req.body;
    const currentUser = req.user;

    const dataIndex = mangroveData.findIndex(data => data.id === id);
    if (dataIndex === -1) {
      return res.status(404).json({ error: 'Mangrove data not found' });
    }

    // Check permissions (only creator, NGO, or authority can update)
    if (mangroveData[dataIndex].createdBy !== currentUser.userId && 
        !['ngo', 'authority'].includes(currentUser.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    // Update data
    if (location) mangroveData[dataIndex].location = location;
    if (area) mangroveData[dataIndex].area = parseFloat(area);
    if (healthStatus) mangroveData[dataIndex].healthStatus = healthStatus;
    if (notes !== undefined) mangroveData[dataIndex].notes = notes;
    
    mangroveData[dataIndex].lastUpdated = new Date();

    res.json({
      message: 'Mangrove data updated successfully',
      data: mangroveData[dataIndex]
    });
  } catch (error) {
    console.error('Update mangrove data error:', error);
    res.status(500).json({ error: 'Failed to update mangrove data' });
  }
};

export const deleteMangroveData = (req, res) => {
  try {
    const { id } = req.params;
    const dataIndex = mangroveData.findIndex(data => data.id === id);

    if (dataIndex === -1) {
      return res.status(404).json({ error: 'Mangrove data not found' });
    }

    mangroveData.splice(dataIndex, 1);
    res.json({ message: 'Mangrove data deleted successfully' });
  } catch (error) {
    console.error('Delete mangrove data error:', error);
    res.status(500).json({ error: 'Failed to delete mangrove data' });
  }
};

// Conservation Project Controllers
export const getConservationProjects = (req, res) => {
  try {
    const { status, location } = req.query;
    let filteredProjects = [...conservationProjects];

    // Apply filters
    if (status) {
      filteredProjects = filteredProjects.filter(project => project.status === status);
    }
    if (location) {
      filteredProjects = filteredProjects.filter(project => 
        project.location.toLowerCase().includes(location.toLowerCase())
      );
    }

    res.json({
      projects: filteredProjects,
      total: filteredProjects.length
    });
  } catch (error) {
    console.error('Get conservation projects error:', error);
    res.status(500).json({ error: 'Failed to get conservation projects' });
  }
};

export const createConservationProject = (req, res) => {
  try {
    const { name, description, location, status, startDate, endDate } = req.body;
    const createdBy = req.user.userId;

    const newProject = {
      id: Date.now().toString(),
      name,
      description,
      location,
      status: status || 'planned',
      startDate: startDate ? new Date(startDate) : null,
      endDate: endDate ? new Date(endDate) : null,
      createdBy,
      createdAt: new Date()
    };

    conservationProjects.push(newProject);

    res.status(201).json({
      message: 'Conservation project created successfully',
      project: newProject
    });
  } catch (error) {
    console.error('Create conservation project error:', error);
    res.status(500).json({ error: 'Failed to create conservation project' });
  }
};

export const updateConservationProject = (req, res) => {
  try {
    const { id } = req.params;
    const { name, description, location, status, startDate, endDate } = req.body;
    const currentUser = req.user;

    const projectIndex = conservationProjects.findIndex(project => project.id === id);
    if (projectIndex === -1) {
      return res.status(404).json({ error: 'Conservation project not found' });
    }

    // Check permissions (only creator, NGO, or authority can update)
    if (conservationProjects[projectIndex].createdBy !== currentUser.userId && 
        !['ngo', 'authority'].includes(currentUser.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    // Update project
    if (name) conservationProjects[projectIndex].name = name;
    if (description) conservationProjects[projectIndex].description = description;
    if (location) conservationProjects[projectIndex].location = location;
    if (status) conservationProjects[projectIndex].status = status;
    if (startDate) conservationProjects[projectIndex].startDate = new Date(startDate);
    if (endDate) conservationProjects[projectIndex].endDate = new Date(endDate);

    res.json({
      message: 'Conservation project updated successfully',
      project: conservationProjects[projectIndex]
    });
  } catch (error) {
    console.error('Update conservation project error:', error);
    res.status(500).json({ error: 'Failed to update conservation project' });
  }
};

export const deleteConservationProject = (req, res) => {
  try {
    const { id } = req.params;
    const projectIndex = conservationProjects.findIndex(project => project.id === id);

    if (projectIndex === -1) {
      return res.status(404).json({ error: 'Conservation project not found' });
    }

    conservationProjects.splice(projectIndex, 1);
    res.json({ message: 'Conservation project deleted successfully' });
  } catch (error) {
    console.error('Delete conservation project error:', error);
    res.status(500).json({ error: 'Failed to delete conservation project' });
  }
};
