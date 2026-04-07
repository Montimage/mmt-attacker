import { useRef, useEffect } from 'react'

function Terminal({
  output = [],
  height = 'h-64',
  className = '',
  autoScroll = true,
  ...props
}) {
  const terminalRef = useRef(null)

  useEffect(() => {
    if (autoScroll && terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [output, autoScroll])

  const getLineColor = (type) => {
    switch (type) {
      case 'success':
        return 'text-green-400'
      case 'error':
        return 'text-gray-300'
      case 'warning':
        return 'text-gray-400'
      case 'info':
      default:
        return 'text-white'
    }
  }

  return (
    <div
      ref={terminalRef}
      className={`bg-black text-white font-mono text-sm p-4 rounded-lg border-2 border-gray-800 overflow-auto ${height} ${className}`}
      {...props}
    >
      {output.length > 0 ? (
        output.map((line, index) => (
          <div key={index} className={`mb-1 ${getLineColor(line.type)}`}>
            {line.timestamp && (
              <span className="text-gray-500 mr-2">[{line.timestamp}]</span>
            )}
            {line.message}
          </div>
        ))
      ) : (
        <div className="text-gray-500">
          <span className="animate-pulse">▋</span> Waiting for output...
        </div>
      )}
    </div>
  )
}

export default Terminal
