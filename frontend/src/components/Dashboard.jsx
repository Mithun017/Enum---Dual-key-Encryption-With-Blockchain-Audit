import React from 'react';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();
    const role = localStorage.getItem('role');
    const username = localStorage.getItem('username');

    const handleLogout = () => {
        localStorage.clear();
        navigate('/');
    };

    return (
        <div className="dashboard-container">
            <nav className="sidebar">
                <h3>Secure System</h3>
                <p>User: {username} ({role})</p>
                <ul>
                    {(role === 'ADMIN' || role === 'SERVICE') && (
                        <li><NavLink to="/dashboard/encrypt" className={({ isActive }) => isActive ? "active-link" : ""}>Encrypt Data</NavLink></li>
                    )}
                    {role === 'ADMIN' && (
                        <li><NavLink to="/dashboard/decrypt" className={({ isActive }) => isActive ? "active-link" : ""}>Decrypt Data</NavLink></li>
                    )}
                    {(role === 'ADMIN' || role === 'AUDITOR') && (
                        <li><NavLink to="/dashboard/ledger" className={({ isActive }) => isActive ? "active-link" : ""}>Audit Ledger</NavLink></li>
                    )}
                    {role === 'ADMIN' && (
                        <li><NavLink to="/dashboard/alerts" className={({ isActive }) => isActive ? "active-link" : ""}>Security Alerts</NavLink></li>
                    )}
                </ul>
                <button onClick={handleLogout} className="logout-btn">Logout</button>
            </nav>
            <main className="content">
                <Outlet />
            </main>
        </div>
    );
};

export default Dashboard;
