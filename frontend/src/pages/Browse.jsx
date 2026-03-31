import { useState, useMemo, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Search, Filter, Grid, List, ChevronDown, ChevronRight } from 'lucide-react'
import { getCategories, getAttacksByCategory } from '../data/attacksData'
import AttackTypeCard from '../components/home/AttackTypeCard'
import { Link } from 'react-router-dom'

function Browse() {
  const [searchParams, setSearchParams] = useSearchParams()
  const categories = getCategories()
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [viewMode, setViewMode] = useState('grid') // 'grid' or 'list'
  const [expandedCategories, setExpandedCategories] = useState(
    categories.reduce((acc, cat) => ({ ...acc, [cat]: true }), {})
  )

  // Update search query from URL params
  useEffect(() => {
    const searchParam = searchParams.get('search')
    if (searchParam) {
      setSearchQuery(searchParam)
    }
  }, [searchParams])

  const categoryDisplayNames = {
    'Network-Layer': 'Network Layer Attacks',
    'Application-Layer': 'Application Layer Attacks',
    'Amplification': 'Amplification Attacks',
    'Credential': 'Credential Attacks',
    'Other': 'Other Attacks'
  }

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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <div className="bg-slate-900 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            Browse Attacks
          </h1>
          <p className="text-slate-400 max-w-3xl">
            Explore our comprehensive collection of attack simulations. Search, filter, and discover different types of cybersecurity attacks.
          </p>
        </div>
      </div>

      {/* Search and Filter Bar */}
      <div className="sticky top-16 z-40 bg-white border-b border-gray-200 shadow-custom-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex flex-col lg:flex-row gap-3 items-start lg:items-center justify-between">
            {/* Search Box */}
            <div className="relative flex-1 w-full lg:max-w-md">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="w-4 h-4 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search attacks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-all bg-white"
              />
            </div>

            {/* Filters and Controls */}
            <div className="flex flex-wrap gap-2 items-center w-full lg:w-auto">
              {/* Category Filter */}
              <div className="flex items-center space-x-2">
                <Filter className="w-4 h-4 text-gray-500" />
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:border-green-500 transition-all bg-white"
                >
                  <option value="all">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>
                      {categoryDisplayNames[cat] || cat}
                    </option>
                  ))}
                </select>
              </div>

              {/* View Mode Toggle */}
              <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1 border border-gray-200">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-1.5 rounded transition-all ${
                    viewMode === 'grid'
                      ? 'bg-white border border-gray-300 shadow-custom text-green-600'
                      : 'text-gray-500 hover:bg-gray-200'
                  }`}
                  title="Grid view"
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-1.5 rounded transition-all ${
                    viewMode === 'list'
                      ? 'bg-white border border-gray-300 shadow-custom text-green-600'
                      : 'text-gray-500 hover:bg-gray-200'
                  }`}
                  title="List view"
                >
                  <List className="w-4 h-4" />
                </button>
              </div>

              {/* Expand/Collapse */}
              <div className="flex items-center space-x-2 text-sm">
                <button
                  onClick={expandAll}
                  className="px-3 py-2 bg-white border border-gray-300 rounded-lg hover:border-green-500 hover:text-green-700 transition-all text-sm text-gray-600"
                >
                  Expand All
                </button>
                <button
                  onClick={collapseAll}
                  className="px-3 py-2 bg-white border border-gray-300 rounded-lg hover:border-green-500 hover:text-green-700 transition-all text-sm text-gray-600"
                >
                  Collapse All
                </button>
              </div>
            </div>
          </div>

          {/* Results Count */}
          <div className="mt-2 text-xs text-gray-500">
            Showing <span className="font-semibold text-gray-800">{totalAttacks}</span> attack{totalAttacks !== 1 ? 's' : ''}
            {searchQuery && <span> matching "{searchQuery}"</span>}
          </div>
        </div>
      </div>

      {/* Attack Categories */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {filteredCategories.length === 0 ? (
          <div className="text-center py-16">
            <Search className="w-14 h-14 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-bold text-gray-700 mb-2">No attacks found</h3>
            <p className="text-gray-500 mb-6 text-sm">Try adjusting your search or filter criteria</p>
            <button
              onClick={() => {
                setSearchQuery('')
                setSelectedCategory('all')
              }}
              className="px-5 py-2.5 bg-white border border-gray-300 rounded-lg hover:border-green-500 hover:text-green-700 transition-all text-sm font-medium"
            >
              Clear All Filters
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {filteredCategories.map(({ name: category, attacks }) => {
              const isExpanded = expandedCategories[category]

              return (
                <div key={category} className="bg-white border border-gray-200 rounded-xl shadow-custom-md overflow-hidden">
                  {/* Category Header */}
                  <button
                    onClick={() => toggleCategory(category)}
                    className="w-full flex items-center justify-between px-6 py-4 bg-white hover:bg-gray-50 transition-colors border-b border-gray-100"
                  >
                    <div className="flex items-center space-x-3">
                      <h2 className="text-xl font-bold text-slate-800">
                        {categoryDisplayNames[category] || category}
                      </h2>
                      <span className="text-xs font-semibold text-green-700 bg-green-50 border border-green-200 px-2.5 py-1 rounded-full">
                        {attacks.length}
                      </span>
                    </div>
                    {isExpanded ? (
                      <ChevronDown className="w-5 h-5 text-gray-400" />
                    ) : (
                      <ChevronRight className="w-5 h-5 text-gray-400" />
                    )}
                  </button>

                  {/* Attack List */}
                  {isExpanded && (
                    <div className="p-6">
                      {viewMode === 'grid' ? (
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
                          {attacks.map(attack => (
                            <AttackTypeCard key={attack.id} attack={attack} />
                          ))}
                        </div>
                      ) : (
                        <div className="space-y-2">
                          {attacks.map(attack => (
                            <Link
                              key={attack.id}
                              to={`/attacks/${attack.id}`}
                              className="flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4 hover:border-green-400 hover:shadow-custom transition-all group"
                            >
                              <div className="flex-1">
                                <h3 className="text-base font-semibold text-slate-800 group-hover:text-green-700 mb-0.5">
                                  {attack.name}
                                </h3>
                                <p className="text-sm text-gray-500 line-clamp-1">
                                  {attack.description}
                                </p>
                              </div>
                              <div className="ml-4 text-xs text-gray-400 whitespace-nowrap">
                                {attack.scenarios.length} scenario{attack.scenarios.length !== 1 ? 's' : ''}
                              </div>
                            </Link>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default Browse
