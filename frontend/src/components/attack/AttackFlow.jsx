import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

// Initialize Mermaid with custom theme
mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#14532d',
    primaryTextColor: '#fff',
    primaryBorderColor: '#15803d',
    lineColor: '#4b5563',
    secondaryColor: '#f9fafb',
    tertiaryColor: '#e5e7eb',
    background: '#ffffff',
    mainBkg: '#ffffff',
    textColor: '#000000',
    fontSize: '14px',
  },
  flowchart: {
    htmlLabels: true,
    curve: 'basis',
  },
  sequence: {
    diagramMarginX: 50,
    diagramMarginY: 10,
    actorMargin: 50,
    width: 150,
    height: 65,
    boxMargin: 10,
    boxTextMargin: 5,
    noteMargin: 10,
    messageMargin: 35,
  },
})

function AttackFlow({ diagram, title, className = '' }) {
  const mermaidRef = useRef(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!diagram) {
      setLoading(false)
      return
    }

    const renderDiagram = async () => {
      try {
        setLoading(true)
        setError(null)

        // Generate unique ID for this diagram
        const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`

        // Render the diagram
        const { svg } = await mermaid.render(id, diagram)

        if (mermaidRef.current) {
          mermaidRef.current.innerHTML = svg
        }

        setLoading(false)
      } catch (err) {
        console.error('Mermaid rendering error:', err)
        setError('Failed to render diagram')
        setLoading(false)
      }
    }

    renderDiagram()
  }, [diagram])

  if (loading) {
    return (
      <div className={`bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6 ${className}`}>
        {title && <h3 className="text-xl font-bold text-black mb-4">{title}</h3>}
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <svg className="animate-spin h-10 w-10 text-green-900 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="mt-4 text-gray-600">Rendering diagram...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={`bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6 ${className}`}>
        {title && <h3 className="text-xl font-bold text-black mb-4">{title}</h3>}
        <div className="bg-gray-50 border-2 border-gray-300 rounded-lg p-4">
          <p className="text-gray-700">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6 ${className}`}>
      {title && <h3 className="text-xl font-bold text-black mb-4">{title}</h3>}
      <div
        ref={mermaidRef}
        className="flex justify-center items-center overflow-auto"
      />
    </div>
  )
}

export default AttackFlow
