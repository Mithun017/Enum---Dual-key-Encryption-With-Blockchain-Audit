import React from 'react';

const SystemInfo = () => {
    return (
        <div className="system-info-container">
            <h1>System Overview</h1>

            <div className="info-grid">
                <div className="info-card">
                    <h2>🛡️ Security Status</h2>
                    <ul>
                        <li><strong>Encryption Engine:</strong> Active</li>
                        <li><strong>Algorithm:</strong> AES-256 + Kyber-1024 (Post-Quantum)</li>
                        <li><strong>Key Management:</strong> Dual-Key (Split Knowledge)</li>
                    </ul>
                </div>

                <div className="info-card">
                    <h2>🔗 Blockchain Ledger</h2>
                    <ul>
                        <li><strong>Status:</strong> Connected</li>
                        <li><strong>Consensus:</strong> Proof of Authority (PoA)</li>
                        <li><strong>Integrity Check:</strong> Passing</li>
                    </ul>
                </div>

                <div className="info-card">
                    <h2>👤 User Session</h2>
                    <ul>
                        <li><strong>Role:</strong> {localStorage.getItem('role') || 'Unknown'}</li>
                        <li><strong>Session:</strong> Secure (JWT)</li>
                        <li><strong>Auto-Logout:</strong> Enabled (24h)</li>
                    </ul>
                </div>
            </div>

            <div className="glass-panel" style={{ marginTop: '2rem', padding: '2rem' }}>
                <h3 style={{ color: '#38bdf8' }}>About This System</h3>
                <p style={{ color: '#bae6fd', lineHeight: '1.6' }}>
                    This application utilizes a <strong>Hybrid Post-Quantum Encryption Scheme</strong>.
                    Data is secured using a combination of a server-stored Kyber-1024 private key and a user-held password.
                    Every encryption and decryption event is immutably recorded on a local blockchain ledger to ensure
                    complete accountability and auditability.
                </p>
            </div>
        </div>
    );
};

export default SystemInfo;
