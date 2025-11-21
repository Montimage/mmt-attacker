import { useEffect, useRef } from 'react'
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import Terminal from '../common/Terminal'

function AttackResults({ results, isRunning }) {
  const metricsRef = useRef(null)

  useEffect(() => {
    if (results && metricsRef.current) {
      // Scroll metrics into view when results appear
      metricsRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  }, [results])

  if (!results && !isRunning) {
    return null
  }

  return (
    <div className="space-y-6">
      {/* Terminal Output */}
      <div className="bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6">
        <h3 className="text-xl font-bold text-black mb-4 flex items-center">
          <span className="mr-2">Attack Output</span>
          {isRunning && (
            <span className="text-sm font-normal text-gray-600">(Running...)</span>
          )}
        </h3>

        <Terminal
          output={results?.timeline?.map(item => ({
            message: item.message,
            type: item.type,
            timestamp: null
          })) || []}
          height="h-80"
          autoScroll={true}
        />
      </div>

      {/* Metrics */}
      {results?.metrics && (
        <div ref={metricsRef} className="bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6">
          <h3 className="text-xl font-bold text-black mb-4">Attack Metrics</h3>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(results.metrics).map(([key, value]) => (
              <div
                key={key}
                className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4"
              >
                <div className="text-sm font-semibold text-gray-500 uppercase mb-1">
                  {key.replace(/([A-Z])/g, ' $1').trim()}
                </div>
                <div className="text-lg font-bold text-black">
                  {typeof value === 'boolean' ? (
                    value ? (
                      <span className="flex items-center text-green-900">
                        <CheckCircle className="w-5 h-5 mr-1" />
                        Yes
                      </span>
                    ) : (
                      <span className="flex items-center text-gray-600">
                        <XCircle className="w-5 h-5 mr-1" />
                        No
                      </span>
                    )
                  ) : typeof value === 'object' ? (
                    <pre className="text-xs overflow-x-auto">{JSON.stringify(value, null, 2)}</pre>
                  ) : (
                    value
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Success/Error Status */}
      {results && (
        <div className={`border-2 rounded-lg p-4 flex items-start space-x-3 ${
          results.success
            ? 'bg-green-50 border-green-700'
            : 'bg-gray-50 border-gray-600'
        }`}>
          {results.success ? (
            <CheckCircle className="w-6 h-6 text-green-900 flex-shrink-0 mt-0.5" />
          ) : (
            <AlertCircle className="w-6 h-6 text-gray-700 flex-shrink-0 mt-0.5" />
          )}
          <div>
            <h4 className={`font-bold mb-1 ${results.success ? 'text-green-900' : 'text-gray-900'}`}>
              {results.success ? 'Simulation Completed Successfully' : 'Simulation Failed'}
            </h4>
            <p className="text-sm text-gray-700">
              {results.success
                ? 'The attack simulation has completed. Review the output and metrics above for detailed results.'
                : results.error || 'An error occurred during the simulation.'}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default AttackResults
