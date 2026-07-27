import React from 'react';

export default function StatCard({ title, value, icon: Icon, colorClass }) {
  return (
    <div className="glass-panel p-6 relative overflow-hidden group hover:border-purple-500/40 transition-all duration-300 hover:-translate-y-1 hover:shadow-purple-500/20 hover:shadow-lg">
      <div className={`absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-10 blur-3xl transition-transform duration-700 group-hover:scale-150 group-hover:opacity-20 ${colorClass}`}></div>
      
      <div className="flex items-center justify-between mb-4 relative z-10">
        <h3 className="text-gray-400 font-medium text-xs tracking-[0.2em] uppercase">{title}</h3>
        {Icon && (
          <div className="p-2 rounded-lg bg-white/5 border border-white/5">
            <Icon className={`w-5 h-5 ${colorClass.replace('bg-', 'text-')}`} />
          </div>
        )}
      </div>
      
      <div className="relative z-10 flex items-baseline gap-2">
        <span className="text-4xl font-extrabold text-white tracking-tight">{value}</span>
      </div>
      
      <div className="absolute bottom-0 left-0 h-1 w-full opacity-50 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
    </div>
  );
}
