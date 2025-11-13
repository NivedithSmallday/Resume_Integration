import React, { useState } from "react";

export default function ResumesTable({ resumes, newResumeIds }) {
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  const [hoveredRow, setHoveredRow] = useState(null);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const sortedResumes = [...resumes].sort((a, b) => {
    if (!sortField) return 0;

    let aVal = a[sortField];
    let bVal = b[sortField];

    if (sortField === 'skills') {
      aVal = a.skills?.join(', ') || '';
      bVal = b.skills?.join(', ') || '';
    }

    if (sortField === 'career_span') {
      aVal = parseInt(aVal) || 0;
      bVal = parseInt(bVal) || 0;
    }

    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase();
      bVal = bVal?.toLowerCase() || '';
    }

    if (sortDirection === 'asc') {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  const SortIcon = ({ field }) => {
    if (sortField !== field) {
      return <span className="text-gray-400 ml-1">↕️</span>;
    }
    return (
      <span className="text-blue-600 ml-1">
        {sortDirection === 'asc' ? '↑' : '↓'}
      </span>
    );
  };

  const SkillTag = ({ skill }) => (
    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-1 mb-1 font-medium">
      {skill}
    </span>
  );

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white">
        <thead className="bg-gradient-to-r from-blue-50 to-indigo-50">
          <tr>
            <th
              className="px-6 py-4 text-left text-sm font-semibold text-gray-700 cursor-pointer hover:bg-blue-100 transition-colors duration-200 select-none"
              onClick={() => handleSort('name')}
            >
              <div className="flex items-center">
                👤 Name
                <SortIcon field="name" />
              </div>
            </th>
            <th
              className="px-6 py-4 text-left text-sm font-semibold text-gray-700 cursor-pointer hover:bg-blue-100 transition-colors duration-200 select-none"
              onClick={() => handleSort('email')}
            >
              <div className="flex items-center">
                📧 Email
                <SortIcon field="email" />
              </div>
            </th>
            <th
              className="px-6 py-4 text-left text-sm font-semibold text-gray-700 cursor-pointer hover:bg-blue-100 transition-colors duration-200 select-none"
              onClick={() => handleSort('phone')}
            >
              <div className="flex items-center">
                📞 Phone
                <SortIcon field="phone" />
              </div>
            </th>
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
              🔗 LinkedIn
            </th>
            <th
              className="px-6 py-4 text-left text-sm font-semibold text-gray-700 cursor-pointer hover:bg-blue-100 transition-colors duration-200 select-none"
              onClick={() => handleSort('career_span')}
            >
              <div className="flex items-center">
                ⏱️ Experience
                <SortIcon field="career_span" />
              </div>
            </th>
            {/*<th*/}
            {/*  className="px-6 py-4 text-left text-sm font-semibold text-gray-700 cursor-pointer hover:bg-blue-100 transition-colors duration-200 select-none"*/}
            {/*  onClick={() => handleSort('skills')}*/}
            {/*>*/}
            {/*  <div className="flex items-center">*/}
            {/*    🛠️ Skills*/}
            {/*    <SortIcon field="skills" />*/}
            {/*  </div>*/}
            {/*</th>*/}gu
            <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
              📄 Resume
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {sortedResumes.map((resume, index) => (
            <tr
              key={resume.id}
              className={`
                transition-all duration-300 transform
                ${newResumeIds.includes(resume.id) 
                  ? "bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-400 shadow-md scale-[1.01]" 
                  : hoveredRow === index 
                    ? "bg-gradient-to-r from-blue-50 to-indigo-50 shadow-lg scale-[1.005]" 
                    : "hover:bg-gray-50"
                }
              `}
              onMouseEnter={() => setHoveredRow(index)}
              onMouseLeave={() => setHoveredRow(null)}
            >
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  {newResumeIds.includes(resume.id) && (
                    <div className="mr-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 animate-pulse">
                        ✨ New
                      </span>
                    </div>
                  )}
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      {resume.name || 'N/A'}
                    </div>
                  </div>
                </div>
              </td>

              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {resume.email ? (
                    <a
                      href={`mailto:${resume.email}`}
                      className="text-blue-600 hover:text-blue-800 hover:underline transition-colors duration-200"
                    >
                      {resume.email}
                    </a>
                  ) : (
                    <span className="text-gray-400">No email</span>
                  )}
                </div>
              </td>

              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {resume.phone ? (
                    <a
                      href={`tel:${resume.phone}`}
                      className="text-blue-600 hover:text-blue-800 hover:underline transition-colors duration-200"
                    >
                      {resume.phone}
                    </a>
                  ) : (
                    <span className="text-gray-400">No phone</span>
                  )}
                </div>
              </td>

              <td className="px-6 py-4 whitespace-nowrap">
                {resume.linkedin ? (
                  <a
                    href={resume.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg text-sm font-medium transition-all duration-200 transform hover:scale-105 shadow-sm"
                  >
                    <span>🔗</span>
                    LinkedIn
                  </a>
                ) : (
                  <span className="text-gray-400 italic">Not provided</span>
                )}
              </td>

              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  {resume.career_span ? (
                    <div className="flex items-center gap-2">
                      <div className="bg-gradient-to-r from-purple-100 to-pink-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                        {resume.career_span} {resume.career_span === 1 ? 'year' : 'years'}
                      </div>
                    </div>
                  ) : (
                    <span className="text-gray-400">Not specified</span>
                  )}
                </div>
              </td>

                <td className="px-6 py-4 whitespace-nowrap">
                  {resume.resume_file ? (
                    <div className="flex gap-2">
                      <a
                        href={resume.resume_file}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 bg-blue-500 hover:bg-blue-600
                                   text-white px-4 py-2 rounded-lg text-sm font-medium
                                   transition-all duration-200 transform hover:scale-105 shadow"
                      >
                        👀 View
                      </a>
                      <a
                      href={`http://localhost:5000/api/resumes/${resume.id}/download`}
                      className="inline-flex items-center gap-2 bg-gradient-to-r from-green-500 to-emerald-500
                                 hover:from-green-600 hover:to-emerald-600 text-white px-4 py-2 rounded-lg
                                 text-sm font-medium transition-all duration-200 transform hover:scale-105
                                 shadow-lg hover:shadow-xl"
                    >
                      ⬇️ Download Resume
                    </a>
                    </div>
                  ) : (
                    <div className="inline-flex items-center gap-2 bg-gray-100 text-gray-500 px-4 py-2 rounded-lg text-sm">
                      <span>📄</span> No File
                    </div>
                  )}
                </td>


              {/*<td className="px-6 py-4">*/}
              {/*  <div className="max-w-xs">*/}
              {/*    {resume.skills && resume.skills.length > 0 ? (*/}
              {/*      <div className="flex flex-wrap gap-1">*/}
              {/*        {resume.skills.slice(0, 3).map((skill, skillIndex) => (*/}
              {/*          <SkillTag key={skillIndex} skill={skill} />*/}
              {/*        ))}*/}
              {/*        {resume.skills.length > 3 && (*/}
              {/*          <span className="inline-block bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full font-medium">*/}
              {/*            +{resume.skills.length - 3} more*/}
              {/*          </span>*/}
              {/*        )}*/}
              {/*      </div>*/}
              {/*    ) : (*/}
              {/*      <span className="text-gray-400 italic">No skills listed</span>*/}
              {/*    )}*/}
              {/*  </div>*/}
              {/*</td>*/}

{/*              <td className="px-6 py-4 whitespace-nowrap">*/}
{/*  {resume.resume_file ? (*/}
{/*    // <a*/}
{/*    //   href={resume.resume_file}*/}
{/*    //   download // 👈 this makes it download instead of view*/}
{/*    //   className="inline-flex items-center gap-2 bg-gradient-to-r from-green-500 to-emerald-500*/}
{/*    //              hover:from-green-600 hover:to-emerald-600 text-white px-4 py-2 rounded-lg*/}
{/*    //              text-sm font-medium transition-all duration-200 transform hover:scale-105*/}
{/*    //              shadow-lg hover:shadow-xl"*/}
{/*    // >*/}
{/*    //   <span>⬇️</span>*/}
{/*    //   Download Resume*/}
{/*    // </a>*/}
{/*      <a*/}
{/*  href={resume.resume_file}*/}
{/*  download*/}
{/*  className="inline-flex items-center gap-2 bg-gradient-to-r from-green-500 to-emerald-500*/}
{/*             hover:from-green-600 hover:to-emerald-600 text-white px-4 py-2 rounded-lg*/}
{/*             text-sm font-medium transition-all duration-200 transform hover:scale-105*/}
{/*             shadow-lg hover:shadow-xl"*/}
{/*>*/}
{/*  ⬇️ Download Resume*/}
{/*</a>*/}

{/*  ) : (*/}
{/*    <div className="inline-flex items-center gap-2 bg-gray-100 text-gray-500 px-4 py-2 rounded-lg text-sm">*/}
{/*      <span>📄</span>*/}
{/*      No File*/}
{/*    </div>*/}
{/*  )}*/}
{/*</td>*/}

            </tr>
          ))}
        </tbody>
      </table>

      {/* Table Footer with Stats */}
      {sortedResumes.length > 0 && (
        <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <div>
              Showing {sortedResumes.length} resume{sortedResumes.length !== 1 ? 's' : ''}
            </div>
            <div>
              {newResumeIds.length > 0 && (
                <span className="inline-flex items-center gap-1 text-green-600 font-medium">
                  <span>✨</span>
                  {newResumeIds.length} new resume{newResumeIds.length !== 1 ? 's' : ''}
                </span>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}