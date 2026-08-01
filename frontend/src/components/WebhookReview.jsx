import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertTriangle, CheckCircle2, XCircle, RefreshCw, Loader2, GitPullRequest, Rocket } from 'lucide-react';
import MarkdownRenderer from './MarkdownRenderer';

import API_BASE from '../config/api';

export default function WebhookReview({ onDecisionComplete }) {
  const [pending, setPending] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Feedback state
  const [feedback, setFeedback] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitText, setSubmitText] = useState('');

  const fetchPending = async () => {
    try {
      const res = await axios.get(`${API_BASE}/dashboard/pending`);
      setPending(res.data || []);
    } catch (err) {
      console.error("Error fetching pending webhooks:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPending();
    const interval = setInterval(fetchPending, 10000); // 10s polling
    return () => clearInterval(interval);
  }, []);

  const handleDecision = async (review, action) => {
    setSubmitting(true);
    if (action === 'approve') setSubmitText('Approving & Finalizing...');
    else if (action === 'reject') setSubmitText('Enhancing Review based on feedback...');
    else if (action === 'auto_fix') setSubmitText('Auto-remediating code & pushing to GitHub...');
    
    try {
      await axios.post(`${API_BASE}/review/${review.review_id}/decision`, {
        approved: action === 'approve', // Keep for backward compatibility in backend if needed
        feedback: feedback.trim(),
        action: action
      });
      
      setFeedback('');
      await fetchPending(); // Immediately fetch next
      if (onDecisionComplete) onDecisionComplete();
    } catch (err) {
      alert("Failed to submit decision. Ensure backend is running.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading && pending.length === 0) return null; // Don't show anything while initially loading
  
  // If no webhooks are pending, render nothing (or a subtle all-clear message if desired, but user wants clean dashboard)
  if (pending.length === 0) {
    return null; 
  }

  // We have at least one pending webhook request
  const currentReview = pending[0]; // Process oldest first

  return (
    <div className="mb-12 animate-in fade-in slide-in-from-top-4 duration-500">
      <div className="bg-[#0f0a18] border-2 border-purple-500/50 rounded-2xl overflow-hidden shadow-[0_0_40px_rgba(168,85,247,0.15)] relative">
        
        {/* Urgent Header */}
        <div className="bg-gradient-to-r from-purple-900/60 to-indigo-900/60 p-4 border-b border-purple-500/30 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-full bg-purple-500/20 text-purple-300 animate-pulse">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white uppercase tracking-wider flex items-center gap-2">
                Action Required: Webhook Request
              </h2>
              <p className="text-purple-300/80 text-sm font-medium flex items-center gap-2 mt-0.5">
                <GitPullRequest className="w-4 h-4" /> 
                {currentReview.repo_name} {currentReview.pr_number && `(PR #${currentReview.pr_number})`}
              </p>
            </div>
          </div>
          <div className="text-right">
            <span className="bg-purple-500/20 text-purple-300 py-1 px-3 rounded-full text-xs font-bold border border-purple-500/30">
              {pending.length} in queue
            </span>
          </div>
        </div>

        {submitting ? (
          <div className="flex flex-col items-center justify-center p-16">
            <Loader2 className="w-12 h-12 text-purple-400 animate-spin mb-4" />
            <p className="text-purple-300 font-bold tracking-widest uppercase text-sm animate-pulse">{submitText}</p>
          </div>
        ) : (
          <div>
            <div className="flex flex-col lg:flex-row divide-y lg:divide-y-0 lg:divide-x divide-purple-500/20">
              
              {/* Markdown Summary (Left Side) */}
              <div className="flex-1 p-6 lg:p-8 bg-black/40 overflow-y-auto max-h-[600px]">
                <MarkdownRenderer content={currentReview.summary || "*No summary available.*"} />
              </div>

              {/* Decision Controls (Right Side) */}
              <div className="w-full lg:w-[400px] p-6 lg:p-8 bg-black/60 flex flex-col shrink-0">
                <h3 className="text-white font-bold mb-6 text-lg">Review Decision</h3>
                
                <div className="flex-1">
                  <label className="block text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Enhancement Feedback</label>
                  <textarea 
                    rows="4"
                    placeholder="e.g. 'Ignore the eval() finding' or 'Make it more concise'"
                    className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500/50 transition-all resize-none mb-6"
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                  />
                </div>
                
                <div className="space-y-4 mt-auto">
                  <button 
                    onClick={() => handleDecision(currentReview, 'auto_fix')}
                    className="w-full py-4 rounded-xl bg-blue-500/20 text-blue-400 font-bold border border-blue-500/30 hover:bg-blue-500/30 hover:shadow-[0_0_15px_rgba(59,130,246,0.2)] transition-all flex items-center justify-center gap-2"
                  >
                    <Rocket className="w-5 h-5" />
                    Auto-Fix Issues
                  </button>
                  
                  <button 
                    onClick={() => handleDecision(currentReview, 'approve')}
                    className="w-full py-4 rounded-xl bg-green-500/20 text-green-400 font-bold border border-green-500/30 hover:bg-green-500/30 hover:shadow-[0_0_15px_rgba(34,197,94,0.2)] transition-all flex items-center justify-center gap-2"
                  >
                    <CheckCircle2 className="w-5 h-5" />
                    Approve & Finalize
                  </button>
                  
                  <button 
                    onClick={() => handleDecision(currentReview, 'reject')}
                    className="w-full py-4 rounded-xl bg-red-500/10 text-red-400 font-bold border border-red-500/20 hover:bg-red-500/20 hover:shadow-[0_0_15px_rgba(239,68,68,0.2)] transition-all flex items-center justify-center gap-2"
                  >
                    <RefreshCw className="w-5 h-5" />
                    Reject & Enhance AI
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
