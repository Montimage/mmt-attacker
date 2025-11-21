import { useState } from 'react'
import { ChevronDown, ChevronUp, BookOpen } from 'lucide-react'

function AttackTheory({ theory }) {
  const [isExpanded, setIsExpanded] = useState(true)

  if (!theory) return null

  return (
    <div className="bg-white border-2 border-gray-200 rounded-lg shadow-custom overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-6 hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center space-x-3">
          <BookOpen className="w-6 h-6 text-green-900" />
          <h3 className="text-xl font-bold text-black">Attack Theory</h3>
        </div>
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-gray-600" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-600" />
        )}
      </button>

      {/* Content */}
      {isExpanded && (
        <div className="px-6 pb-6 space-y-4 border-t-2 border-gray-200">
          {/* Description */}
          {theory.description && (
            <div>
              <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">Description</h4>
              <p className="text-gray-700 leading-relaxed">{theory.description}</p>
            </div>
          )}

          {/* Mechanism */}
          {theory.mechanism && (
            <div>
              <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">Mechanism</h4>
              <p className="text-gray-700 leading-relaxed">{theory.mechanism}</p>
            </div>
          )}

          {/* Impact */}
          {theory.impact && (
            <div>
              <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">Impact</h4>
              <p className="text-gray-700 leading-relaxed">{theory.impact}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default AttackTheory
