export async function fetchResumes(search = "") {
  try {
    const url = search
      ? `http://localhost:5000/api/resumes?search=${encodeURIComponent(search)}`
      : "http://localhost:5000/api/resumes";

    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    return await response.json();
  } catch (err) {
    console.error("❌ Failed to fetch resumes:", err);
    return [];
  }
}
