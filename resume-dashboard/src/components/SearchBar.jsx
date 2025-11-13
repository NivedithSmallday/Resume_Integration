import React from "react";

export default function SearchBar({ value, onChange, placeholder }) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="p-2 border border-gray-300 rounded-lg shadow-sm flex-1"
    />
  );
}
