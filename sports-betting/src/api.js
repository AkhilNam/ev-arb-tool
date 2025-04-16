import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const fetchOdds = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/api/odds`);
    return response.data;
  } catch (error) {
    console.error('Error fetching odds:', error);
    throw error;
  }
};

export const fetchBaseballOdds = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/api/baseball`);
    return response.data;
  } catch (error) {
    console.error('Error fetching baseball odds:', error);
    throw error;
  }
};

export const fetchNcaabOdds = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/api/ncaab`);
    return response.data;
  } catch (error) {
    console.error('Error fetching NCAAB odds:', error);
    throw error;
  }
};

export const fetchDfsData = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/api/dfs`);
    return response.data || [];
  } catch (error) {
    console.error('Error fetching DFS data:', error);
    return [];
  }
};
