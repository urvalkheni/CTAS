const API_BASE_URL = 'http://localhost:5000/api';

// API service class
class ApiService {
  private baseURL: string;
  private token: string | null;

  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('token');
  }

  // Set auth token
  setToken(token: string) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  // Clear auth token
  clearToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  // Get auth headers
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  // Generic request method
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const config: RequestInit = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth endpoints
  async register(userData: {
    name: string;
    email: string;
    password: string;
    role: 'authority' | 'ngo' | 'community';
  }) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: { email: string; password: string }) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async logout() {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  async getProfile() {
    return this.request('/auth/profile');
  }

  async updateProfile(profileData: { name?: string; email?: string }) {
    return this.request('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }

  // Landing page info
  async getLandingInfo() {
    return this.request('/landing');
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Coastal alerts
  async getAlerts(params?: { severity?: string; status?: string; location?: string }) {
    const queryString = params ? `?${new URLSearchParams(params).toString()}` : '';
    return this.request(`/coastal/alerts${queryString}`);
  }

  async createAlert(alertData: {
    title: string;
    description: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    location: string;
  }) {
    return this.request('/coastal/alerts', {
      method: 'POST',
      body: JSON.stringify(alertData),
    });
  }

  // Coastal reports
  async getReports(params?: { type?: string; status?: string; location?: string }) {
    const queryString = params ? `?${new URLSearchParams(params).toString()}` : '';
    return this.request(`/coastal/reports${queryString}`);
  }

  async createReport(reportData: {
    title: string;
    description: string;
    type: 'incident' | 'observation' | 'suggestion';
    location: string;
  }) {
    return this.request('/coastal/reports', {
      method: 'POST',
      body: JSON.stringify(reportData),
    });
  }

  // Mangrove data
  async getMangroveData(params?: { healthStatus?: string; location?: string }) {
    const queryString = params ? `?${new URLSearchParams(params).toString()}` : '';
    return this.request(`/mangrove/data${queryString}`);
  }

  async createMangroveData(data: {
    location: string;
    area: number;
    healthStatus: 'excellent' | 'good' | 'fair' | 'poor';
    notes?: string;
  }) {
    return this.request('/mangrove/data', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Conservation projects
  async getConservationProjects(params?: { status?: string; location?: string }) {
    const queryString = params ? `?${new URLSearchParams(params).toString()}` : '';
    return this.request(`/mangrove/projects${queryString}`);
  }

  async createConservationProject(projectData: {
    name: string;
    description: string;
    location: string;
    status?: 'planned' | 'active' | 'completed' | 'on-hold';
    startDate?: string;
    endDate?: string;
  }) {
    return this.request('/mangrove/projects', {
      method: 'POST',
      body: JSON.stringify(projectData),
    });
  }
}

// Create and export singleton instance
export const apiService = new ApiService();
export default apiService;
