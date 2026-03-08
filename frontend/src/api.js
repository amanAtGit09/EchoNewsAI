const BASE_URL = "https://aewms58hek.execute-api.us-east-1.amazonaws.com/Prod/news";

export const fetchNews = async (params = {}) => {
  // FIX: Force 'top' category if searching by keyword to avoid backend 404s
  if (params.q && !params.category) {
    params.category = 'top';
  }

  const query = new URLSearchParams(params).toString();
  const url = `${BASE_URL}?${query}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Network response was not ok");
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    return null;
  }
};