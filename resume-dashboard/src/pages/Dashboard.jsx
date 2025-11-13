import React, { useEffect, useState } from "react";
import { fetchResumes } from "../api/resumes";
import ResumesTable from "../components/ResumesTable";
import SearchBar from "../components/SearchBar";
import Notification from "../components/Notification";

export default function Dashboard() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchSkill, setSearchSkill] = useState("");
  const [careerSpan, setCareerSpan] = useState("");
  const [name, setName] = useState("");
  const [newResumeIds, setNewResumeIds] = useState([]);
  const [notification, setNotification] = useState("");
  const [lastRefresh, setLastRefresh] = useState(new Date());
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    loadResumes();

    // EventSource for real-time updates
    const eventSource = new EventSource("http://localhost:5000/api/events");
    eventSource.onmessage = (event) => {
      const newId = parseInt(event.data, 10);
      setNewResumeIds((prev) => [...prev, newId]);
      setNotification("🆕 A new resume has arrived!");
      loadResumes();
      setTimeout(() => setNotification(""), 4000);
    };

    // Auto-refresh every 2 minutes
    const refreshInterval = setInterval(() => {
      setIsRefreshing(true);
      loadResumes();
      setLastRefresh(new Date());
      setTimeout(() => setIsRefreshing(false), 1000);
    }, 120000); // 2 minutes = 120000ms

    return () => {
      eventSource.close();
      clearInterval(refreshInterval);
    };
  }, []);

  const loadResumes = async () => {
    setLoading(true);
    try {
      const data = await fetchResumes();
      setResumes(data || []);
    } catch (error) {
      console.error("Error loading resumes:", error);
      setNotification("❌ Error loading resumes. Please try again.");
      setTimeout(() => setNotification(""), 4000);
    } finally {
      setLoading(false);
    }
  };

  const handleManualRefresh = () => {
    setIsRefreshing(true);
    loadResumes();
    setLastRefresh(new Date());
    setNotification("🔄 Refreshed successfully!");
    setTimeout(() => {
      setNotification("");
      setIsRefreshing(false);
    }, 2000);
  };

  const clearAllFilters = () => {
    setName("");
    setSearchSkill("");
    setCareerSpan("");
  };

  const filteredResumes = resumes.filter((resume) => {
    const matchesName = name
      ? resume.name?.toLowerCase().includes(name.toLowerCase())
      : true;
    const matchesSkill = searchSkill
      ? resume.skills?.some((s) =>
          s.toLowerCase().includes(searchSkill.toLowerCase())
        )
      : true;
    const matchesCareerSpan = careerSpan
      ? String(resume.career_span)
          .toLowerCase()
          .includes(careerSpan.toLowerCase())
      : true;
    return matchesName && matchesSkill && matchesCareerSpan;
  });

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const hasActiveFilters = name || searchSkill || careerSpan;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-blue-50 to-cyan-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Animated Header */}
        <header className="mb-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 mb-4">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-3 rounded-xl shadow-lg">
                <span className="text-2xl">📄</span>
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-900 to-indigo-900 bg-clip-text text-transparent">
                  Resume Dashboard
                </h1>
                <p className="text-gray-600 mt-1">Manage and explore candidate profiles</p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-500 bg-white px-3 py-1 rounded-full shadow">
                Last updated: {formatTime(lastRefresh)}
              </div>
              <button
                onClick={handleManualRefresh}
                disabled={loading || isRefreshing}
                className="flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white px-4 py-2 rounded-lg shadow-lg transition-all duration-200 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span className={`${isRefreshing ? 'animate-spin' : ''}`}>🔄</span>
                {isRefreshing ? 'Refreshing...' : 'Refresh'}
              </button>
            </div>
          </div>
          <Notification message={notification} />
        </header>

        {/* Enhanced Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-6 rounded-xl text-white shadow-lg transform hover:scale-105 transition-all duration-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100">Total Resumes</p>
                <p className="text-3xl font-bold">{resumes.length}</p>
              </div>
              <div className="text-4xl opacity-80">📊</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 p-6 rounded-xl text-white shadow-lg transform hover:scale-105 transition-all duration-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100">Filtered Results</p>
                <p className="text-3xl font-bold">{filteredResumes.length}</p>
              </div>
              <div className="text-4xl opacity-80">🎯</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 p-6 rounded-xl text-white shadow-lg transform hover:scale-105 transition-all duration-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100">New Today</p>
                <p className="text-3xl font-bold">{newResumeIds.length}</p>
              </div>
              <div className="text-4xl opacity-80">✨</div>
            </div>
          </div>
        </div>

        {/* Enhanced Filters */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-8 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
              🔍 Search & Filter
            </h2>
            {hasActiveFilters && (
              <button
                onClick={clearAllFilters}
                className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-600 px-3 py-1 rounded-lg transition-colors duration-200"
              >
                Clear All Filters
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Name</label>
              <SearchBar
                value={name}
                onChange={setName}
                placeholder="Search by candidate name..."
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Skills</label>
              <SearchBar
                value={searchSkill}
                onChange={setSearchSkill}
                placeholder="Search by skills..."
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Experience</label>
              <SearchBar
                value={careerSpan}
                onChange={setCareerSpan}
                placeholder="Filter by years of experience..."
              />
            </div>
          </div>

          {hasActiveFilters && (
            <div className="mt-4 flex items-center gap-2 text-sm text-blue-600">
              <span>🏷️</span>
              <span>Active filters applied</span>
            </div>
          )}
        </div>

        {/* Enhanced Table Container */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
                📋 Resume List
                <span className="text-sm font-normal text-gray-500">
                  ({filteredResumes.length} results)
                </span>
              </h2>

              {loading && (
                <div className="flex items-center gap-2 text-blue-600">
                  <div className="animate-spin w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full"></div>
                  <span className="text-sm">Loading...</span>
                </div>
              )}
            </div>
          </div>

          <div className="p-6">
            {loading ? (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mb-4"></div>
                <p className="text-gray-500 text-lg">Loading resumes...</p>
                <p className="text-gray-400 text-sm mt-1">Please wait while we fetch the latest data</p>
              </div>
            ) : filteredResumes.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="text-6xl mb-4">🔍</div>
                <p className="text-gray-500 text-lg mb-2">No resumes found</p>
                <p className="text-gray-400 text-sm">Try adjusting your search filters</p>
                {hasActiveFilters && (
                  <button
                    onClick={clearAllFilters}
                    className="mt-4 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
                  >
                    Clear Filters
                  </button>
                )}
              </div>
            ) : (
              <ResumesTable resumes={filteredResumes} newResumeIds={newResumeIds} />
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-8 text-center text-gray-500 text-sm">
          <p>Dashboard auto-refreshes every 2 minutes • Last refresh: {formatTime(lastRefresh)}</p>
        </footer>
      </div>
    </div>
  );
}