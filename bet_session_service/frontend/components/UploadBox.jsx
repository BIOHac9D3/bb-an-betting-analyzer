import { useAuth } from "../context/AuthContext";

export default function UploadBox({ onUpload }) {
  const { user } = useAuth();

  const handleFile = async (e) => {
    const files = Array.from(e.target.files);
    const jsonData = [];

    for (const file of files) {
      const text = await file.text();
      try {
        const parsed = JSON.parse(text);
        jsonData.push(...(Array.isArray(parsed) ? parsed : [parsed]));
      } catch (err) {
        console.error("Invalid JSON in", file.name);
      }
    }

    const summary = jsonData.map((b, i) => ({
      id: b.id || i,
      game: b.gameName || b.game || "?",
      amount: b.amount,
      payout: b.payout,
      currency: b.currency,
      createdAt: b.createdAt
    }));

    sessionStorage.setItem("betData", JSON.stringify({ summary }));
    onUpload(summary);

    if (user && user.token) {
      fetch("/api/upload-session", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.token}`,
        },
        body: JSON.stringify(summary),
      });
    }
  };

  return (
    <div className="mb-4">
      <input
        type="file"
        multiple
        accept=".json"
        onChange={handleFile}
        className="file:bg-blue-500 file:text-white file:px-4 file:py-1 file:rounded file:cursor-pointer"
      />
    </div>
  );
}
