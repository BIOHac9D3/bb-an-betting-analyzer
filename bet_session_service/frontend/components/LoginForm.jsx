import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function LoginForm() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    setError(null);
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || "Login failed");
        return;
      }
      const data = await res.json();
      login({ username, token: data.access_token });
    } catch (err) {
      setError("Network error");
    }
  };

  return (
    <div className="bg-gray-800 text-white p-4 rounded w-64">
      <h3 className="font-semibold mb-2">Login</h3>
      <input
        type="text"
        value={username}
        onChange={e => setUsername(e.target.value)}
        className="w-full mb-2 p-1"
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        className="w-full mb-2 p-1"
        placeholder="Password"
      />
      {error && <div className="text-red-500 mb-2">{error}</div>}
      <button onClick={handleLogin} className="bg-blue-500 px-4 py-1 rounded">
        Login
      </button>
    </div>
  );
}
