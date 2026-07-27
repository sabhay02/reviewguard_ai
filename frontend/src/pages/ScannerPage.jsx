import React from 'react';
import { ShieldCheck, Code2, TerminalSquare, ArrowLeft } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import ScannerForm from '../components/ScannerForm';

function ScannerPage() {
  const navigate = useNavigate();

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
            <Link to="/" className="flex items-center gap-4 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-[0_0_20px_rgba(139,92,246,0.3)]">
                <ShieldCheck className="text-white w-6 h-6" />
              </div>
              <span className="text-2xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 via-purple-300 to-purple-400 drop-shadow-[0_0_15px_rgba(168,85,247,0.4)]">
                ReviewGuard <span className="font-light text-purple-200">AI</span>
              </span>
            </Link>
            
            <div className="flex items-center gap-6">
              <Link to="/" className="text-gray-400 hover:text-white transition-colors flex items-center gap-2 text-sm font-medium">
                <ArrowLeft className="w-4 h-4" />
                Back to Dashboard
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-[800px] mx-auto px-6 py-12 relative z-10">
        <div className="mb-8">
          <h1 className="text-4xl font-black text-white mb-2 tracking-tight">Manual AI Scanner</h1>
          <p className="text-gray-400 font-light">Deploy DevSecOps agents against any public repository or Pull Request to receive an instant analysis.</p>
        </div>
        
        <div className="h-auto">
          <ScannerForm onScanComplete={() => navigate('/')} />
        </div>
      </main>
    </div>
  );
}

export default ScannerPage;
