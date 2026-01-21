import React, { useEffect, useState } from 'react';
import api from '../api';

const Ledger = () => {
    const [chain, setChain] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchLedger = async () => {
            try {
                const res = await api.get('/audit/ledger');
                setChain(res.data.chain);
            } catch (err) {
                setError('Failed to fetch ledger. ' + (err.response?.data?.detail || err.message));
            }
        };
        fetchLedger();
    }, []);

    return (
        <div className="table-container">
            <h2>Blockchain Audit Ledger</h2>
            {error && <p className="error">{error}</p>}
            <table>
                <thead>
                    <tr>
                        <th>Index</th>
                        <th>Event</th>
                        <th>User ID</th>
                        <th>Key ID</th>
                        <th>Timestamp</th>
                        <th>Hash</th>
                    </tr>
                </thead>
                <tbody>
                    {chain.map((block) => (
                        <tr key={block.hash}>
                            <td>{block.index}</td>
                            <td>{block.event_type}</td>
                            <td>{block.user_id}</td>
                            <td>{block.key_id}</td>
                            <td>{new Date(block.timestamp * 1000).toLocaleString()}</td>
                            <td className="hash-cell" title={block.hash}>{block.hash.substring(0, 10)}...</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Ledger;
