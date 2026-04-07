import { X } from 'lucide-react'
import { useEffect } from 'react'
import AttackResults from './AttackResults'

function ResultsModal({ isOpen, onClose, results, isRunning }) {
  // Handle ESC key to close modal
  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === 'Escape' && isOpen) {
        onClose()
      }
    }
    window.addEventListener('keydown', handleEsc)
    return () => window.removeEventListener('keydown', handleEsc)
  }, [isOpen, onClose])

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal Content */}
      <div className="relative bg-white rounded-lg shadow-custom-xl max-w-6xl w-full max-h-[90vh] overflow-hidden border-2 border-gray-400 animate-slide-up">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b-2 border-gray-300 bg-gray-50">
          <h2 className="text-2xl font-bold text-black">Attack Simulation Results</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-200 transition-colors border-2 border-gray-300 hover:border-black"
            aria-label="Close modal"
          >
            <X className="w-6 h-6 text-black" />
          </button>
        </div>

        {/* Results Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-88px)]">
          <AttackResults results={results} isRunning={isRunning} />
        </div>

        {/* Footer */}
        <div className="flex justify-end p-6 border-t-2 border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-black text-white font-semibold rounded-lg hover:bg-gray-800 transition-colors border-2 border-black shadow-custom-md hover:shadow-custom-lg"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default ResultsModal
