import React from "react";

export default function ResumesTable({ resumes }) {
  if (!resumes.length) {
    return <p className="text-gray-500">No resumes found.</p>;
  }

  return (
    <div className="overflow-x-auto shadow-lg rounded-lg border border-gray-200">
      <table className="min-w-full border-collapse bg-white">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-3 text-left text-sm font-semibold text-gray-600">Name</th>
            <th className="p-3 text-left text-sm font-semibold text-gray-600">Email</th>
            <th className="p-3 text-left text-sm font-semibold text-gray-600">Career Span</th>
            <th className="p-3 text-left text-sm font-semibold text-gray-600">Skills</th>
          </tr>
        </thead>
        <tbody>
          {resumes.map((resume, idx) => (
            <tr
              key={idx}
              className="hover:bg-gray-50 transition-colors border-t"
            >
              <td className="p-3 text-sm text-gray-800">{resume.name}</td>
              <td className="p-3 text-sm text-gray-600">{resume.email}</td>
              <td className="p-3 text-sm text-gray-600">{resume.career_span}</td>
              <td className="p-3 text-sm text-gray-600">{resume.skills}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
