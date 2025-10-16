import { Outlet } from 'react-router-dom';
import Sidebar from './sidebar';
import Header from './Header';
import './Layout.css';

const Layout = () => {
  return (
    <div className="flex h-screen bg-[var(--color-dark-bg)]">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto scrollbar-hide p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;