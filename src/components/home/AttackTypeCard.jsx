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
      className="bg-gray-800 border border-gray-700 rounded-xl shadow-custom p-5 hover:shadow-custom-lg hover:border-green-500 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer group"
    >
      {/* Icon and Badge */}
      <div className="flex items-start justify-between mb-4">
        <div className="bg-green-950 border border-green-800 p-2.5 rounded-lg group-hover:bg-green-900 transition-colors">
          <Icon className="w-6 h-6 text-green-400" />
        </div>
        <Badge variant="outline" className="text-xs">
          {attack.category}
        </Badge>
      </div>

      {/* Title */}
      <h3 className="text-base font-bold text-gray-100 mb-1.5 group-hover:text-green-400 transition-colors">
        {attack.name}
      </h3>

      {/* Description */}
      <p className="text-gray-400 text-sm mb-4 line-clamp-2">
        {attack.description}
      </p>

      {/* Key Features Preview */}
      {attack.keyFeatures && attack.keyFeatures.length > 0 && (
        <div className="mb-4">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Key Features:</p>
          <ul className="space-y-1">
            {attack.keyFeatures.slice(0, 2).map((feature, index) => (
              <li key={index} className="text-xs text-gray-400 flex items-start">
                <span className="text-green-500 mr-1.5 mt-0.5">•</span>
                <span className="line-clamp-1">{feature}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Scenarios Count */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-700">
        <span className="text-xs text-gray-500">
          {attack.scenarios.length} scenario{attack.scenarios.length !== 1 ? 's' : ''}
        </span>
        <div className="flex items-center space-x-1 text-green-400 font-medium text-sm group-hover:translate-x-1 transition-transform">
          <span>Learn More</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </div>
      </div>
    </div>
  )
}

export default AttackTypeCard
