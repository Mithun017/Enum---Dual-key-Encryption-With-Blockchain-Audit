import React, { useState, useEffect } from 'react';
import api from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

const Alerts = () => {
    const [alerts, setAlerts] = useState([]);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [alertsRes, statsRes] = await Promise.all([
                    api.get('/monitor/alerts'),
                    api.get('/monitor/stats')
                ]);
                setAlerts(alertsRes.data.alerts);
                setStats(statsRes.data);
            } catch (err) {
                const errorMsg = err.response?.data?.detail || err.message || 'Unknown error';
                setError(`Failed to fetch data: ${errorMsg}`);
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div className="result-box">Loading security data...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="alerts-container">
            <h2 className="alerts-header">Security Dashboard</h2>

            {/* Stats Overview */}
            {stats && (
                <div className="info-grid" style={{ marginBottom: '2rem' }}>
                    <div className="info-card">
                        <h2>Total Events</h2>
                        <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#38bdf8' }}>{stats.total_events}</p>
                    </div>
                    <div className="info-card">
                        <h2>Last 24 Hours</h2>
                        <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#34d399' }}>{stats.events_last_24h}</p>
                    </div>
                    <div className="info-card">
                        <h2>Failures</h2>
                        <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f87171' }}>{stats.distribution.FAILURE}</p>
                    </div>
                </div>
            )}

            {/* Graphs */}
            {stats && (
                <div className="charts-container" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '3rem' }}>
                    <div className="glass-panel" style={{ padding: '1.5rem' }}>
                        <h3 style={{ marginBottom: '1rem', color: '#bae6fd' }}>Activity Timeline (24h)</h3>
                        <div style={{ height: '300px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={stats.timeline}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                    <XAxis dataKey="time" stroke="#94a3b8" />
                                    <YAxis stroke="#94a3b8" />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', color: '#f1f5f9' }}
                                    />
                                    <Line type="monotone" dataKey="events" stroke="#38bdf8" strokeWidth={2} dot={{ r: 4 }} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    <div className="glass-panel" style={{ padding: '1.5rem' }}>
                        <h3 style={{ marginBottom: '1rem', color: '#bae6fd' }}>Event Distribution</h3>
                        <div style={{ height: '300px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={[
                                    { name: 'Encrypt', value: stats.distribution.ENCRYPTION, fill: '#38bdf8' },
                                    { name: 'Decrypt', value: stats.distribution.DECRYPTION, fill: '#34d399' },
                                    { name: 'Failure', value: stats.distribution.FAILURE, fill: '#f87171' },
                                ]}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                    <XAxis dataKey="name" stroke="#94a3b8" />
                                    <YAxis stroke="#94a3b8" />
                                    <Tooltip
                                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                        contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', color: '#f1f5f9' }}
                                    />
                                    <Bar dataKey="value" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>
            )}

            <h3 className="alerts-header" style={{ fontSize: '1.5rem', borderBottom: 'none' }}>Active Alerts</h3>
            {alerts.length === 0 ? (
                <div className="no-alerts">
                    No active security alerts. System is healthy.
                </div>
            ) : (
                <div>
                    {alerts.map((alert, index) => (
                        <div key={index} className="alert-item">
                            <p className="alert-message">{alert.message || alert}</p>
                            {alert.timestamp && (
                                <p className="alert-timestamp">
                                    {new Date(alert.timestamp * 1000).toLocaleString()}
                                </p>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Alerts;
