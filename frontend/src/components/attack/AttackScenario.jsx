import { useState } from 'react'
import AttackParameters from './AttackParameters'
import Button from '../common/Button'

function AttackScenario({ scenarios, onExecute, isExecuting }) {
  const [activeScenario, setActiveScenario] = useState(0)
  const [parameters, setParameters] = useState({})
  const [errors, setErrors] = useState({})

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
    // Validate all required fields
    const newErrors = {}
    currentScenario.parameters.forEach(param => {
      if (param.required && !parameters[param.name]) {
        newErrors[param.name] = `${param.label} is required`
      }
    })

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    // Execute the attack
    onExecute(currentScenario.id, parameters)
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

        {/* Parameters Form */}
        <AttackParameters
          parameters={currentScenario.parameters}
          values={parameters}
          onChange={handleParameterChange}
          errors={errors}
        />

        {/* Execute Button */}
        <div className="mt-6 pt-6 border-t-2 border-gray-200">
          <Button
            variant="primary"
            onClick={handleExecute}
            disabled={isExecuting}
            loading={isExecuting}
            className="w-full md:w-auto"
          >
            {isExecuting ? 'Running Simulation...' : 'Start Attack Simulation'}
          </Button>
          {Object.keys(errors).length > 0 && (
            <p className="mt-2 text-sm text-red-600">
              Please fix the errors above before starting the simulation.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default AttackScenario
