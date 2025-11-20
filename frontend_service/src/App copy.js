import React, { useState, useEffect } from 'react';
import { MessageSquare, LogOut, Send, User, TrendingUp, History } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000/api/v1'; // Change this to your backend URL

export default function LLMQueryApp() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [token, setToken] = useState('');
  const [currentUser, setCurrentUser] = useState('');
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [stats, setStats] = useState(null);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    const savedToken = sessionStorage.getItem('token');
    const savedUser = sessionStorage.getItem('username');
    if (savedToken && savedUser) {
      setToken(savedToken);
      setCurrentUser(savedUser);
      setIsLoggedIn(true);
      fetchStats(savedToken);
    }
  }, []);

  const fetchStats = async (authToken) => {
    try {
      const response = await fetch(`${API_BASE_URL}/queries/stats`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/queries/history`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        const formattedMessages = [];
        data.forEach(item => {
          formattedMessages.push({ role: 'user', content: item.query, timestamp: item.timestamp });
          formattedMessages.push({ role: 'assistant', content: item.response, timestamp: item.timestamp });
        });
        setMessages(formattedMessages);
        setShowHistory(false);
      } else {
        setError('Failed to fetch history');
      }
    } catch (err) {
      setError('Error fetching history: ' + err.message);
    }
  };

  const handleRegister = async () => {
    setError('');
    if (!username.trim() || !password.trim() || !email.trim()) {
      setError('Please fill in all fields');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          email: email,
          password: password
        })
      });

      const data = await response.json();

      if (response.ok) {
        setError('');
        setIsRegistering(false);
        setEmail('');
        alert('Registration successful! Please login.');
      } else {
        setError(data.detail || data.message || 'Registration failed');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    }
  };

  const handleLogin = async () => {
    setError('');
    if (!username.trim() || !password.trim()) {
      setError('Please enter username and password');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password
        })
      });

      const data = await response.json();

      if (response.ok) {
        const authToken = data.access_token || data.token;
        setToken(authToken);
        setCurrentUser(username);
        setIsLoggedIn(true);
        sessionStorage.setItem('token', authToken);
        sessionStorage.setItem('username', username);
        setUsername('');
        setPassword('');
        setError('');
        fetchStats(authToken);
      } else {
        setError(data.detail || data.message || 'Login failed');
      }
    } catch (err) {
      setError('Network error: ' + err.message);
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('username');
    setIsLoggedIn(false);
    setToken('');
    setCurrentUser('');
    setMessages([]);
    setStats(null);
  };

  const handleSubmitQuery = async () => {
    if (!query.trim() || isLoading) return;

    const userMessage = { role: 'user', content: query };
    setMessages(prev => [...prev, userMessage]);
    const currentQuery = query;
    setQuery('');
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/queries/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          query: currentQuery
        })
      });

      const data = await response.json();

      if (response.ok) {
        const assistantMessage = {
          role: 'assistant',
          content: data.response || data.answer || 'No response received'
        };
        setMessages(prev => [...prev, assistantMessage]);
        fetchStats(token);
      } else {
        const errorMessage = {
          role: 'assistant',
          content: `Error: ${data.detail || data.message || 'Failed to get response'}`
        };
        setMessages(prev => [...prev, errorMessage]);
        setError(data.detail || data.message || 'Query failed');
      }
    } catch (err) {
      const errorMessage = {
        role: 'assistant',
        content: 'Network error: ' + err.message
      };
      setMessages(prev => [...prev, errorMessage]);
      setError('Network error: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (isLoggedIn) {
        handleSubmitQuery();
      } else if (isRegistering) {
        handleRegister();
      } else {
        handleLogin();
      }
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
          <div className="flex items-center justify-center mb-6">
            <MessageSquare className="w-12 h-12 text-indigo-600" />
          </div>
          <h1 className="text-3xl font-bold text-center text-gray-800 mb-2">
            LLM Query App
          </h1>
          <p className="text-center text-gray-600 mb-8">
            {isRegistering ? 'Create your account' : 'Sign in to start chatting'}
          </p>
          
          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="space-y-4">
            {isRegistering && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                  placeholder="Enter email"
                />
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                onKeyPress={handleKeyPress}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                placeholder="Enter username"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyPress={handleKeyPress}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                placeholder="Enter password"
              />
            </div>
            <button
              onClick={isRegistering ? handleRegister : handleLogin}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition shadow-lg"
            >
              {isRegistering ? 'Register' : 'Sign In'}
            </button>
            <button
              onClick={() => {
                setIsRegistering(!isRegistering);
                setError('');
              }}
              className="w-full text-indigo-600 py-2 rounded-lg font-medium hover:bg-indigo-50 transition"
            >
              {isRegistering ? 'Already have an account? Sign In' : 'Need an account? Register'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-3">
            <MessageSquare className="w-8 h-8 text-indigo-600" />
            <h1 className="text-2xl font-bold text-gray-800">LLM Query App</h1>
          </div>
          
          {stats && (
            <div className="flex items-center gap-2 px-4 py-2 bg-indigo-50 rounded-lg">
              <TrendingUp className="w-5 h-5 text-indigo-600" />
              <span className="text-sm font-medium text-gray-700">
                Queries: {stats.daily_queries || stats.queries_today || 0} / {stats.daily_limit || stats.limit || 'unlimited'}
              </span>
            </div>
          )}

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-gray-700">
              <User className="w-5 h-5" />
              <span className="font-medium">{currentUser}</span>
            </div>
            <button
              onClick={fetchHistory}
              className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition"
            >
              <History className="w-4 h-4" />
              History
            </button>
            <button
              onClick={clearChat}
              className="px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition"
            >
              Clear
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="max-w-5xl mx-auto w-full px-4 pt-4">
          <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-5xl mx-auto space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-12">
              <MessageSquare className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p className="text-lg">No messages yet. Start a conversation!</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-2xl px-6 py-4 rounded-2xl ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-white text-gray-800 shadow-md border border-gray-200'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-2xl px-6 py-4 rounded-2xl bg-white text-gray-800 shadow-md border border-gray-200">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-5xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your query here..."
              className="flex-1 px-6 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
              disabled={isLoading}
            />
            <button
              onClick={handleSubmitQuery}
              disabled={isLoading || !query.trim()}
              className="px-8 py-4 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2 font-semibold shadow-lg"
            >
              <Send className="w-5 h-5" />
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}