import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function MarkdownRenderer({ content }) {
  return (
    <div className="prose prose-invert prose-purple max-w-none prose-sm lg:prose-base">
      <ReactMarkdown
        components={{
          code({node, inline, className, children, ...props}) {
            const match = /language-(\w+)/.exec(className || '')
            return !inline && match ? (
              <div className="relative group rounded-xl overflow-hidden border border-white/10 my-6 shadow-[0_0_20px_rgba(0,0,0,0.5)]">
                <div className="flex items-center justify-between px-4 py-2 bg-[#1e1e1e] border-b border-white/5">
                  <span className="text-xs font-mono text-gray-400 uppercase tracking-wider">{match[1]}</span>
                  <button 
                    onClick={() => navigator.clipboard.writeText(String(children).replace(/\n$/, ''))}
                    className="text-xs font-semibold text-gray-500 hover:text-white transition-colors"
                  >
                    Copy
                  </button>
                </div>
                <SyntaxHighlighter
                  {...props}
                  children={String(children).replace(/\n$/, '')}
                  style={vscDarkPlus}
                  language={match[1]}
                  PreTag="div"
                  customStyle={{ margin: 0, padding: '1rem', background: '#0a0a0f' }}
                  showLineNumbers={true}
                />
              </div>
            ) : (
              <code {...props} className={`${className} bg-purple-500/10 text-purple-300 px-1.5 py-0.5 rounded-md font-mono text-sm border border-purple-500/20`}>
                {children}
              </code>
            )
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
