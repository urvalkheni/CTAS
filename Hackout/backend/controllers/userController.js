// Mock user database (import from authController)
let users = [
  {
    id: '1',
    name: 'Admin User',
    email: 'admin@shoreguard.com',
    password: '$2a$10$example.hash',
    role: 'authority',
    createdAt: new Date()
  }
];

// Get all users (admin only)
export const getAllUsers = (req, res) => {
  try {
    const usersWithoutPasswords = users.map(user => {
      const { password: _, ...userWithoutPassword } = user;
      return userWithoutPassword;
    });

    res.json({
      users: usersWithoutPasswords,
      total: usersWithoutPasswords.length
    });
  } catch (error) {
    console.error('Get all users error:', error);
    res.status(500).json({ error: 'Failed to get users' });
  }
};

// Get user by ID
export const getUserById = (req, res) => {
  try {
    const { id } = req.params;
    const user = users.find(user => user.id === id);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const { password: _, ...userWithoutPassword } = user;
    res.json({ user: userWithoutPassword });
  } catch (error) {
    console.error('Get user by ID error:', error);
    res.status(500).json({ error: 'Failed to get user' });
  }
};

// Update user
export const updateUser = (req, res) => {
  try {
    const { id } = req.params;
    const { name, email, role } = req.body;
    const currentUser = req.user;

    const userIndex = users.findIndex(user => user.id === id);
    if (userIndex === -1) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Check permissions
    if (currentUser.role !== 'authority' && currentUser.userId !== id) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    // Check if email is already taken by another user
    if (email && email !== users[userIndex].email) {
      const existingUser = users.find(user => user.email === email);
      if (existingUser) {
        return res.status(400).json({ error: 'Email already in use' });
      }
    }

    // Update user
    if (name) users[userIndex].name = name;
    if (email) users[userIndex].email = email;
    if (role && currentUser.role === 'authority') users[userIndex].role = role;

    const { password: _, ...userWithoutPassword } = users[userIndex];
    res.json({
      message: 'User updated successfully',
      user: userWithoutPassword
    });
  } catch (error) {
    console.error('Update user error:', error);
    res.status(500).json({ error: 'Failed to update user' });
  }
};

// Delete user (admin only)
export const deleteUser = (req, res) => {
  try {
    const { id } = req.params;
    const userIndex = users.findIndex(user => user.id === id);

    if (userIndex === -1) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Prevent admin from deleting themselves
    if (req.user.userId === id) {
      return res.status(400).json({ error: 'Cannot delete your own account' });
    }

    users.splice(userIndex, 1);
    res.json({ message: 'User deleted successfully' });
  } catch (error) {
    console.error('Delete user error:', error);
    res.status(500).json({ error: 'Failed to delete user' });
  }
};
