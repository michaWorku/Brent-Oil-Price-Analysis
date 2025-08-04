// Simulates an API call to a backend that performs the data analysis.
export const fetchAnalysisData = async () => {
  try {
    // The URL  points to the comprehensive API endpoint.
    const response = await fetch('http://localhost:5000/api/all_data');
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};
