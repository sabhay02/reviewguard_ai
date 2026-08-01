import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShieldCheck, Activity, AlertTriangle, Bug, Code2, TerminalSquare, Zap } from 'lucide-react';
import StatCard from '../components/StatCard';
import ReviewsTable from '../components/ReviewsTable';
import WebhookReview from '../components/WebhookReview';
import { Link } from 'react-router-dom';

import API_BASE from '../config/api';
const DASHBOARD_URL = `${API_BASE}/dashboard`;

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const [statsRes, reviewsRes] = await Promise.all([
        axios.get(`${DASHBOARD_URL}/stats`),
        axios.get(`${DASHBOARD_URL}/reviews`),
      ]);
      setStats(statsRes.data);
      setReviews(reviewsRes.data);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
      setError("Failed to connect to ReviewGuard AI backend. Ensure FastAPI is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-[#050505] selection:bg-purple-500/30 selection:text-purple-200">
      
      {/* Abstract Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/20 blur-[120px]"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-blue-900/10 blur-[120px]"></div>
      </div>

      {/* Top Navbar */}
      <nav className="border-b border-white/[0.08] bg-black/40 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-[0_0_20px_rgba(139,92,246,0.3)]">
                <ShieldCheck className="text-white w-6 h-6" />
              </div>
              <span className="text-2xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 via-purple-300 to-purple-400 drop-shadow-[0_0_15px_rgba(168,85,247,0.4)]">
                ReviewGuard <span className="font-light text-purple-200">AI</span>
              </span>
            </div>
            
            <div className="flex items-center gap-6">
              <Link to="/scan" className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 text-white text-sm font-bold transition-all shadow-[0_0_15px_rgba(147,51,234,0.3)] hover:shadow-[0_0_25px_rgba(147,51,234,0.5)]">
                Start Manual Scan
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-[1400px] mx-auto px-6 lg:px-8 py-10 relative z-10">
        
        {/* Header Section */}
        <div className="flex items-end justify-between mb-12">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-bold tracking-widest uppercase mb-4 shadow-[0_0_15px_rgba(168,85,247,0.15)]">
              <Zap className="w-3 h-3 text-purple-400" />
              System Online
            </div>
            <h1 className="text-4xl md:text-5xl font-black text-white mb-3 tracking-tight">Mission Control</h1>
            <p className="text-lg text-gray-400 max-w-2xl font-light leading-relaxed">
              Real-time monitoring of your multi-agent DevSecOps pipeline. Track security vulnerabilities, code quality, and AI reviews across all repositories.
            </p>
          </div>
        </div>

        {error ? (
          <div className="bg-red-950/30 border border-red-500/30 rounded-2xl p-8 text-center text-red-400 shadow-[0_0_30px_rgba(220,38,38,0.15)]">
            <AlertTriangle className="w-16 h-16 mx-auto mb-4 text-red-500/80" />
            <h3 className="text-xl font-bold mb-2">System Disconnected</h3>
            <p className="text-red-400/80 max-w-lg mx-auto">{error}</p>
          </div>
        ) : loading ? (
          <div className="flex flex-col items-center justify-center h-[400px]">
            <div className="relative w-20 h-20">
              <div className="absolute inset-0 border-4 border-white/10 rounded-full"></div>
              <div className="absolute inset-0 border-4 border-purple-500 rounded-full border-t-transparent animate-spin"></div>
            </div>
            <p className="mt-6 text-purple-300 font-medium tracking-widest uppercase text-sm animate-pulse">Initializing Data Stream...</p>
          </div>
        ) : (
          <div className="animate-in fade-in slide-in-from-bottom-8 duration-700 ease-out fill-mode-both">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
              <StatCard 
                title="Total Reviews" 
                value={stats.total_reviews} 
                icon={Activity}
                colorClass="bg-blue-500" 
              />
              <StatCard 
                title="Avg Security Score" 
                value={`${stats.average_score}`} 
                icon={ShieldCheck}
                colorClass="bg-purple-500" 
              />
              <StatCard 
                title="Total Findings" 
                value={stats.total_findings} 
                icon={Bug}
                colorClass="bg-orange-500" 
              />
              <StatCard 
                title="Critical Risks" 
                value={stats.critical_risk_count} 
                icon={AlertTriangle}
                colorClass="bg-red-500" 
              />
            </div>

            {/* Webhook Reviewer (Only visible if pending items exist) */}
            <WebhookReview onDecisionComplete={() => fetchData()} />

            {/* Scan History (Full Width) */}
            <div className="w-full">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center">
                  Scan History
                </h2>
              </div>
              <ReviewsTable reviews={reviews} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Dashboard;
