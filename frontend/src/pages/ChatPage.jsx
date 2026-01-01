import ChatInterface from '../components/Chat/ChatInterface';
import { ASSISTANT_NAME, ASSISTANT_TAGLINE } from '../constants/app';

const ChatPage = () => {
  return (
    <div className="min-h-screen bg-port-gore">
      {/* Modern Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/5 backdrop-blur-md border-b border-white/10">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-rajah to-primary rounded-xl flex items-center justify-center shadow-lg">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">{ASSISTANT_NAME}</h1>
              <p className="text-xs text-primary/80">{ASSISTANT_TAGLINE}</p>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Interface */}
      <div className="pt-20 h-screen">
        <ChatInterface />
      </div>
    </div>
  );
};

export default ChatPage;
