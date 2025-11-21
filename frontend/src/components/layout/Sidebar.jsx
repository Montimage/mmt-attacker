import { Link, useLocation } from 'react-router-dom'
import { ChevronDown, ChevronRight, Shield, Home, Search, X, Filter } from 'lucide-react'
import { useState, useMemo } from 'react'
import { getCategories, getAttacksByCategory } from '../../data/attacksData'

function Sidebar({ isOpen, onClose }) {
  const location = useLocation()
  const categories = getCategories()
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [expandedCategories, setExpandedCategories] = useState(
    // Collapse all categories by default for better performance with many attacks
    {}
  )

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }))
  }

  const collapseAll = () => {
    setExpandedCategories({})
  }

  const expandAll = () => {
    setExpandedCategories(
      categories.reduce((acc, cat) => ({ ...acc, [cat]: true }), {})
    )
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

  // Filter attacks based on search query and category filter
  const filteredCategories = useMemo(() => {
    if (!searchQuery && selectedCategory === 'all') {
      return categories.map(cat => ({
        name: cat,
        attacks: getAttacksByCategory(cat)
      }))
    }

    return categories
      .map(cat => {
        const attacks = getAttacksByCategory(cat)
        const filtered = attacks.filter(attack =>
          attack.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
          (selectedCategory === 'all' || cat === selectedCategory)
        )
        return { name: cat, attacks: filtered }
      })
      .filter(cat => cat.attacks.length > 0)
  }, [searchQuery, selectedCategory, categories])

  const totalAttacks = useMemo(() => {
    return filteredCategories.reduce((sum, cat) => sum + cat.attacks.length, 0)
  }, [filteredCategories])

  const clearSearch = () => {
    setSearchQuery('')
    setSelectedCategory('all')
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
        className={`fixed lg:sticky top-20 left-0 h-[calc(100vh-5rem)] w-72 bg-white border-r border-gray-300 overflow-hidden z-50 transition-transform duration-300 flex flex-col ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-4 space-y-4 flex-shrink-0 border-b-2 border-gray-300 bg-gray-50">
          {/* Home Link */}
          <Link
            to="/"
            onClick={onClose}
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 border-2 font-semibold ${
              location.pathname === '/'
                ? 'bg-black text-white border-black shadow-custom-md'
                : 'bg-white text-gray-700 border-gray-300 hover:border-gray-500 hover:shadow-custom hover:-translate-y-0.5'
            }`}
          >
            <Home className="w-5 h-5" />
            <span className="font-medium">Home</span>
          </Link>

          {/* Search Bar */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="w-4 h-4 text-gray-500" />
            </div>
            <input
              type="text"
              placeholder="Search attacks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-10 py-2.5 text-sm border-2 border-gray-400 rounded-lg focus:outline-none focus:border-black focus:shadow-custom-md transition-all bg-white"
            />
            {searchQuery && (
              <button
                onClick={clearSearch}
                className="absolute inset-y-0 right-0 pr-3 flex items-center hover:opacity-70 transition-opacity"
              >
                <X className="w-4 h-4 text-gray-600" />
              </button>
            )}
          </div>

          {/* Category Filter */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-bold text-gray-700 uppercase flex items-center space-x-1">
                <Filter className="w-3 h-3" />
                <span>Filter by Category</span>
              </label>
            </div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3 py-2 text-sm border-2 border-gray-400 rounded-lg focus:outline-none focus:border-black focus:shadow-custom-md transition-all bg-white font-medium"
            >
              <option value="all">All Categories ({categories.length})</option>
              {categories.map(cat => (
                <option key={cat} value={cat}>
                  {categoryDisplayNames[cat] || cat}
                </option>
              ))}
            </select>
          </div>

          {/* Results info and expand/collapse controls */}
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-700 font-semibold">
              {totalAttacks} attack{totalAttacks !== 1 ? 's' : ''} found
            </span>
            <div className="flex space-x-1">
              <button
                onClick={expandAll}
                className="px-2 py-1 text-gray-600 hover:text-black hover:bg-gray-200 rounded transition-colors font-medium"
              >
                Expand All
              </button>
              <span className="text-gray-400">|</span>
              <button
                onClick={collapseAll}
                className="px-2 py-1 text-gray-600 hover:text-black hover:bg-gray-200 rounded transition-colors font-medium"
              >
                Collapse All
              </button>
            </div>
          </div>
        </div>

        {/* Attack Categories - Scrollable area */}
        <div className="flex-1 overflow-y-auto p-4">
          <div className="space-y-2">

            {filteredCategories.length === 0 ? (
              <div className="text-center py-8">
                <Shield className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p className="text-sm text-gray-600 font-medium">No attacks found</p>
                <p className="text-xs text-gray-500 mt-1">Try adjusting your search or filter</p>
                <button
                  onClick={clearSearch}
                  className="mt-3 px-4 py-2 text-sm bg-white border-2 border-gray-400 rounded-lg hover:border-black hover:shadow-custom transition-all font-semibold"
                >
                  Clear Filters
                </button>
              </div>
            ) : (
              filteredCategories.map(({ name: category, attacks }) => {
                const isExpanded = expandedCategories[category]

                return (
                  <div key={category} className="mb-2">
                    {/* Category Header with attack count */}
                    <button
                      onClick={() => toggleCategory(category)}
                      className="w-full flex items-center justify-between px-4 py-2.5 text-left font-semibold text-gray-900 bg-white border-2 border-gray-300 hover:border-gray-500 hover:shadow-custom rounded-lg transition-all duration-200"
                    >
                      <div className="flex items-center space-x-2">
                        <span className="text-sm">{categoryDisplayNames[category] || category}</span>
                        <span className="text-xs font-bold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                          {attacks.length}
                        </span>
                      </div>
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-black" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-black" />
                      )}
                    </button>

                    {/* Attack List */}
                    {isExpanded && (
                      <div className="mt-1 space-y-1">
                        {attacks.map(attack => (
                          <Link
                            key={attack.id}
                            to={`/attacks/${attack.id}`}
                            onClick={onClose}
                            className={`block px-4 py-2 rounded-lg text-sm transition-all duration-200 border ${
                              isActiveAttack(attack.id)
                                ? 'bg-black text-white font-semibold border-black shadow-custom-md'
                                : 'text-gray-700 bg-white border-gray-200 hover:bg-gray-50 hover:border-gray-400 hover:text-black hover:shadow-custom'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span className="truncate">{attack.name}</span>
                              {isActiveAttack(attack.id) && (
                                <div className="w-2 h-2 bg-green-500 rounded-full shadow-custom flex-shrink-0 ml-2" />
                              )}
                            </div>
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                )
              })
            )}
          </div>
        </div>

        {/* Sidebar Footer */}
        <div className="sticky bottom-0 bg-white border-t-2 border-gray-400 p-4 shadow-custom-md">
          <div className="text-xs text-gray-700 text-center bg-gray-50 border border-gray-300 rounded-lg p-3">
            <p className="font-bold mb-1 text-black">Educational Use Only</p>
            <p className="font-medium">Always obtain authorization</p>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
