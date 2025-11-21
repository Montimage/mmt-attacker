import { Activity, Info, Lightbulb } from 'lucide-react'

function AttackExplanation({ explanation }) {
  if (!explanation) return null

  return (
    <div className="space-y-6">
      {/* What's Happening */}
      {explanation.happening && (
        <div className="bg-white border-2 border-green-900 rounded-lg shadow-custom p-6">
          <div className="flex items-start space-x-3">
            <div className="bg-green-50 p-2 rounded-lg border-2 border-green-900">
              <Activity className="w-6 h-6 text-green-900" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-black mb-3">What's Happening</h3>
              <p className="text-gray-700 leading-relaxed">{explanation.happening}</p>
            </div>
          </div>
        </div>
      )}

      {/* Key Highlights */}
      {explanation.highlights && explanation.highlights.length > 0 && (
        <div className="bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6">
          <div className="flex items-start space-x-3">
            <div className="bg-gray-50 p-2 rounded-lg border-2 border-gray-300">
              <Lightbulb className="w-6 h-6 text-gray-700" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-black mb-3">Key Highlights</h3>
              <ul className="space-y-2">
                {explanation.highlights.map((highlight, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-green-900 font-bold mr-3 text-lg">•</span>
                    <span className="text-gray-700 flex-1">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Result Interpretation */}
      {explanation.interpretation && (
        <div className="bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6">
          <div className="flex items-start space-x-3">
            <div className="bg-gray-50 p-2 rounded-lg border-2 border-gray-300">
              <Info className="w-6 h-6 text-gray-700" />
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-black mb-3">Result Interpretation</h3>
              <p className="text-gray-700 leading-relaxed">{explanation.interpretation}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AttackExplanation
