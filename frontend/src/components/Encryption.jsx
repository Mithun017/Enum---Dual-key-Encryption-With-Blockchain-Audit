import React, { useState } from 'react';
import api from '../api';

const Encryption = () => {
    const [mode, setMode] = useState('text'); // 'text' or 'file'
    const [formData, setFormData] = useState({
        data: '',
        user_key: '',
        key_id: ''
    });
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleEncrypt = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);
        setLoading(true);

        try {
            let res;
            if (mode === 'text') {
                res = await api.post('/encryption/encrypt', formData);
                setResult(res.data);
            } else {
                if (!file) {
                    setError("Please select a file to encrypt.");
                    setLoading(false);
                    return;
                }
                const data = new FormData();
                data.append('file', file);
                data.append('user_key', formData.user_key);
                data.append('key_id', formData.key_id);

                res = await api.post('/encryption/encrypt-file', data, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
                setResult(res.data);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Encryption failed');
        } finally {
            setLoading(false);
        }
    };

    const downloadFile = () => {
        if (!result || !result.encrypted_file) return;

        // Convert base64 to blob
        const byteCharacters = atob(result.encrypted_file);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: "application/octet-stream" });

        // Create link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = result.filename || "encrypted_file.enc";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    };

    return (
        <div className="form-container">
            <h2>Encrypt Data</h2>

            <div className="tabs">
                <button
                    className={`tab-btn ${mode === 'text' ? 'active' : ''}`}
                    onClick={() => { setMode('text'); setResult(null); setError(''); }}
                >
                    Text Encryption
                </button>
                <button
                    className={`tab-btn ${mode === 'file' ? 'active' : ''}`}
                    onClick={() => { setMode('file'); setResult(null); setError(''); }}
                >
                    File Encryption
                </button>
            </div>

            <form onSubmit={handleEncrypt}>
                {mode === 'text' ? (
                    <div className="form-group">
                        <label>Data to Encrypt</label>
                        <textarea
                            name="data"
                            value={formData.data}
                            onChange={handleChange}
                            required
                            placeholder="Enter sensitive text here..."
                        />
                    </div>
                ) : (
                    <div className="form-group">
                        <label>Select File</label>
                        <input
                            type="file"
                            onChange={handleFileChange}
                            required
                            className="file-input"
                        />
                    </div>
                )}

                <div className="form-group">
                    <label>User Key (Key-B)</label>
                    <input
                        type="password"
                        name="user_key"
                        value={formData.user_key}
                        onChange={handleChange}
                        required
                        placeholder="Enter your secret password"
                    />
                </div>

                <div className="form-group">
                    <label>Key ID (Key-A)</label>
                    <input
                        type="text"
                        name="key_id"
                        value={formData.key_id}
                        onChange={handleChange}
                        required
                        placeholder="e.g., sys-key-1"
                    />
                </div>

                <button type="submit" disabled={loading}>
                    {loading ? 'Encrypting...' : 'Encrypt'}
                </button>
            </form>

            {error && <p className="error">{error}</p>}

            {result && (
                <div className="result-box">
                    <h3>Encryption Successful!</h3>
                    <p><strong>Key ID:</strong> {result.key_id}</p>

                    <div className="result-field">
                        <label>Kyber Ciphertext (SAVE THIS!):</label>
                        <textarea readOnly value={result.kyber_ciphertext} />
                        <button
                            className="copy-btn"
                            onClick={() => navigator.clipboard.writeText(result.kyber_ciphertext)}
                        >
                            Copy Ciphertext
                        </button>
                    </div>

                    {mode === 'text' ? (
                        <div className="result-field">
                            <label>Encrypted Data:</label>
                            <textarea readOnly value={result.encrypted_data} />
                            <button
                                className="copy-btn"
                                onClick={() => navigator.clipboard.writeText(result.encrypted_data)}
                            >
                                Copy Encrypted Data
                            </button>
                        </div>
                    ) : (
                        <div className="result-field">
                            <label>Encrypted File:</label>
                            <p>File ready for download.</p>
                            <button className="download-btn" onClick={downloadFile}>
                                Download {result.filename}
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Encryption;
