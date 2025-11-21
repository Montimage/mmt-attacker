import HeroSection from '../components/home/HeroSection'
import AttackTypeCard from '../components/home/AttackTypeCard'
import { getCategories, getAttacksByCategory } from '../data/attacksData'

function Home() {
  const categories = getCategories()

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <HeroSection />

      {/* Attack Categories Section */}
      <div id="attack-categories" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-black mb-4">
            Attack Categories
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Explore different types of network and application attacks. Each attack includes
            detailed theory, interactive simulations, and educational explanations.
          </p>
        </div>

        {/* Attacks by Category */}
        {categories.map((category) => {
          const attacks = getAttacksByCategory(category)

          const categoryDisplayNames = {
            'Network-Layer': 'Network Layer Attacks',
            'Application-Layer': 'Application Layer Attacks',
            'Amplification': 'Amplification Attacks',
            'Credential': 'Credential Attacks',
            'Other': 'Other Attacks'
          }

          return (
            <div key={category} className="mb-16 last:mb-0">
              {/* Category Header */}
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-black mb-2">
                  {categoryDisplayNames[category] || category}
                </h3>
                <div className="h-1 w-20 bg-green-900 rounded"></div>
              </div>

              {/* Attack Cards Grid */}
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {attacks.map((attack) => (
                  <AttackTypeCard key={attack.id} attack={attack} />
                ))}
              </div>
            </div>
          )
        })}
      </div>

      {/* Bottom CTA Section */}
      <div className="bg-gray-50 border-t-2 border-gray-200 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3 className="text-2xl font-bold text-black mb-4">
            Ready to Learn About Cybersecurity?
          </h3>
          <p className="text-gray-600 mb-6">
            Choose an attack type above to explore detailed simulations, understand the mechanisms,
            and learn how to protect against these threats.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="https://github.com/montimage/mmt-attacker"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white text-gray-900 px-6 py-3 rounded-lg border-2 border-gray-300 shadow-custom hover:border-gray-400 hover:shadow-custom-md transition-all duration-200 font-medium"
            >
              View on GitHub
            </a>
            <a
              href="https://github.com/montimage/mmt-attacker/blob/main/docs/PLAYBOOK.md"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-green-900 text-white px-6 py-3 rounded-lg border-2 border-green-900 shadow-custom hover:bg-green-800 hover:shadow-custom-md transition-all duration-200 font-medium"
            >
              Read Documentation
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
