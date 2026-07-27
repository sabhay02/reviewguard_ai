import React from 'react';
import { ShieldAlert, ShieldCheck, Shield, AlertTriangle, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const RiskBadge = ({ risk }) => {
  const styles = {
    CRITICAL: 'bg-red-500/10 text-red-400 border-red-500/30 shadow-[0_0_10px_rgba(239,68,68,0.2)]',
    HIGH: 'bg-orange-500/10 text-orange-400 border-orange-500/30 shadow-[0_0_10px_rgba(249,115,22,0.2)]',
    MEDIUM: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30 shadow-[0_0_10px_rgba(234,179,8,0.2)]',
    LOW: 'bg-green-500/10 text-green-400 border-green-500/30 shadow-[0_0_10px_rgba(34,197,94,0.2)]',
  };

  const icons = {
    CRITICAL: <ShieldAlert className="w-3.5 h-3.5 mr-1.5" />,
    HIGH: <AlertTriangle className="w-3.5 h-3.5 mr-1.5" />,
    MEDIUM: <Shield className="w-3.5 h-3.5 mr-1.5" />,
    LOW: <ShieldCheck className="w-3.5 h-3.5 mr-1.5" />,
  };

  const style = styles[risk] || styles.LOW;
  
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold tracking-wide border ${style}`}>
      {icons[risk] || icons.LOW}
      {risk}
    </span>
  );
};

const GradeBadge = ({ grade }) => {
  const color = grade === 'A' || grade === 'B' ? 'text-green-400 drop-shadow-[0_0_8px_rgba(34,197,94,0.5)]' : 
                grade === 'C' ? 'text-yellow-400 drop-shadow-[0_0_8px_rgba(234,179,8,0.5)]' : 
                'text-red-400 drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]';
  
  return <span className={`text-xl font-black ${color}`}>{grade}</span>;
};

export default function ReviewsTable({ reviews }) {
  const navigate = useNavigate();

  if (!reviews || reviews.length === 0) {
    return (
      <div className="glass-panel p-12 text-center flex flex-col items-center justify-center">
        <Shield className="w-12 h-12 text-gray-600 mb-4" />
        <h3 className="text-xl font-medium text-gray-300">No Scans Found</h3>
        <p className="text-gray-500 mt-2">Connect a repository and trigger a webhook to see results here.</p>
      </div>
    );
  }

  return (
    <div className="glass-panel overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-white/10 bg-white/[0.02]">
              <th className="px-6 py-5 text-xs font-bold text-gray-500 uppercase tracking-widest">Repository</th>
              <th className="px-6 py-5 text-xs font-bold text-gray-500 uppercase tracking-widest">Date scanned</th>
              <th className="px-6 py-5 text-xs font-bold text-gray-500 uppercase tracking-widest">Risk Level</th>
              <th className="px-6 py-5 text-xs font-bold text-gray-500 uppercase tracking-widest">Grade</th>
              <th className="px-6 py-5 text-xs font-bold text-gray-500 uppercase tracking-widest">Security Score</th>
              <th className="px-6 py-5 text-xs font-bold text-gray-500 uppercase tracking-widest">Issues</th>
              <th className="px-6 py-5"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.05]">
            {reviews.map((review) => (
              <tr 
                key={review.id} 
                onClick={() => {
                  if (review.review_id) {
                    navigate(`/report/${review.review_id}`);
                  } else {
                    alert("This older scan does not have a saved report file linked to it.");
                  }
                }}
                className="hover:bg-white/[0.03] transition-colors group cursor-pointer"
              >
                <td className="px-6 py-5 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-purple-500/30 flex items-center justify-center mr-3">
                      <Shield className="w-4 h-4 text-purple-400" />
                    </div>
                    <span className="text-sm font-semibold text-gray-200 group-hover:text-purple-300 transition-colors">
                      {review.repository.split('/').pop()}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-5 whitespace-nowrap text-sm text-gray-400">
                  {new Date(review.review_date).toLocaleString(undefined, {
                    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                  })}
                </td>
                <td className="px-6 py-5 whitespace-nowrap">
                  <RiskBadge risk={review.risk} />
                </td>
                <td className="px-6 py-5 whitespace-nowrap">
                  <GradeBadge grade={review.grade} />
                </td>
                <td className="px-6 py-5 whitespace-nowrap">
                  <div className="flex items-center w-32">
                    <div className="w-full bg-gray-800 rounded-full h-1.5 mr-3 overflow-hidden border border-gray-700">
                      <div 
                        className={`h-full rounded-full transition-all duration-1000 ${
                          review.score > 80 ? 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]' :
                          review.score > 50 ? 'bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.5)]' :
                          'bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]'
                        }`} 
                        style={{ width: `${review.score}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-bold text-gray-300 w-8">{review.score}</span>
                  </div>
                </td>
                <td className="px-6 py-5 whitespace-nowrap text-sm font-medium text-gray-300">
                  <div className="flex items-center">
                    <BugIcon count={review.findings} />
                    <span className="ml-2">{review.findings}</span>
                  </div>
                </td>
                <td className="px-6 py-5 whitespace-nowrap text-right">
                  <button className="text-gray-500 group-hover:text-purple-400 transition-colors p-2 rounded-full hover:bg-white/5">
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function BugIcon({ count }) {
  if (count === 0) return <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.8)]" />;
  if (count < 10) return <span className="w-2 h-2 rounded-full bg-yellow-500 shadow-[0_0_8px_rgba(234,179,8,0.8)]" />;
  return <span className="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)] animate-pulse" />;
}
