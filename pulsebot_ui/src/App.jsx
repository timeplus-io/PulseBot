import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Chat from './pages/Chat';
import Dashboard from './pages/Dashboard';
import Events from './pages/Events';
import LLMLogs from './pages/LLMLogs';
import ToolLogs from './pages/ToolLogs';
import Agents from './pages/Agents';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/events" element={<Events />} />
        <Route path="/llm-logs" element={<LLMLogs />} />
        <Route path="/tool-logs" element={<ToolLogs />} />
        <Route path="/agents" element={<Agents />} />
      </Routes>
    </Layout>
  );
}
