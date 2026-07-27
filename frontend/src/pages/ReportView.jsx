import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, FileText, AlertTriangle, BarChart3, PieChart as PieChartIcon } from 'lucide-react';
import ChatBot from '../components/ChatBot';
import MarkdownRenderer from '../components/MarkdownRenderer';
import { 
  PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer, 
  BarChart, Bar, XAxis, YAxis, CartesianGrid 
} from 'recharts';

const API_BASE = 'http://localhost:8000';

export default function ReportView() {
  const { id } = useParams();
  const [content, setContent] = useState('');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await axios.get(`${API_BASE}/dashboard/report/${id}`);
        setContent(res.data.content);
        if (res.data.stats && Object.keys(res.data.stats).length > 0) {
          setStats(res.data.stats);
        }
      } catch (err) {
        console.error("Error fetching report:", err);
        setError("Report not found or failed to load.");
      } finally {
        setLoading(false);
      }
    };
    
    if (id) {
      fetchReport();
    }
  }, [id]);

  return (
    <div className="min-h-screen bg-[#050505] selection:bg-purple-500/30 selection:text-purple-200 p-6 lg:p-12">
      
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/10 blur-[120px]"></div>
      </div>

      <div className="max-w-5xl mx-auto relative z-10">
        {/* Navigation Header */}
        <div className="mb-8 flex items-center justify-between">
          <Link 
            to="/" 
            className="flex items-center gap-2 text-gray-400 hover:text-white bg-white/5 hover:bg-white/10 px-4 py-2 rounded-lg transition-all"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </Link>
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-purple-500/20 border border-purple-500/30">
              <FileText className="w-5 h-5 text-purple-400" />
            </div>
            <span className="text-gray-300 font-mono text-sm">{id}</span>
          </div>
        </div>

        {/* Content Area */}
        <div className="glass-panel p-8 lg:p-12">
          {loading ? (
             <div className="flex flex-col items-center justify-center py-24">
                <div className="w-16 h-16 border-4 border-white/10 border-t-purple-500 rounded-full animate-spin mb-4"></div>
                <p className="text-gray-400">Loading full report...</p>
             </div>
          ) : error ? (
             <div className="flex flex-col items-center justify-center py-24 text-center">
                <AlertTriangle className="w-16 h-16 text-red-500/80 mb-4" />
                <h2 className="text-2xl font-bold text-white mb-2">Report Unavailable</h2>
                <p className="text-red-400/80 max-w-md">{error}</p>
                <p className="text-gray-500 mt-4 text-sm">Note: Older scans might not have a saved review_id linked to a markdown file.</p>
             </div>
          ) : (
            <>
              {stats && (
                <div className="mb-12">
                  <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                    <BarChart3 className="w-5 h-5 text-purple-400" />
                    Interactive Analytics
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    {/* Severity Donut Chart */}
                    <div className="bg-black/30 border border-white/5 rounded-2xl p-6">
                      <h4 className="text-gray-400 text-sm font-semibold uppercase tracking-widest mb-4 flex items-center gap-2">
                        <PieChartIcon className="w-4 h-4" />
                        Severity Distribution
                      </h4>
                      <div className="h-[250px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={[
                                { name: 'Critical', value: stats.critical, color: '#ef4444' },
                                { name: 'High', value: stats.high, color: '#f97316' },
                                { name: 'Medium', value: stats.medium, color: '#eab308' },
                                { name: 'Low', value: stats.low, color: '#22c55e' }
                              ].filter(d => d.value > 0)}
                              cx="50%"
                              cy="50%"
                              innerRadius={60}
                              outerRadius={80}
                              paddingAngle={5}
                              dataKey="value"
                            >
                              {
                                [
                                  { name: 'Critical', value: stats.critical, color: '#ef4444' },
                                  { name: 'High', value: stats.high, color: '#f97316' },
                                  { name: 'Medium', value: stats.medium, color: '#eab308' },
                                  { name: 'Low', value: stats.low, color: '#22c55e' }
                                ].filter(d => d.value > 0).map((entry, index) => (
                                  <Cell key={`cell-${index}`} fill={entry.color} />
                                ))
                              }
                            </Pie>
                            <RechartsTooltip 
                              contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
                              itemStyle={{ color: '#fff' }}
                            />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    {/* Scanner Breakdown Bar Chart */}
                    <div className="bg-black/30 border border-white/5 rounded-2xl p-6">
                      <h4 className="text-gray-400 text-sm font-semibold uppercase tracking-widest mb-4 flex items-center gap-2">
                        <BarChart3 className="w-4 h-4" />
                        Scanner Breakdown
                      </h4>
                      <div className="h-[250px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={
                            Object.entries(stats.findings_per_scanner || {}).map(([name, value]) => ({ name, value }))
                          }>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                            <XAxis dataKey="name" stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
                            <YAxis stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} allowDecimals={false} />
                            <RechartsTooltip 
                              contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
                              cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                            />
                            <Bar dataKey="value" fill="#a855f7" radius={[4, 4, 0, 0]} />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                  </div>
                  
                  <div className="my-10 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
                </div>
              )}

              <MarkdownRenderer content={content} />
            </>
          )}
        </div>
      </div>
      
      {/* ChatBot floating on top of ReportView */}
      {id && !loading && !error && (
        <ChatBot reviewId={id} />
      )}
    </div>
  );
}
