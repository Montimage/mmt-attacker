import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, AlertTriangle } from 'lucide-react'
import { getAttackById } from '../../data/attacksData'
import useAttackSimulation from '../../hooks/useAttackSimulation'
import Badge from '../../components/common/Badge'
import AttackTheory from '../../components/attack/AttackTheory'
import AttackFlow from '../../components/attack/AttackFlow'
import AttackScenario from '../../components/attack/AttackScenario'

function AttackPageTemplate() {
  const { attackId } = useParams()
  const attack = getAttackById(attackId)
  const { isExecuting, results, executeAttack, reset } = useAttackSimulation()

  if (!attack) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-black mb-4">Attack Not Found</h1>
          <p className="text-gray-600 mb-6">The requested attack type could not be found.</p>
          <Link to="/" className="text-green-900 hover:text-green-800 font-medium">
            ← Back to Home
          </Link>
        </div>
      </div>
    )
  }

  const handleExecute = (scenarioId, parameters) => {
    reset()
    executeAttack(attackId, scenarioId, parameters)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        to="/"
        className="inline-flex items-center space-x-2 text-gray-600 hover:text-green-900 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="font-medium">Back to Home</span>
      </Link>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-3">
          <h1 className="text-3xl md:text-4xl font-bold text-black">{attack.name}</h1>
          <Badge variant="primary">{attack.category}</Badge>
        </div>
        <p className="text-lg text-gray-600">{attack.description}</p>
      </div>

      {/* Content Sections */}
      <div className="space-y-8">
        {/* Attack Theory */}
        <AttackTheory theory={attack.theory} />

        {/* Attack Flow Diagram */}
        {attack.mermaidDiagram && (
          <AttackFlow diagram={attack.mermaidDiagram} title="Attack Flow" />
        )}

        {/* Key Features */}
        {attack.keyFeatures && attack.keyFeatures.length > 0 && (
          <div className="bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6">
            <h3 className="text-xl font-bold text-black mb-4">Key Features</h3>
            <ul className="grid md:grid-cols-2 gap-3">
              {attack.keyFeatures.map((feature, index) => (
                <li key={index} className="flex items-start">
                  <span className="text-green-900 font-bold mr-2">✓</span>
                  <span className="text-gray-700">{feature}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Attack Scenarios */}
        <div>
          <h2 className="text-2xl font-bold text-black mb-4">Attack Scenarios</h2>
          <AttackScenario
            attackId={attackId}
            scenarios={attack.scenarios}
            onExecute={handleExecute}
            isExecuting={isExecuting}
            results={results}
          />
        </div>

        {/* Safety Considerations */}
        {attack.safetyConsiderations && attack.safetyConsiderations.length > 0 && (
          <div className="bg-white border-2 border-gray-600 rounded-lg shadow-custom p-6">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="w-6 h-6 text-gray-700 flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-xl font-bold text-black mb-3">Safety Considerations</h3>
                <ul className="space-y-2">
                  {attack.safetyConsiderations.map((consideration, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-gray-700 mr-2">•</span>
                      <span className="text-gray-700">{consideration}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AttackPageTemplate
