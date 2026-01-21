import React from 'react';

const SystemInfo = () => {
    return (
        <div className="system-info-container">
            <h1>System Overview</h1>

            <div className="info-grid">

                {/* Encryption Card */}
                <div className="info-card" style={{ borderColor: 'rgba(59, 130, 246, 0.3)' }}>
                    <h2 style={{ color: '#93c5fd' }}>🔐 Dual-Key Encryption</h2>
                    <p style={{ color: '#cbd5e1', marginBottom: '1rem' }}>
                        This system uses a hybrid post-quantum encryption scheme to protect your data.
                    </p>
                    <ul>
                        <li>
                            <strong>Kyber-1024 (KEM):</strong> A NIST-approved post-quantum algorithm used to securely exchange keys, resistant to future quantum computer attacks.
                        </li>
                        <li>
                            <strong>AES-256 (GCM):</strong> Advanced Encryption Standard used for high-speed, military-grade data encryption.
                        </li>
                        <li>
                            <strong>Dual Control:</strong> Decryption requires BOTH the System Key (stored on server) and the User Key (provided by you).
                        </li>
                    </ul>
                </div>

                {/* Blockchain Card */}
                <div className="info-card" style={{ borderColor: 'rgba(34, 197, 94, 0.3)' }}>
                    <h2 style={{ color: '#86efac' }}>🔗 Blockchain Audit</h2>
                    <p style={{ color: '#cbd5e1', marginBottom: '1rem' }}>
                        Every action in the system is permanently recorded in an immutable ledger.
                    </p>
                    <ul>
                        <li>
                            <strong>Immutable Ledger:</strong> Once a block is added, it cannot be changed or deleted.
                        </li>
                        <li>
                            <strong>SHA-256 Hashing:</strong> Each block is cryptographically linked to the previous one, ensuring chain integrity.
                        </li>
                        <li>
                            <strong>Transparency:</strong> Auditors can verify the entire history of encryption and decryption events.
                        </li>
                    </ul>
                </div>

                {/* Database Card */}
                <div className="info-card" style={{ borderColor: 'rgba(168, 85, 247, 0.3)' }}>
                    <h2 style={{ color: '#d8b4fe' }}>🗄️ Secure Storage</h2>
                    <p style={{ color: '#cbd5e1', marginBottom: '1rem' }}>
                        Data is stored securely using enterprise-grade technologies.
                    </p>
                    <ul>
                        <li>
                            <strong>MySQL Database:</strong> Robust relational storage for users, keys, and the ledger.
                        </li>
                        <li>
                            <strong>Role-Based Access:</strong> Strict permission controls for Admins, Services, and Auditors.
                        </li>
                    </ul>
                </div>

            </div>
        </div>
    );
};

export default SystemInfo;
