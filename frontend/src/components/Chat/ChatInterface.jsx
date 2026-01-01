import { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';
import PropertyCard from '../Properties/PropertyCard';
import { chatAPI } from '../../services/api';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [error, setError] = useState(null);
  const [propertyPages, setPropertyPages] = useState({}); // Track current page for each message
  const messagesEndRef = useRef(null);

  const PROPERTIES_PER_PAGE = 6;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Add welcome message on mount
  useEffect(() => {
    setMessages([
      {
        id: 'welcome',
        text: "Hello! 👋 I'm your AI assistant for finding homes in Lagos. I can help you discover properties, compare neighborhoods, and read authentic tenant reviews. What are you looking for today?",
        isUser: false,
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  const handlePageChange = (messageId, newPage) => {
    setPropertyPages((prev) => ({
      ...prev,
      [messageId]: newPage,
    }));
  };

  const getCurrentPage = (messageId) => {
    return propertyPages[messageId] || 1;
  };

  const getPaginatedProperties = (properties, messageId) => {
    const currentPage = getCurrentPage(messageId);
    const startIndex = (currentPage - 1) * PROPERTIES_PER_PAGE;
    const endIndex = startIndex + PROPERTIES_PER_PAGE;
    return properties.slice(startIndex, endIndex);
  };

  const getTotalPages = (properties) => {
    return Math.ceil(properties.length / PROPERTIES_PER_PAGE);
  };

  const handleSendMessage = async (messageText) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      text: messageText,
      isUser: true,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setError(null);
    setIsLoading(true);

    try {
      // Call backend API
      const response = await chatAPI.sendMessage(messageText, conversationId);

      // Set conversation ID if not set
      if (!conversationId && response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response,
        isUser: false,
        timestamp: new Date().toISOString(),
        properties: response.properties || [],
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to get a response. Please try again.');

      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm sorry, I encountered an error. Please try again or rephrase your question.",
        isUser: false,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-5xl mx-auto px-4">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto py-8 pr-8 space-y-6">
        {messages.length === 0 && !isLoading && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center max-w-2xl">
              <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-rajah/20 to-primary/20 rounded-3xl flex items-center justify-center">
                <svg className="w-10 h-10 text-rajah" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <h3 className="text-3xl font-bold text-white mb-4">Start Your Conversation</h3>
              <p className="text-white/70 mb-8">Ask me anything about properties in Lagos</p>
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 text-left">
                <p className="text-rajah font-semibold mb-3">Try asking:</p>
                <div className="space-y-2 text-white/80">
                  <p>💬 "Show me 2-bedroom apartments in Lekki"</p>
                  <p>💬 "What's it like living in Ikeja?"</p>
                  <p>💬 "Find properties under ₦3 million per year"</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div key={msg.id}>
            <ChatMessage
              message={msg.text}
              isUser={msg.isUser}
              timestamp={msg.timestamp}
            />
            {/* Show properties inline if available */}
            {msg.properties && msg.properties.length > 0 && (
              <div className="mt-4 ml-0 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {getPaginatedProperties(msg.properties, msg.id).map((property) => (
                    <PropertyCard key={property.id} property={property} />
                  ))}
                </div>

                {/* Pagination Controls */}
                {msg.properties.length > PROPERTIES_PER_PAGE && (
                  <div className="flex items-center justify-between mt-6 px-4">
                    {/* Previous Button */}
                    <button
                      onClick={() => handlePageChange(msg.id, getCurrentPage(msg.id) - 1)}
                      disabled={getCurrentPage(msg.id) === 1}
                      className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all ${
                        getCurrentPage(msg.id) === 1
                          ? 'bg-white/5 text-white/30 cursor-not-allowed'
                          : 'bg-marlin hover:bg-marlin/80 text-white border border-primary/20'
                      }`}
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                      </svg>
                      Previous
                    </button>

                    {/* Page Info */}
                    <div className="text-white/80 text-sm">
                      Page <span className="font-bold text-primary">{getCurrentPage(msg.id)}</span> of{' '}
                      <span className="font-bold text-primary">{getTotalPages(msg.properties)}</span>
                      <span className="text-white/60 ml-2">
                        ({msg.properties.length} properties total)
                      </span>
                    </div>

                    {/* Next Button */}
                    <button
                      onClick={() => handlePageChange(msg.id, getCurrentPage(msg.id) + 1)}
                      disabled={getCurrentPage(msg.id) === getTotalPages(msg.properties)}
                      className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all ${
                        getCurrentPage(msg.id) === getTotalPages(msg.properties)
                          ? 'bg-white/5 text-white/30 cursor-not-allowed'
                          : 'bg-marlin hover:bg-marlin/80 text-white border border-primary/20'
                      }`}
                    >
                      Next
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        {isLoading && <TypingIndicator />}
        {error && (
          <div className="bg-red-900/20 border border-red-500/50 text-red-200 px-6 py-4 rounded-2xl text-sm backdrop-blur-sm">
            {error}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input */}
      <div className="pb-6">
        <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatInterface;
