import axios from 'axios';

const BASE_URL = 'http://localhost:8000/rbac-data';

export const fetchRolesData = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/roles`);
    return response.data.rbac_data;
  } catch (error) {
    console.error('Error fetching roles:', error);
    throw error;
  }
};

export const fetchResourcesData = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/resources`);
    return response.data.rbac_data;
  } catch (error) {
    console.error('Error fetching resources:', error);
    throw error;
  }
};
