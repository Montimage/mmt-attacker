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
    <div className="min-h-screen bg-white">
      {/* Header Section */}
      <div className="bg-gray-50 border-b-2 border-gray-300 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">
            Browse Attacks
          </h1>
          <p className="text-lg text-gray-700 max-w-3xl">
            Explore our comprehensive collection of attack simulations. Search, filter, and discover different types of cybersecurity attacks.
          </p>
        </div>
      </div>

      {/* Search and Filter Bar */}
      <div className="sticky top-20 z-40 bg-white border-b-2 border-gray-300 shadow-custom-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
            {/* Search Box */}
            <div className="relative flex-1 w-full lg:max-w-md">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="w-5 h-5 text-gray-500" />
              </div>
              <input
                type="text"
                placeholder="Search attacks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3 text-base border-2 border-gray-400 rounded-lg focus:outline-none focus:border-black focus:shadow-custom-md transition-all bg-white font-medium"
              />
            </div>

            {/* Filters and Controls */}
            <div className="flex flex-wrap gap-3 items-center w-full lg:w-auto">
              {/* Category Filter */}
              <div className="flex items-center space-x-2">
                <Filter className="w-4 h-4 text-gray-600" />
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="px-4 py-2.5 text-sm border-2 border-gray-400 rounded-lg focus:outline-none focus:border-black focus:shadow-custom transition-all bg-white font-semibold"
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
              <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1 border border-gray-300">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded transition-all ${
                    viewMode === 'grid'
                      ? 'bg-white border border-gray-400 shadow-custom'
                      : 'hover:bg-gray-200'
                  }`}
                  title="Grid view"
                >
                  <Grid className="w-4 h-4 text-gray-700" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded transition-all ${
                    viewMode === 'list'
                      ? 'bg-white border border-gray-400 shadow-custom'
                      : 'hover:bg-gray-200'
                  }`}
                  title="List view"
                >
                  <List className="w-4 h-4 text-gray-700" />
                </button>
              </div>

              {/* Expand/Collapse */}
              <div className="flex items-center space-x-2 text-sm">
                <button
                  onClick={expandAll}
                  className="px-3 py-2 bg-white border-2 border-gray-300 rounded-lg hover:border-gray-500 hover:shadow-custom transition-all font-semibold"
                >
                  Expand All
                </button>
                <button
                  onClick={collapseAll}
                  className="px-3 py-2 bg-white border-2 border-gray-300 rounded-lg hover:border-gray-500 hover:shadow-custom transition-all font-semibold"
                >
                  Collapse All
                </button>
              </div>
            </div>
          </div>

          {/* Results Count */}
          <div className="mt-4 text-sm text-gray-700 font-semibold">
            Showing <span className="text-black">{totalAttacks}</span> attack{totalAttacks !== 1 ? 's' : ''}
            {searchQuery && <span> matching "{searchQuery}"</span>}
          </div>
        </div>
      </div>

      {/* Attack Categories */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {filteredCategories.length === 0 ? (
          <div className="text-center py-16">
            <Search className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-gray-900 mb-2">No attacks found</h3>
            <p className="text-gray-600 mb-6">Try adjusting your search or filter criteria</p>
            <button
              onClick={() => {
                setSearchQuery('')
                setSelectedCategory('all')
              }}
              className="px-6 py-3 bg-white border-2 border-black rounded-lg hover:shadow-custom-md transition-all font-bold"
            >
              Clear All Filters
            </button>
          </div>
        ) : (
          <div className="space-y-8">
            {filteredCategories.map(({ name: category, attacks }) => {
              const isExpanded = expandedCategories[category]

              return (
                <div key={category} className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md overflow-hidden">
                  {/* Category Header */}
                  <button
                    onClick={() => toggleCategory(category)}
                    className="w-full flex items-center justify-between px-6 py-4 bg-gray-50 hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex items-center space-x-3">
                      <h2 className="text-2xl font-bold text-black">
                        {categoryDisplayNames[category] || category}
                      </h2>
                      <span className="text-sm font-bold text-gray-600 bg-gray-200 px-3 py-1 rounded-full">
                        {attacks.length}
                      </span>
                    </div>
                    {isExpanded ? (
                      <ChevronDown className="w-6 h-6 text-black" />
                    ) : (
                      <ChevronRight className="w-6 h-6 text-black" />
                    )}
                  </button>

                  {/* Attack List */}
                  {isExpanded && (
                    <div className="p-6">
                      {viewMode === 'grid' ? (
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {attacks.map(attack => (
                            <AttackTypeCard key={attack.id} attack={attack} />
                          ))}
                        </div>
                      ) : (
                        <div className="space-y-3">
                          {attacks.map(attack => (
                            <Link
                              key={attack.id}
                              to={`/attacks/${attack.id}`}
                              className="block bg-white border-2 border-gray-300 rounded-lg p-4 hover:border-gray-500 hover:shadow-custom transition-all"
                            >
                              <div className="flex items-center justify-between">
                                <div className="flex-1">
                                  <h3 className="text-lg font-bold text-black mb-1">
                                    {attack.name}
                                  </h3>
                                  <p className="text-sm text-gray-600 line-clamp-1">
                                    {attack.description}
                                  </p>
                                </div>
                                <div className="ml-4 text-sm text-gray-500">
                                  {attack.scenarios.length} scenario{attack.scenarios.length !== 1 ? 's' : ''}
                                </div>
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
