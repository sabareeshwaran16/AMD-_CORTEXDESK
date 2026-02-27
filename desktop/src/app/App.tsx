import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from '../pages/Dashboard/Dashboard';
import Meetings from '../pages/Meetings/Meetings';
import ResearchWorkspace from '../pages/ResearchWorkspace/ResearchWorkspace';
import Tasks from '../pages/Tasks/Tasks';
import Settings from '../pages/Settings/Settings';
import Layout from './layout/Layout';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/meetings" element={<Meetings />} />
          <Route path="/research" element={<ResearchWorkspace />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;

