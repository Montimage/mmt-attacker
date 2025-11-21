import { useState, useCallback } from 'react'
import { simulateAttack } from '../data/simulationEngine'

/**
 * Custom hook for managing attack simulation state
 */
function useAttackSimulation() {
  const [isExecuting, setIsExecuting] = useState(false)
  const [results, setResults] = useState(null)
  const [currentTimeline, setCurrentTimeline] = useState([])

  /**
   * Execute an attack simulation
   */
  const executeAttack = useCallback(async (attackId, scenarioId, parameters) => {
    setIsExecuting(true)
    setResults(null)
    setCurrentTimeline([])

    try {
      // Run the simulation
      const simulationResults = await simulateAttack(attackId, scenarioId, parameters)

      if (simulationResults.success && simulationResults.timeline) {
        // Animate timeline events
        for (let i = 0; i < simulationResults.timeline.length; i++) {
          const event = simulationResults.timeline[i]

          // Wait for the event time
          if (i > 0) {
            const previousTime = simulationResults.timeline[i - 1].time
            const delay = event.time - previousTime
            await new Promise(resolve => setTimeout(resolve, delay))
          } else {
            await new Promise(resolve => setTimeout(resolve, event.time))
          }

          // Add event to current timeline
          setCurrentTimeline(prev => [...prev, event])
        }

        // Set final results
        setResults(simulationResults)
      } else {
        // Simulation failed
        setResults(simulationResults)
      }
    } catch (error) {
      console.error('Simulation error:', error)
      setResults({
        success: false,
        error: error.message || 'An unexpected error occurred during simulation'
      })
    } finally {
      setIsExecuting(false)
    }
  }, [])

  /**
   * Reset simulation state
   */
  const reset = useCallback(() => {
    setIsExecuting(false)
    setResults(null)
    setCurrentTimeline([])
  }, [])

  return {
    isExecuting,
    results: results ? { ...results, timeline: currentTimeline } : null,
    executeAttack,
    reset
  }
}

export default useAttackSimulation
