import React from "react";
import { createRoot } from "react-dom/client";
import Dashboard from "./components/Dashboard.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";

function App() {
  return (
    <AuthProvider>
      <div className="max-w-screen-xl mx-auto p-4">
        <Dashboard />
      </div>
    </AuthProvider>
  );
}

const root = createRoot(document.getElementById("root"));
root.render(<App />);
