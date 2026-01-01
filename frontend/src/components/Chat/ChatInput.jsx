import { useState } from 'react';

const ChatInput = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="relative bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 focus-within:border-rajah/50 transition-all duration-300">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about Lagos properties..."
          disabled={disabled}
          rows={1}
          className="w-full bg-transparent text-white rounded-3xl px-6 py-4 pr-24 focus:outline-none resize-none placeholder-white/40 disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ minHeight: '56px', maxHeight: '150px' }}
        />
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="absolute right-2 bottom-2 bg-gradient-to-r from-rajah to-primary text-white rounded-2xl p-3 font-semibold shadow-lg hover:shadow-rajah/50 transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2.5}
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </div>
      <p className="text-xs text-white/40 mt-3 ml-2">
        💡 Press Enter to send • Shift+Enter for new line
      </p>
    </form>
  );
};

export default ChatInput;
