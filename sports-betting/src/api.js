import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Adjust to your FastAPI backend URL
});

export const getProps = async () => {
  try {
    const response = await api.get('/props');
    return response.data;
  } catch (error) {
    console.error('Error fetching props:', error);
    throw error;
  }
};

export const getOdds = async () => {
  try {
    const response = await api.get('/odds');
    return response.data;
  } catch (error) {
    console.error('Error fetching odds:', error);
    throw error;
  }
};

export const getBaseballProps = async () => {
  try {
    const response = await api.get('/baseball');
    return response.data;
  } catch (error) {
    console.error('Error fetching baseball props:', error);
    throw error;
  }
};
