import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('ADMIN');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            // Construct payload to match backend LoginRequest model
            const payload = {
                user: { username, role },
                password
            };

            const res = await api.post('/auth/login', payload);

            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('role', role);
            localStorage.setItem('username', username);
            navigate('/dashboard');
        } catch (err) {
            setError('Login failed. Check credentials.');
            console.error(err);
        }
    };

    return (
        <div className="login-container">
            <h2>Secure Login</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleLogin}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Role:</label>
                    <select value={role} onChange={(e) => setRole(e.target.value)}>
                        <option value="ADMIN">ADMIN</option>
                        <option value="SERVICE">SERVICE</option>
                        <option value="AUDITOR">AUDITOR</option>
                    </select>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
