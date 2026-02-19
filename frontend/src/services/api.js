import axios from 'axios'

// Base URL for all API requests
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message =
      error.response?.data?.message ||
      error.response?.data?.error ||
      error.message ||
      'An unexpected error occurred'
    
    console.error('API Error:', message)
    return Promise.reject(new Error(message))
  }
)

/**
 * Upload resume file for analysis
 * @param {FormData} formData - Form data containing the resume file
 * @returns {Promise} - Parsed resume data
 */
export const uploadResume = async (formData) => {
  return apiClient.post('/upload-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

/**
 * Start the interview process
 * @param {Object} data - Interview configuration data
 * @returns {Promise} - Interview session data with first question
 */
export const startInterview = async (data) => {
  return apiClient.post('/start-interview', data)
}

/**
 * Submit answer to a technical interview question
 * @param {Object} data - Answer data including question and response
 * @returns {Promise} - Next question or completion status
 */
export const submitAnswer = async (data) => {
  return apiClient.post('/submit-answer', data)
}

/**
 * Submit answer to an HR interview question
 * @param {Object} data - HR answer data
 * @returns {Promise} - Next HR question or completion status
 */
export const submitHRAnswer = async (data) => {
  return apiClient.post('/submit-hr-answer', data)
}

/**
 * Get the final interview report
 * @returns {Promise} - Complete interview report with scores and feedback
 */
export const getReport = async () => {
  return apiClient.get('/report')
}

// Export the axios instance for custom requests
export default apiClient
