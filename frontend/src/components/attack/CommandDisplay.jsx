/**
 * CommandDisplay Component
 * Displays generated Python CLI command with copy functionality
 */

import React, { useState } from 'react'
import { generatePythonCommand, getParameterMapping } from '../../utils/commandGenerator'

const CommandDisplay = ({ attackId, scenario, parameterValues }) => {
  const [copied, setCopied] = useState(false)

  // Generate the command
  const command = generatePythonCommand(attackId, scenario, parameterValues)

  // Get parameter mapping for reference
  const paramMapping = getParameterMapping(scenario)

  /**
   * Copy command to clipboard
   */
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(command)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <div className="space-y-6">
      {/* Command Display */}
      <div>
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg font-semibold text-gray-800">Python Command</h3>
          <button
            onClick={handleCopy}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              copied
                ? 'bg-green-600 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            {copied ? (
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Copied!
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Copy Command
              </span>
            )}
          </button>
        </div>

        {/* Command Code Block */}
        <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
          <pre className="text-green-400 font-mono text-sm whitespace-pre-wrap break-all">
            {command}
          </pre>
        </div>

        {/* Usage Note */}
        <div className="mt-3 text-sm text-gray-600 flex items-start gap-2">
          <svg className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p>
            Run this command from the mmt-attacker root directory. Make sure you have activated
            your Python virtual environment and installed all requirements.
          </p>
        </div>
      </div>

      {/* Parameter Mapping Reference */}
      {paramMapping.length > 0 && (
        <div>
          <h4 className="text-md font-semibold text-gray-800 mb-3">Parameter Reference</h4>
          <div className="bg-gray-50 rounded-lg p-4 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-300">
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">UI Parameter</th>
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">CLI Argument</th>
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">Type</th>
                  <th className="text-left py-2 px-3 font-semibold text-gray-700">Required</th>
                </tr>
              </thead>
              <tbody>
                {paramMapping.map((param, index) => (
                  <tr key={index} className="border-b border-gray-200 hover:bg-gray-100">
                    <td className="py-2 px-3 text-gray-800">{param.uiName}</td>
                    <td className="py-2 px-3 font-mono text-blue-600">{param.cliArg}</td>
                    <td className="py-2 px-3 text-gray-600">
                      <span className="px-2 py-1 bg-gray-200 rounded text-xs">
                        {param.type}
                      </span>
                    </td>
                    <td className="py-2 px-3">
                      {param.required ? (
                        <span className="text-red-600 font-semibold">Yes</span>
                      ) : (
                        <span className="text-gray-400">No</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Additional Notes */}
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
        <div className="flex items-start gap-2">
          <svg className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h5 className="font-semibold text-yellow-800 mb-1">Important Notes</h5>
            <ul className="text-sm text-yellow-700 space-y-1 list-disc list-inside">
              <li>Many attacks require root/administrator privileges. Use <code className="bg-yellow-100 px-1 rounded">sudo</code> if needed.</li>
              <li>Only run attacks in authorized testing environments.</li>
              <li>Review the safety considerations before executing any attack.</li>
              <li>Monitor system resources during attack execution.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CommandDisplay
