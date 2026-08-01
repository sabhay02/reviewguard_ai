import React, { useState } from 'react';
import axios from 'axios';
import { CheckCircle2, XCircle, UserCheck } from 'lucide-react';

import API_BASE from '../config/api';
const REVIEW_URL = `${API_BASE}/review`;

export default function DecisionForm({ onDecisionComplete }) {
  const [reviewId, setReviewId] = useState('');
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleDecision = async (approved) => {
    if (!reviewId.trim()) {
      setError("Please enter a Review ID.");
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await axios.post(`${REVIEW_URL}/${reviewId.trim()}/decision`, {
        approved: approved === true,
        feedback: feedback.trim(),
        action: typeof approved === 'string' ? approved : (approved ? 'approve' : 'reject')
      });
      
      setSuccess(`Review decision submitted successfully!`);
      setReviewId('');
      setFeedback('');
      
      if (onDecisionComplete) onDecisionComplete();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to submit decision. Ensure the ID is valid and the review is paused.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-6 mt-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-green-500/20 text-green-400">
          <UserCheck className="w-5 h-5" />
        </div>
        <h2 className="text-xl font-bold text-white">Human Approval</h2>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Review ID</label>
          <input 
            type="text" 
            placeholder="Paste ID from scanner..."
            className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-green-500/50 focus:ring-1 focus:ring-green-500/50 transition-all font-mono text-sm"
            value={reviewId}
            onChange={(e) => setReviewId(e.target.value)}
          />
        </div>
        
        <div>
          <label className="block text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Feedback (Optional)</label>
          <textarea 
            rows="2"
            placeholder="Leave a comment..."
            className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-gray-200 placeholder-gray-600 focus:outline-none focus:border-green-500/50 focus:ring-1 focus:ring-green-500/50 transition-all resize-none"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
        </div>

        <div className="flex gap-4 pt-2">
          <button 
            onClick={() => handleDecision('auto_fix')}
            disabled={loading}
            className="flex-1 py-3 rounded-lg bg-blue-500/20 text-blue-400 font-bold border border-blue-500/30 hover:bg-blue-500/30 hover:shadow-[0_0_15px_rgba(59,130,246,0.2)] transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <CheckCircle2 className="w-5 h-5" />
            Auto-Fix
          </button>

          <button 
            onClick={() => handleDecision(true)}
            disabled={loading}
            className="flex-1 py-3 rounded-lg bg-green-500/20 text-green-400 font-bold border border-green-500/30 hover:bg-green-500/30 hover:shadow-[0_0_15px_rgba(34,197,94,0.2)] transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <CheckCircle2 className="w-5 h-5" />
            Approve
          </button>
          
          <button 
            onClick={() => handleDecision(false)}
            disabled={loading}
            className="flex-1 py-3 rounded-lg bg-red-500/10 text-red-400 font-bold border border-red-500/20 hover:bg-red-500/20 hover:shadow-[0_0_15px_rgba(239,68,68,0.2)] transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <XCircle className="w-5 h-5" />
            Reject
          </button>
        </div>
      </div>

      {error && (
        <div className="mt-4 p-4 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="mt-4 p-4 rounded-lg bg-green-500/10 border border-green-500/30 text-green-400 text-sm">
          {success}
        </div>
      )}
    </div>
  );
}
