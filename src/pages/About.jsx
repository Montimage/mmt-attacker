import { Link } from 'react-router-dom'
import { ArrowLeft, Building2, Target, Users, Mail, Globe, Award } from 'lucide-react'

function About() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        to="/"
        className="inline-flex items-center space-x-2 text-gray-400 hover:text-green-400 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="font-medium">Back to Home</span>
      </Link>

      {/* Header */}
      <div className="text-center mb-12">
        <div className="flex justify-center mb-6">
          <img
            src="/logo.svg"
            alt="MAG Logo"
            className="w-24 h-24 object-contain"
          />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-gray-100 mb-4">About MAG</h1>
        <p className="text-xl text-gray-400 max-w-3xl mx-auto">
          A comprehensive cybersecurity training platform developed by Montimage
        </p>
      </div>

      {/* About Montimage */}
      <div className="bg-gray-900 border-2 border-gray-700 rounded-lg shadow-custom-md p-8 mb-8">
        <div className="flex items-center space-x-3 mb-6">
          <Building2 className="w-8 h-8 text-gray-300" />
          <h2 className="text-3xl font-bold text-gray-100">About Montimage</h2>
        </div>

        <div className="space-y-4 text-gray-300 leading-relaxed">
          <p className="text-lg">
            <strong className="text-gray-100">Montimage</strong> is a leading French company specializing in network monitoring,
            security testing, and quality of service (QoS) analysis. Founded in 2011 and based in Paris,
            France, Montimage has established itself as a trusted partner for organizations seeking
            advanced network security solutions.
          </p>

          <div className="grid md:grid-cols-2 gap-6 my-8">
            <div className="bg-gray-800 border-2 border-gray-700 rounded-lg p-6">
              <Award className="w-8 h-8 text-gray-300 mb-3" />
              <h3 className="font-bold text-gray-100 mb-2">Our Expertise</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>• Network monitoring and analysis</li>
                <li>• Cybersecurity testing and validation</li>
                <li>• Quality of Service (QoS) assessment</li>
                <li>• Deep packet inspection technology</li>
                <li>• Security incident detection</li>
              </ul>
            </div>

            <div className="bg-gray-800 border-2 border-gray-700 rounded-lg p-6">
              <Users className="w-8 h-8 text-gray-300 mb-3" />
              <h3 className="font-bold text-gray-100 mb-2">Who We Serve</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>• Telecommunications providers</li>
                <li>• Government agencies</li>
                <li>• Research institutions</li>
                <li>• Enterprise organizations</li>
                <li>• Security professionals</li>
              </ul>
            </div>
          </div>

          <p>
            Our flagship product, <strong className="text-gray-100">MMT (Montimage Monitoring Tool)</strong>, is a comprehensive
            network traffic analysis solution that combines deep packet inspection with advanced analytics
            to provide real-time insights into network behavior and security threats.
          </p>
        </div>
      </div>

      {/* Why We Built This Tool */}
      <div className="bg-gray-900 border-2 border-gray-700 rounded-lg shadow-custom-md p-8 mb-8">
        <div className="flex items-center space-x-3 mb-6">
          <Target className="w-8 h-8 text-gray-300" />
          <h2 className="text-3xl font-bold text-gray-100">Why We Built This Tool</h2>
        </div>

        <div className="space-y-4 text-gray-300 leading-relaxed">
          <p className="text-lg font-semibold text-gray-100">
            MAG (Montimage Attack Generator) was developed with a clear mission: to provide comprehensive, hands-on
            cybersecurity training in a safe and controlled environment.
          </p>

          <div className="bg-green-950 border-2 border-green-700 rounded-lg p-6 my-6">
            <h3 className="font-bold text-green-300 mb-3 text-xl">Training Purpose</h3>
            <p className="mb-3 text-gray-300">
              In today's rapidly evolving threat landscape, security professionals need practical
              experience with attack techniques to effectively defend their networks. However,
              practicing these techniques in production environments is dangerous and often illegal.
            </p>
            <p className="text-gray-300">
              MAG bridges this gap by providing a fully simulated attack demonstration
              platform where users can:
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {[
              { title: '✓ Learn Attack Techniques', desc: 'Understand how common attacks work, their mechanisms, and their impact on systems.' },
              { title: '✓ Practice Safely', desc: 'Experiment with attack scenarios without risk to real systems or legal consequences.' },
              { title: '✓ Build Defense Strategies', desc: 'Develop effective countermeasures by understanding attacker methodologies.' },
              { title: '✓ Educate Teams', desc: 'Train security teams, students, and researchers with interactive demonstrations.' },
            ].map(({ title, desc }) => (
              <div key={title} className="bg-gray-800 border-2 border-gray-700 rounded-lg p-4">
                <h4 className="font-bold text-gray-100 mb-2">{title}</h4>
                <p className="text-sm text-gray-400">{desc}</p>
              </div>
            ))}
          </div>

          <p className="text-lg mt-6">
            This platform is an extension of Montimage's commitment to advancing cybersecurity
            awareness and providing practical tools for the security community. All attack simulations
            are educational demonstrations designed to help users understand security vulnerabilities
            and develop better defensive strategies.
          </p>
        </div>
      </div>

      {/* Contact Information */}
      <div className="bg-gray-900 border-2 border-gray-700 rounded-lg shadow-custom-md p-8">
        <h2 className="text-3xl font-bold text-gray-100 mb-6">Contact Montimage</h2>

        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-bold text-gray-100 mb-4">Company Information</h3>
            <div className="space-y-3 text-gray-400">
              <p className="font-semibold text-gray-300">Montimage EURL</p>
              <p>39 rue Bobillot</p>
              <p>75013 Paris, France</p>
            </div>
          </div>

          <div>
            <h3 className="font-bold text-gray-100 mb-4">Get in Touch</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Globe className="w-5 h-5 text-gray-400" />
                <a
                  href="https://www.montimage.eu"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-400 hover:text-green-300 font-medium"
                >
                  www.montimage.eu
                </a>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 text-gray-400" />
                <a
                  href="mailto:contact@montimage.eu"
                  className="text-green-400 hover:text-green-300 font-medium"
                >
                  contact@montimage.eu
                </a>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t-2 border-gray-700">
          <p className="text-sm text-gray-500 text-center">
            For technical support, security inquiries, or partnership opportunities, please contact us
            through the channels above.
          </p>
        </div>
      </div>

      {/* Back to Home Button */}
      <div className="text-center mt-8">
        <Link
          to="/"
          className="inline-flex items-center space-x-2 bg-gray-800 text-gray-100 px-6 py-3 rounded-lg font-semibold hover:bg-gray-700 transition-colors shadow-custom-md hover:shadow-custom-lg border border-gray-600"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>
      </div>
    </div>
  )
}

export default About
