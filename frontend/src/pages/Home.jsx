import HeroSection from '../components/home/HeroSection'

function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section with Enhanced Content */}
      <HeroSection />

      {/* Stats Section */}
      <div className="py-16 border-t-2 border-gray-300 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-5xl font-bold text-black mb-2">10+</div>
              <div className="text-lg text-gray-700 font-semibold">Attack Types</div>
              <p className="text-sm text-gray-600 mt-2">Network, Application & More</p>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-black mb-2">5</div>
              <div className="text-lg text-gray-700 font-semibold">Categories</div>
              <p className="text-sm text-gray-600 mt-2">Organized for Easy Discovery</p>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-black mb-2">100%</div>
              <div className="text-lg text-gray-700 font-semibold">Interactive</div>
              <p className="text-sm text-gray-600 mt-2">Hands-on Simulations</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
