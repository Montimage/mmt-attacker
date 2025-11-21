import { useNavigate } from 'react-router-dom'
import { ArrowRight, Network, Globe, Zap, Key, FileText } from 'lucide-react'
import Badge from '../common/Badge'

// Icon mapping for categories
const categoryIcons = {
  'Network-Layer': Network,
  'Application-Layer': Globe,
  'Amplification': Zap,
  'Credential': Key,
  'Other': FileText
}

function AttackTypeCard({ attack }) {
  const navigate = useNavigate()
  const Icon = categoryIcons[attack.category] || Network

  const handleClick = () => {
    navigate(`/attacks/${attack.id}`)
  }

  return (
    <div
      onClick={handleClick}
      className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-6 hover:shadow-custom-lg hover:border-gray-500 hover:-translate-y-1 transition-all duration-200 cursor-pointer group"
    >
      {/* Icon and Badge */}
      <div className="flex items-start justify-between mb-4">
        <div className="bg-gray-100 p-3 rounded-lg border-2 border-gray-400 group-hover:bg-gray-200 group-hover:border-gray-500 transition-colors shadow-custom">
          <Icon className="w-8 h-8 text-black" />
        </div>
        <Badge variant="outline" className="text-xs">
          {attack.category}
        </Badge>
      </div>

      {/* Title */}
      <h3 className="text-xl font-bold text-black mb-2 transition-colors">
        {attack.name}
      </h3>

      {/* Description */}
      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
        {attack.description}
      </p>

      {/* Key Features Preview */}
      {attack.keyFeatures && attack.keyFeatures.length > 0 && (
        <div className="mb-4">
          <p className="text-xs font-semibold text-gray-500 uppercase mb-2">Key Features:</p>
          <ul className="space-y-1">
            {attack.keyFeatures.slice(0, 2).map((feature, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start">
                <span className="text-black mr-2">•</span>
                <span className="line-clamp-1">{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Scenarios Count */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-300">
        <span className="text-sm text-gray-600 font-medium">
          {attack.scenarios.length} scenario{attack.scenarios.length !== 1 ? 's' : ''}
        </span>
        <div className="flex items-center space-x-2 text-black font-semibold text-sm group-hover:translate-x-1 transition-transform">
          <span>Learn More</span>
          <ArrowRight className="w-4 h-4" />
        </div>
      </div>
    </div>
  )
}

export default AttackTypeCard
