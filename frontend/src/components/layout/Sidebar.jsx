import { Link, useLocation } from 'react-router-dom'
import { ChevronDown, ChevronRight, Shield, Home } from 'lucide-react'
import { useState } from 'react'
import { getCategories, getAttacksByCategory } from '../../data/attacksData'

function Sidebar({ isOpen, onClose }) {
  const location = useLocation()
  const categories = getCategories()
  const [expandedCategories, setExpandedCategories] = useState(
    // Expand all categories by default
    categories.reduce((acc, cat) => ({ ...acc, [cat]: true }), {})
  )

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }))
  }

  const isActiveAttack = (attackId) => {
    return location.pathname === `/attacks/${attackId}`
  }

  const categoryDisplayNames = {
    'Network-Layer': 'Network Layer',
    'Application-Layer': 'Application Layer',
    'Amplification': 'Amplification',
    'Credential': 'Credential Attacks',
    'Other': 'Other Attacks'
  }

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:sticky top-16 left-0 h-[calc(100vh-4rem)] w-64 bg-white border-r-2 border-gray-200 shadow-custom overflow-y-auto z-50 transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-4">
          {/* Home Link */}
          <Link
            to="/"
            onClick={onClose}
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg mb-4 transition-colors ${
              location.pathname === '/'
                ? 'bg-green-900 text-white'
                : 'hover:bg-gray-100 text-gray-700'
            }`}
          >
            <Home className="w-5 h-5" />
            <span className="font-medium">Home</span>
          </Link>

          {/* Attack Categories */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2 px-4 py-2 text-sm font-semibold text-gray-500 uppercase">
              <Shield className="w-4 h-4" />
              <span>Attack Types</span>
            </div>

            {categories.map(category => {
              const attacks = getAttacksByCategory(category)
              const isExpanded = expandedCategories[category]

              return (
                <div key={category} className="mb-2">
                  {/* Category Header */}
                  <button
                    onClick={() => toggleCategory(category)}
                    className="w-full flex items-center justify-between px-4 py-2 text-left font-medium text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <span className="text-sm">{categoryDisplayNames[category] || category}</span>
                    {isExpanded ? (
                      <ChevronDown className="w-4 h-4 text-gray-500" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-gray-500" />
                    )}
                  </button>

                  {/* Attack List */}
                  {isExpanded && (
                    <div className="mt-1 space-y-1 ml-2">
                      {attacks.map(attack => (
                        <Link
                          key={attack.id}
                          to={`/attacks/${attack.id}`}
                          onClick={onClose}
                          className={`block px-4 py-2 rounded-lg text-sm transition-colors ${
                            isActiveAttack(attack.id)
                              ? 'bg-green-900 text-white font-medium'
                              : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <span>{attack.name}</span>
                            {isActiveAttack(attack.id) && (
                              <div className="w-2 h-2 bg-white rounded-full" />
                            )}
                          </div>
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Sidebar Footer */}
        <div className="sticky bottom-0 bg-white border-t-2 border-gray-200 p-4">
          <div className="text-xs text-gray-500 text-center">
            <p className="font-semibold mb-1">Educational Use Only</p>
            <p>Always obtain authorization</p>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
