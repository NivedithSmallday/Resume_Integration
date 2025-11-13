import React from "react";

export default function Notification({ message }) {
  if (!message) return null;
  return (
    <div className="mb-4 px-4 py-2 bg-blue-100 text-blue-800 rounded shadow">
      {message}
    </div>
  );
}