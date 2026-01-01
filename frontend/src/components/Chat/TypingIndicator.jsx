const TypingIndicator = () => {
  return (
    <div className="flex justify-start slide-in-left">
      {/* AI Avatar */}
      <div className="flex-shrink-0 mr-3">
        <div className="w-10 h-10 bg-gradient-to-br from-rajah to-primary rounded-xl flex items-center justify-center shadow-lg">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl px-6 py-4 flex items-center space-x-3">
        <div className="flex space-x-1">
          <div
            className="w-2.5 h-2.5 bg-rajah rounded-full"
            style={{ animation: 'bounce 1.4s infinite ease-in-out both', animationDelay: '-0.32s' }}
          ></div>
          <div
            className="w-2.5 h-2.5 bg-primary rounded-full"
            style={{ animation: 'bounce 1.4s infinite ease-in-out both', animationDelay: '-0.16s' }}
          ></div>
          <div
            className="w-2.5 h-2.5 bg-rajah rounded-full"
            style={{ animation: 'bounce 1.4s infinite ease-in-out both' }}
          ></div>
        </div>
        <span className="text-sm text-white/70">AI is thinking...</span>
      </div>
    </div>
  );
};

export default TypingIndicator;
