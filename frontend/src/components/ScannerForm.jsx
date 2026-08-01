import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Search, GitPullRequest, Loader2, Play, CheckCircle2, XCircle, FileText, AlertCircle, RefreshCw, Rocket } from 'lucide-react';

import API_BASE from '../config/api';
const REVIEW_URL = `${API_BASE}/review`;

export default function ScannerWizard({ onScanComplete }) {
  const [tab, setTab] = useState('github'); // 'github' or 'pr'
  const [repoUrl, setRepoUrl] = useState('');
  const [prNumber, setPrNumber] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [loadingText, setLoadingText] = useState('Running AI Agents...');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  // Feedback for rejection
  const [feedback, setFeedback] = useState('');

  const resetForm = () => {
    setResult(null);
    setRepoUrl('');
    setPrNumber('');
    setFeedback('');
    if (onScanComplete) onScanComplete();
  };

  const handleScan = async (e) => {
    e.preventDefault();
    setLoading(true);
    setLoadingText('Analyzing Repository & Finding Vulnerabilities...');
    setError(null);
    setResult(null);
    
    try {
      const endpoint = tab === 'github' ? `${REVIEW_URL}/github` : `${REVIEW_URL}/pr`;
      const payload = tab === 'github' 
        ? { repo_url: repoUrl } 
        : { repo_url: repoUrl, pr_number: parseInt(prNumber, 10) };

      const res = await axios.post(endpoint, payload);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to trigger scan. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const handleDecision = async (approved) => {
    if (!result || !result.review_id) return;
    setLoading(true);
    setLoadingText(approved ? 'Approving & Finalizing...' : 'Enhancing Review based on feedback...');
    setError(null);

    try {
      const res = await axios.post(`${REVIEW_URL}/${result.review_id}/decision`, {
        approved: approved === true,
        feedback: feedback.trim(),
        action: typeof approved === 'string' ? approved : (approved ? 'approve' : 'reject')
      });
      setResult(res.data); // This might be WAITING_FOR_REVIEW again or COMPLETED
      setFeedback(''); // clear feedback after submit
      if (res.data.status === 'COMPLETED' && onScanComplete) {
        onScanComplete();
      }
    } catch (err) {
      setError("Failed to submit decision. Ensure backend is running.");
      setLoading(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 flex flex-col h-full max-h-[85vh]">
      <div className="flex items-center gap-3 mb-6 shrink-0">
        <div className="p-2 rounded-lg bg-blue-500/20 text-blue-400">
          <Play className="w-5 h-5" />
        </div>
        <h2 className="text-xl font-bold text-white">Security Scanner Wizard</h2>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center flex-1 py-12">
          <div className="relative w-20 h-20 mb-6">
            <div className="absolute inset-0 border-4 border-white/10 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-purple-500 rounded-full border-t-transparent animate-spin"></div>
          </div>
          <p className="text-purple-300 font-bold tracking-widest uppercase text-sm animate-pulse">{loadingText}</p>
        </div>
      ) : result && result.status === 'WAITING_FOR_REVIEW' ? (
        <div className="flex flex-col flex-1 overflow-hidden animate-in fade-in zoom-in duration-500">
          
          {/* Top Info Bar */}
          <div className="flex items-center justify-between bg-black/40 p-4 rounded-t-xl border border-white/10 shrink-0">
             <div>
                <h3 className="text-white font-bold text-lg flex items-center gap-2">
                  Reviewing: {repoUrl.split('/').pop()}
                  {tab === 'pr' && (
                    <span className="bg-blue-500/20 text-blue-300 text-xs px-2 py-0.5 rounded">PR #{prNumber}</span>
                  )}
                </h3>
             </div>
             <div className="flex items-center gap-4 text-sm">
                <span className="flex items-center gap-1 font-bold text-red-400"><AlertCircle className="w-4 h-4"/> Risk: {result.risk}</span>
                <span className="flex items-center gap-1 font-bold text-orange-400">Score: {result.score}/100</span>
             </div>
          </div>

          {/* Markdown Report Area */}
          <div className="flex-1 overflow-y-auto bg-black/20 p-6 border-l border-r border-white/10">
            <div className="prose prose-invert prose-purple max-w-none prose-sm lg:prose-base">
              <ReactMarkdown>{result.summary || "*No summary generated.*"}</ReactMarkdown>
            </div>
          </div>

          {/* Decision Area */}
          <div className="bg-black/60 p-4 rounded-b-xl border border-white/10 shrink-0 border-t-0">
             <label className="block text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Enhancement Feedback (Optional)</label>
             <textarea 
                rows="2"
                placeholder="e.g. 'Make this sound more urgent' or 'Ignore finding about XYZ'"
                className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-yellow-500/50 focus:ring-1 focus:ring-yellow-500/50 transition-all resize-none mb-3"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
              />
              
              <div className="flex gap-4">
                <button 
                  onClick={() => handleDecision('auto_fix')}
                  className="flex-1 py-3 rounded-lg bg-blue-500/20 text-blue-400 font-bold border border-blue-500/30 hover:bg-blue-500/30 hover:shadow-[0_0_15px_rgba(59,130,246,0.2)] transition-all flex items-center justify-center gap-2"
                >
                  <Rocket className="w-5 h-5" />
                  Auto-Fix
                </button>

                <button 
                  onClick={() => handleDecision(true)}
                  className="flex-1 py-3 rounded-lg bg-green-500/20 text-green-400 font-bold border border-green-500/30 hover:bg-green-500/30 hover:shadow-[0_0_15px_rgba(34,197,94,0.2)] transition-all flex items-center justify-center gap-2"
                >
                  <CheckCircle2 className="w-5 h-5" />
                  Approve
                </button>
                
                <button 
                  onClick={() => handleDecision(false)}
                  className="flex-1 py-3 rounded-lg bg-red-500/10 text-red-400 font-bold border border-red-500/20 hover:bg-red-500/20 hover:shadow-[0_0_15px_rgba(239,68,68,0.2)] transition-all flex items-center justify-center gap-2"
                >
                  <RefreshCw className="w-5 h-5" />
                  Reject & Enhance AI
                </button>
              </div>
          </div>
        </div>
      ) : result && result.status === 'COMPLETED' ? (
        <div className="flex flex-col items-center justify-center flex-1 py-12 animate-in fade-in slide-in-from-bottom-4">
           <div className="w-20 h-20 rounded-full bg-green-500/20 flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(34,197,94,0.3)]">
             <CheckCircle2 className="w-10 h-10 text-green-400" />
           </div>
           <h3 className="text-2xl font-bold text-white mb-2">Scan Complete!</h3>
           <p className="text-gray-400 mb-8 text-center max-w-sm">The AI review has been finalized, approved, and persisted to the database.</p>
           
           <button 
             onClick={resetForm}
             className="px-8 py-3 rounded-full bg-white/10 text-white font-bold hover:bg-white/20 transition-all"
           >
             Start New Scan
           </button>
        </div>
      ) : (
        <div className="flex flex-col flex-1 animate-in fade-in slide-in-from-left-4">
          <div className="flex bg-black/40 rounded-lg p-1 mb-6 border border-white/5 shrink-0">
            <button 
              type="button"
              onClick={() => setTab('github')}
              className={`flex-1 flex items-center justify-center gap-2 py-2 text-sm font-medium rounded-md transition-all ${tab === 'github' ? 'bg-purple-500/20 text-purple-300 shadow-[0_0_10px_rgba(168,85,247,0.2)]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}
            >
              <Search className="w-4 h-4" />
              Full Repository
            </button>
            <button 
              type="button"
              onClick={() => setTab('pr')}
              className={`flex-1 flex items-center justify-center gap-2 py-2 text-sm font-medium rounded-md transition-all ${tab === 'pr' ? 'bg-purple-500/20 text-purple-300 shadow-[0_0_10px_rgba(168,85,247,0.2)]' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}
            >
              <GitPullRequest className="w-4 h-4" />
              Pull Request
            </button>
          </div>

          <form onSubmit={handleScan} className="space-y-4 flex-1">
            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Repository URL</label>
              <input 
                type="url" 
                required
                placeholder="https://github.com/owner/repo"
                className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
              />
            </div>
            
            {tab === 'pr' && (
              <div className="animate-in fade-in slide-in-from-top-2 duration-300">
                <label className="block text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">PR Number</label>
                <input 
                  type="number" 
                  required
                  min="1"
                  placeholder="e.g. 3"
                  className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all"
                  value={prNumber}
                  onChange={(e) => setPrNumber(e.target.value)}
                />
              </div>
            )}

            <button 
              type="submit" 
              disabled={!repoUrl}
              className="w-full py-4 mt-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold hover:from-purple-500 hover:to-indigo-500 transition-all shadow-[0_0_20px_rgba(147,51,234,0.3)] hover:shadow-[0_0_25px_rgba(147,51,234,0.5)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg"
            >
              Deploy Security Agents
            </button>
          </form>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm shrink-0">
          {error}
        </div>
      )}

    </div>
  );
}
