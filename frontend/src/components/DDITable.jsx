import React from 'react';

/**
 * DDITable
 * Visualizes DDI summary and ADR flags in a color-coded table.
 * Props: { ddi_summary: array, adr_flags: array }
 */
export default function DDITable({ ddi_summary = [], adr_flags = [] }) {
  // Normalize different possible response shapes from API or mock data
  console.log('DDITable props:', { ddi_summary, adr_flags });

  // If ddi_summary was sent as an object with different keys, try common alternatives
  let interactions = [];
  if (Array.isArray(ddi_summary)) {
    interactions = ddi_summary;
  } else if (ddi_summary && typeof ddi_summary === 'object') {
    if (Array.isArray(ddi_summary.interactions)) interactions = ddi_summary.interactions;
    else if (Array.isArray(ddi_summary.ddi)) interactions = ddi_summary.ddi;
    else if (Array.isArray(ddi_summary.data)) interactions = ddi_summary.data;
  }

  const hasDDI = interactions.length > 0;
  const hasADR = Array.isArray(adr_flags) && adr_flags.length > 0;

  // Always render a card so the section is visible; show a friendly message when empty
  return (
    <div className="my-8 p-6 bg-white rounded-xl shadow-lg border border-gray-100">
      <h2 className="text-xl font-bold mb-4 text-gray-800 flex items-center gap-2">
        <span className="w-2 h-2 bg-red-500 rounded-full"></span>
        Drug–Drug Interactions (DDI) & Adverse Drug Reactions (ADR)
      </h2>

      {hasDDI ? (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Drug Interactions</h3>
          <div className="overflow-x-auto rounded-lg border border-gray-200">
            <table className="min-w-full bg-white">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Drug 1</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Drug 2</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Interaction</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">Severity</th>
                </tr>
              </thead>
              <tbody>
                {interactions.map((ddi, i) => {
                  const severity = ddi.severity || ddi.level || (ddi.risk && ddi.risk.toUpperCase()) || 'UNKNOWN';

                  const severityColors = {
                    'CRITICAL': 'bg-red-50 border-l-4 border-red-500',
                    'HIGH': 'bg-orange-50 border-l-4 border-orange-500',
                    'MOD': 'bg-yellow-50 border-l-4 border-yellow-500',
                    'MODERATE': 'bg-yellow-50 border-l-4 border-yellow-500',
                    'LOW': 'bg-green-50 border-l-4 border-green-500'
                  };

                  const severityTextColors = {
                    'CRITICAL': 'text-red-700',
                    'HIGH': 'text-orange-700',
                    'MOD': 'text-yellow-700',
                    'MODERATE': 'text-yellow-700',
                    'LOW': 'text-green-700'
                  };

                  const bgClass = severityColors[severity] || 'bg-gray-50';
                  const textClass = severityTextColors[severity] || 'text-gray-700';

                  // Support different field names
                  const drug1 = ddi.drug1 || ddi.nameA || ddi.drug_a || ddi.primary || '—';
                  const drug2 = ddi.drug2 || ddi.nameB || ddi.drug_b || ddi.secondary || '—';
                  const interactionText = ddi.interaction || ddi.description || ddi.note || 'No details available';

                  return (
                    <tr key={i} className={`${bgClass} hover:bg-opacity-75 transition-colors`}>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{drug1}</td>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">{drug2}</td>
                      <td className="px-4 py-3 text-sm text-gray-700">{interactionText}</td>
                      <td className={`px-4 py-3 text-sm font-bold ${textClass}`}>
                        <span className="px-2 py-1 rounded-full text-xs font-semibold bg-white">
                          {severity}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="text-sm text-gray-600 py-4 border border-dashed border-gray-200 rounded-md px-4">
          No significant drug–drug interactions found.
        </div>
      )}

      {hasADR && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Adverse Drug Reaction Flags</h3>
          <div className="bg-pink-50 border border-pink-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-pink-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-white text-xs font-bold">!</span>
              </div>
              <div>
                <p className="text-pink-800 font-semibold text-sm mb-2">
                  Warning: Potential Adverse Drug Reactions Detected
                </p>
                <ul className="text-pink-700 text-sm space-y-1">
                  {adr_flags.map((flag, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 bg-pink-500 rounded-full mt-1.5"></span>
                      {typeof flag === 'string' ? (
                        <span>{flag}</span>
                      ) : (
                        <div>
                          <span className="font-medium">{flag.drug || flag.name || 'Unknown'}</span>
                          {flag.reaction && <span>: {flag.reaction}</span>}
                          {flag.severity && <span className="ml-2 px-2 py-1 bg-pink-200 rounded text-xs">{flag.severity}</span>}
                          {flag.management && <div className="text-xs text-pink-600 mt-1">Management: {flag.management}</div>}
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
