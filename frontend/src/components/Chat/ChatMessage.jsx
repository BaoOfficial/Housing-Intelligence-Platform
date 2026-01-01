import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatMessage = ({
  message,
  isUser,
  timestamp
}) => {
  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} ${
        isUser ? 'slide-in-right' : 'slide-in-left'
      }`}
    >
      {/* AI Avatar */}
      {!isUser && (
        <div className="flex-shrink-0 mr-3">
          <div className="w-10 h-10 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center border border-white/20">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      )}

      <div
        className={`max-w-[75%] rounded-2xl px-6 py-4 ${
          isUser
            ? 'bg-gradient-to-r from-marlin to-primary text-white shadow-lg'
            : 'bg-white/5 backdrop-blur-sm text-white border border-white/10'
        }`}
      >
        <div className="text-base leading-relaxed prose prose-invert max-w-none">
          {isUser ? (
            <p className="whitespace-pre-wrap">{message}</p>
          ) : (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                // Headings
                h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mb-3 text-rajah" {...props} />,
                h2: ({ node, ...props }) => <h2 className="text-xl font-bold mb-3 text-rajah" {...props} />,
                h3: ({ node, ...props }) => <h3 className="text-lg font-semibold mb-2 text-primary" {...props} />,
                h4: ({ node, ...props }) => <h4 className="text-base font-semibold mb-2 text-primary" {...props} />,

                // Paragraphs
                p: ({ node, ...props }) => <p className="mb-3 last:mb-0" {...props} />,

                // Lists
                ul: ({ node, ...props }) => <ul className="list-disc list-outside mb-3 space-y-2 pl-5" {...props} />,
                ol: ({ node, ...props }) => <ol className="list-decimal list-outside mb-3 space-y-2 pl-5" {...props} />,
                li: ({ node, ...props }) => <li className="ml-0 pl-2" {...props} />,

                // Strong/Bold
                strong: ({ node, ...props }) => <strong className="font-bold text-rajah" {...props} />,

                // Emphasis/Italic
                em: ({ node, ...props }) => <em className="italic text-primary" {...props} />,

                // Code
                code: ({ node, inline, ...props }) =>
                  inline ? (
                    <code className="bg-white/10 px-1.5 py-0.5 rounded text-sm font-mono" {...props} />
                  ) : (
                    <code className="block bg-white/10 p-3 rounded-lg text-sm font-mono overflow-x-auto mb-3" {...props} />
                  ),

                // Links
                a: ({ node, ...props }) => (
                  <a className="text-rajah hover:text-rajah/80 underline" target="_blank" rel="noopener noreferrer" {...props} />
                ),

                // Blockquotes
                blockquote: ({ node, ...props }) => (
                  <blockquote className="border-l-4 border-rajah pl-4 italic my-3 text-white/80" {...props} />
                ),

                // Horizontal Rule
                hr: ({ node, ...props }) => <hr className="border-white/20 my-4" {...props} />,
              }}
            >
              {message}
            </ReactMarkdown>
          )}
        </div>
        {timestamp && (
          <p className="text-xs mt-2 opacity-50">
            {new Date(timestamp).toLocaleTimeString('en-US', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="flex-shrink-0 ml-3">
          <div className="w-10 h-10 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center border border-white/20">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
