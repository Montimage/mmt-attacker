import { useState } from 'react'
import { Eye } from 'lucide-react'
import AttackParameters from './AttackParameters'
import Button from '../common/Button'
import CommandDisplay from './CommandDisplay'
import ResultsModal from './ResultsModal'

function AttackScenario({ attackId, scenarios, onExecute, isExecuting, results }) {
  const [activeScenario, setActiveScenario] = useState(0)
  const [activeTab, setActiveTab] = useState('configure') // 'configure' or 'command'
  const [parameters, setParameters] = useState({})
  const [errors, setErrors] = useState({})
  const [isModalOpen, setIsModalOpen] = useState(false)

  const currentScenario = scenarios[activeScenario]

  const handleParameterChange = (name, value, error) => {
    setParameters(prev => ({
      ...prev,
      [name]: value
    }))

    if (error) {
      setErrors(prev => ({
        ...prev,
        [name]: error
      }))
    } else {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }

  const handleExecute = () => {
    // Validate all required fields, considering default values
    const newErrors = {}
    currentScenario.parameters.forEach(param => {
      const value = parameters[param.name] !== undefined ? parameters[param.name] : param.defaultValue
      if (param.required && !value) {
        newErrors[param.name] = `${param.label} is required`
      }
    })

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    // Merge parameters with default values for execution
    const finalParameters = {}
    currentScenario.parameters.forEach(param => {
      finalParameters[param.name] = parameters[param.name] !== undefined
        ? parameters[param.name]
        : param.defaultValue
    })

    // Execute the attack and open modal
    onExecute(currentScenario.id, finalParameters)
    setIsModalOpen(true)
  }

  return (
    <div className="bg-white border-2 border-gray-200 rounded-lg shadow-custom">
      {/* Scenario Tabs */}
      {scenarios.length > 1 && (
        <div className="flex border-b-2 border-gray-200 overflow-x-auto">
          {scenarios.map((scenario, index) => (
            <button
              key={scenario.id}
              onClick={() => {
                setActiveScenario(index)
                setParameters({})
                setErrors({})
                setActiveTab('configure')
              }}
              className={`flex-1 px-6 py-4 font-medium text-sm transition-colors whitespace-nowrap ${
                activeScenario === index
                  ? 'bg-green-900 text-white border-b-4 border-green-900'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              {scenario.name}
            </button>
          ))}
        </div>
      )}

      {/* Scenario Content */}
      <div className="p-6">
        {/* Scenario Description */}
        <div className="mb-6">
          <h3 className="text-xl font-bold text-black mb-2">{currentScenario.name}</h3>
          {currentScenario.description && (
            <p className="text-gray-600">{currentScenario.description}</p>
          )}
        </div>

        {/* Sub-Tabs: Configure | Python Command */}
        <div className="mb-6">
          <div className="flex border-b border-gray-300">
            <button
              onClick={() => setActiveTab('configure')}
              className={`px-6 py-3 font-medium text-sm transition-colors ${
                activeTab === 'configure'
                  ? 'text-green-900 border-b-2 border-green-900'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Configure
            </button>
            <button
              onClick={() => setActiveTab('command')}
              className={`px-6 py-3 font-medium text-sm transition-colors ${
                activeTab === 'command'
                  ? 'text-green-900 border-b-2 border-green-900'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Python Command
            </button>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'configure' ? (
          <>
            {/* Parameters Form */}
            <AttackParameters
              parameters={currentScenario.parameters}
              values={parameters}
              onChange={handleParameterChange}
              errors={errors}
            />

            {/* Execute Button */}
            <div className="mt-6 pt-6 border-t-2 border-gray-200">
              <div className="flex flex-wrap gap-3">
                <Button
                  variant="primary"
                  onClick={handleExecute}
                  disabled={isExecuting}
                  loading={isExecuting}
                  className="flex-1 md:flex-initial"
                >
                  {isExecuting ? 'Running Simulation...' : 'Start Attack Simulation'}
                </Button>

                {results && (
                  <Button
                    variant="secondary"
                    onClick={() => setIsModalOpen(true)}
                    className="flex-1 md:flex-initial inline-flex items-center justify-center"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    <span>Show Results</span>
                  </Button>
                )}
              </div>
              {Object.keys(errors).length > 0 && (
                <p className="mt-2 text-sm text-red-600">
                  Please fix the errors above before starting the simulation.
                </p>
              )}
            </div>
          </>
        ) : (
          /* Python Command Display */
          <CommandDisplay
            attackId={attackId}
            scenario={currentScenario}
            parameterValues={parameters}
          />
        )}
      </div>

      {/* Results Modal */}
      <ResultsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        results={results}
        isRunning={isExecuting}
      />
    </div>
  )
}

export default AttackScenario
