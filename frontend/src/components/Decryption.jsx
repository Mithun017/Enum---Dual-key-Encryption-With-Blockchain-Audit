import React, { useState } from 'react';
import api from '../api';

const Decryption = () => {
    const [mode, setMode] = useState('text'); // 'text' or 'file'
    const [formData, setFormData] = useState({
        encrypted_data: '',
        kyber_ciphertext: '',
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

    const handleDecrypt = async (e) => {
        e.preventDefault();
        setError('');
        setResult(null);
        setLoading(true);

        try {
            let res;
            if (mode === 'text') {
                res = await api.post('/encryption/decrypt', formData);
                setResult(res.data.data);
            } else {
                if (!file) {
                    setError("Please select an encrypted file.");
                    setLoading(false);
                    return;
                }
                const data = new FormData();
                data.append('file', file);
                data.append('kyber_ciphertext', formData.kyber_ciphertext);
                data.append('user_key', formData.user_key);
                data.append('key_id', formData.key_id);

                res = await api.post('/encryption/decrypt-file', data, {
                    responseType: 'blob', // Important for file download
                    headers: { 'Content-Type': 'multipart/form-data' }
                });

                // Create download link for decrypted file
                const url = window.URL.createObjectURL(new Blob([res.data]));
                const link = document.createElement('a');
                link.href = url;
                const originalName = file.name.replace(".enc", "");
                link.setAttribute('download', `decrypted_${originalName}`);
                document.body.appendChild(link);
                link.click();
                link.remove();

                setResult("File decrypted and downloaded successfully!");
            }
        } catch (err) {
            console.error(err);
            if (err.response && err.response.data instanceof Blob) {
                // Parse blob error
                const text = await err.response.data.text();
                try {
                    const json = JSON.parse(text);
                    setError(json.detail || 'Decryption failed');
                } catch {
                    setError('Decryption failed');
                }
            } else {
                setError(err.response?.data?.detail || 'Decryption failed');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-container">
            <h2>Decrypt Data</h2>

            <div className="tabs">
                <button
                    className={`tab-btn ${mode === 'text' ? 'active' : ''}`}
                    onClick={() => { setMode('text'); setResult(null); setError(''); }}
                >
                    Text Decryption
                </button>
                <button
                    className={`tab-btn ${mode === 'file' ? 'active' : ''}`}
                    onClick={() => { setMode('file'); setResult(null); setError(''); }}
                >
                    File Decryption
                </button>
            </div>

            <form onSubmit={handleDecrypt}>
                {mode === 'text' ? (
                    <div className="form-group">
                        <label>Encrypted Data</label>
                        <textarea
                            name="encrypted_data"
                            value={formData.encrypted_data}
                            onChange={handleChange}
                            required
                            placeholder="Paste encrypted string here..."
                        />
                    </div>
                ) : (
                    <div className="form-group">
                        <label>Select Encrypted File (.enc)</label>
                        <input
                            type="file"
                            onChange={handleFileChange}
                            required
                            className="file-input"
                        />
                    </div>
                )}

                <div className="form-group">
                    <label>Kyber Ciphertext</label>
                    <textarea
                        name="kyber_ciphertext"
                        value={formData.kyber_ciphertext}
                        onChange={handleChange}
                        required
                        placeholder="Paste Kyber ciphertext here..."
                    />
                </div>

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
                    {loading ? 'Decrypting...' : 'Decrypt'}
                </button>
            </form>

            {error && <p className="error">{error}</p>}

            {result && (
                <div className="result-box">
                    <h3>Decryption Successful!</h3>
                    {mode === 'text' ? (
                        <div className="result-field">
                            <label>Decrypted Data:</label>
                            <textarea readOnly value={result} />
                            <button
                                className="copy-btn"
                                onClick={() => navigator.clipboard.writeText(result)}
                            >
                                Copy Text
                            </button>
                        </div>
                    ) : (
                        <p className="success-msg">{result}</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default Decryption;
