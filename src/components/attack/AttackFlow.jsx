import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

// Initialize Mermaid with dark theme
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#1f2937',
    primaryTextColor: '#f3f4f6',
    primaryBorderColor: '#15803d',
    lineColor: '#9ca3af',
    secondaryColor: '#111827',
    tertiaryColor: '#374151',
    background: '#111827',
    mainBkg: '#1f2937',
    secondaryBkg: '#1f2937',
    tertiaryBkg: '#111827',
    textColor: '#f3f4f6',
    secondaryTextColor: '#f3f4f6',
    tertiaryTextColor: '#f3f4f6',
    actorTextColor: '#f3f4f6',
    actorBkg: '#1f2937',
    actorBorder: '#15803d',
    labelTextColor: '#f3f4f6',
    labelBoxBkgColor: '#111827',
    labelBoxBorderColor: '#6b7280',
    noteBkgColor: '#451a03',
    noteTextColor: '#f3f4f6',
    noteBorderColor: '#f59e0b',
    nodeTextColor: '#f3f4f6',
    clusterBkg: '#1f2937',
    clusterBorder: '#6b7280',
    fontSize: '16px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  flowchart: {
    htmlLabels: true,
    curve: 'basis',
    padding: 15,
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
    actorFontSize: 16,
    actorFontWeight: 600,
    messageFontSize: 14,
    messageFontWeight: 400,
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

        console.log('Rendering mermaid diagram...', diagram.substring(0, 50))

        // Wait for next tick to ensure ref is attached
        await new Promise(resolve => setTimeout(resolve, 0))

        if (!mermaidRef.current) {
          console.error('mermaidRef.current is null after waiting')
          setError('Failed to attach diagram container')
          setLoading(false)
          return
        }

        // Generate unique ID for this diagram
        const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`

        // Render the diagram
        const { svg } = await mermaid.render(id, diagram)

        console.log('Mermaid SVG generated successfully, length:', svg.length)

        if (mermaidRef.current) {
          mermaidRef.current.innerHTML = svg
          console.log('SVG injected into DOM')
        } else {
          console.error('mermaidRef.current is null after render')
        }

        setLoading(false)
      } catch (err) {
        console.error('Mermaid rendering error:', err)
        console.error('Diagram content:', diagram)
        setError(`Failed to render diagram: ${err.message}`)
        setLoading(false)
      }
    }

    renderDiagram()
  }, [diagram])

  return (
    <div className={`bg-gray-900 border-2 border-gray-700 rounded-lg shadow-custom p-6 ${className}`}>
      {title && <h3 className="text-xl font-bold text-gray-100 mb-4">{title}</h3>}
      <div className="relative">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-90 z-10 min-h-[300px]">
            <div className="text-center">
              <svg className="animate-spin h-10 w-10 text-green-400 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p className="mt-4 text-gray-400">Rendering diagram...</p>
            </div>
          </div>
        )}
        {error && (
          <div className="bg-gray-900 border-2 border-gray-600 rounded-lg p-4 min-h-[300px] flex items-center justify-center">
            <p className="text-gray-300">{error}</p>
          </div>
        )}
        <div
          ref={mermaidRef}
          className="flex justify-center items-center overflow-auto min-h-[300px] w-full mermaid-container"
          style={{ minHeight: '300px', visibility: loading || error ? 'hidden' : 'visible' }}
        />
      </div>
      <style>{`
        .mermaid-container svg {
          max-width: 100%;
          height: auto;
          display: block;
          margin: 0 auto;
        }

        /* Flowchart nodes */
        .mermaid-container .node rect,
        .mermaid-container .node circle,
        .mermaid-container .node ellipse,
        .mermaid-container .node polygon,
        .mermaid-container .node path {
          fill: #1f2937 !important;
          stroke: #15803d !important;
          stroke-width: 2px !important;
        }

        /* Sequence diagram actors */
        .mermaid-container .actor {
          fill: #1f2937 !important;
          stroke: #15803d !important;
          stroke-width: 2px !important;
        }
        .mermaid-container .actor-line {
          stroke: #6b7280 !important;
        }

        /* All text elements - force light color */
        .mermaid-container text,
        .mermaid-container .messageText,
        .mermaid-container .labelText,
        .mermaid-container .actor-label,
        .mermaid-container .nodeLabel,
        .mermaid-container .label,
        .mermaid-container span,
        .mermaid-container foreignObject div,
        .mermaid-container tspan {
          fill: #f3f4f6 !important;
          color: #f3f4f6 !important;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
          font-size: 14px !important;
          font-weight: 500 !important;
        }

        /* Edge labels */
        .mermaid-container .edgeLabel {
          background-color: #111827 !important;
          color: #f3f4f6 !important;
        }
        .mermaid-container .edgeLabel span {
          color: #f3f4f6 !important;
        }
        .mermaid-container .labelBox {
          fill: #111827 !important;
          stroke: #6b7280 !important;
        }

        /* Decision nodes */
        .mermaid-container .node.decision rect,
        .mermaid-container .node.decision polygon {
          fill: #451a03 !important;
          stroke: #f59e0b !important;
        }
      `}</style>
    </div>
  )
}

export default AttackFlow
