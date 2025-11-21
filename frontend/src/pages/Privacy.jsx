import { Link } from 'react-router-dom'
import { ArrowLeft, Shield, Eye, Lock, Database, FileText } from 'lucide-react'

function Privacy() {
  const lastUpdated = "January 2025"

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        to="/"
        className="inline-flex items-center space-x-2 text-gray-600 hover:text-green-900 mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="font-medium">Back to Home</span>
      </Link>

      {/* Header */}
      <div className="text-center mb-12">
        <div className="flex justify-center mb-4">
          <Shield className="w-16 h-16 text-black" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">Privacy Policy</h1>
        <p className="text-lg text-gray-600">
          Last Updated: {lastUpdated}
        </p>
      </div>

      {/* Introduction */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Introduction</h2>
        <p className="text-gray-700 leading-relaxed">
          Montimage EURL ("we," "our," or "us") is committed to protecting your privacy. This Privacy
          Policy explains how we collect, use, disclose, and safeguard your information when you use
          the MMT-Attacker demonstration platform (the "Service"). Please read this privacy policy
          carefully. If you do not agree with the terms of this privacy policy, please do not access
          the Service.
        </p>
      </div>

      {/* Data Collection */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <Database className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">Information We Collect</h2>
        </div>

        <div className="space-y-4 text-gray-700">
          <div>
            <h3 className="font-bold text-black mb-2">1. Automatically Collected Information</h3>
            <p className="mb-2">
              When you access the Service, we may automatically collect certain information about your
              device, including:
            </p>
            <ul className="list-disc list-inside ml-4 space-y-1">
              <li>IP address</li>
              <li>Browser type and version</li>
              <li>Operating system</li>
              <li>Access times and dates</li>
              <li>Pages viewed and interactions with the Service</li>
              <li>Referring website addresses</li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold text-black mb-2">2. Simulation Data</h3>
            <p>
              The MMT-Attacker platform operates as a demonstration tool with simulated attacks. All
              attack parameters you input and simulation results are:
            </p>
            <ul className="list-disc list-inside ml-4 space-y-1 mt-2">
              <li>Processed locally in your browser</li>
              <li>Not transmitted to our servers</li>
              <li>Not stored or logged by Montimage</li>
              <li>Purely educational and simulated</li>
            </ul>
          </div>

          <div>
            <h3 className="font-bold text-black mb-2">3. Cookies and Tracking Technologies</h3>
            <p>
              We may use cookies and similar tracking technologies to monitor activity on our Service
              and store certain information. You can instruct your browser to refuse all cookies or to
              indicate when a cookie is being sent.
            </p>
          </div>
        </div>
      </div>

      {/* How We Use Information */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <Eye className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">How We Use Your Information</h2>
        </div>

        <div className="space-y-3 text-gray-700">
          <p>We use the collected information for the following purposes:</p>
          <ul className="list-disc list-inside ml-4 space-y-2">
            <li>
              <strong>Service Provision:</strong> To provide, maintain, and improve the demonstration
              platform
            </li>
            <li>
              <strong>Analytics:</strong> To understand how users interact with the Service and improve
              user experience
            </li>
            <li>
              <strong>Security:</strong> To detect, prevent, and address technical issues and security
              threats
            </li>
            <li>
              <strong>Legal Compliance:</strong> To comply with applicable laws, regulations, and legal
              processes
            </li>
            <li>
              <strong>Communication:</strong> To send you technical notices, updates, and security alerts
            </li>
          </ul>
        </div>
      </div>

      {/* Data Security */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <Lock className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">Data Security</h2>
        </div>

        <p className="text-gray-700 leading-relaxed">
          We implement appropriate technical and organizational security measures to protect your
          information against unauthorized access, alteration, disclosure, or destruction. These
          measures include:
        </p>

        <ul className="list-disc list-inside ml-4 space-y-2 mt-4 text-gray-700">
          <li>Encryption of data in transit using HTTPS/TLS protocols</li>
          <li>Regular security assessments and updates</li>
          <li>Access controls and authentication mechanisms</li>
          <li>Secure hosting infrastructure</li>
          <li>Monitoring for security vulnerabilities</li>
        </ul>

        <div className="bg-yellow-50 border-2 border-yellow-600 rounded-lg p-4 mt-4">
          <p className="text-sm text-gray-800">
            <strong>Note:</strong> No method of transmission over the Internet or electronic storage is
            100% secure. While we strive to use commercially acceptable means to protect your information,
            we cannot guarantee its absolute security.
          </p>
        </div>
      </div>

      {/* Third-Party Services */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Third-Party Services</h2>

        <div className="space-y-4 text-gray-700">
          <p>
            The Service may contain links to third-party websites or services that are not owned or
            controlled by Montimage. We have no control over, and assume no responsibility for, the
            content, privacy policies, or practices of any third-party websites or services.
          </p>

          <p>
            We may use third-party service providers to facilitate our Service, including:
          </p>

          <ul className="list-disc list-inside ml-4 space-y-1">
            <li>Hosting and content delivery network (CDN) services</li>
            <li>Analytics and performance monitoring tools</li>
            <li>Security and fraud prevention services</li>
          </ul>

          <p>
            These third parties have access to your information only to perform these tasks on our behalf
            and are obligated not to disclose or use it for any other purpose.
          </p>
        </div>
      </div>

      {/* Your Rights */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <FileText className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">Your Privacy Rights</h2>
        </div>

        <div className="space-y-3 text-gray-700">
          <p>Depending on your location, you may have the following rights regarding your personal data:</p>

          <ul className="list-disc list-inside ml-4 space-y-2">
            <li>
              <strong>Access:</strong> Request access to the personal data we hold about you
            </li>
            <li>
              <strong>Correction:</strong> Request correction of inaccurate or incomplete data
            </li>
            <li>
              <strong>Deletion:</strong> Request deletion of your personal data
            </li>
            <li>
              <strong>Objection:</strong> Object to our processing of your personal data
            </li>
            <li>
              <strong>Data Portability:</strong> Request transfer of your data to another service
            </li>
            <li>
              <strong>Withdraw Consent:</strong> Withdraw consent where processing is based on consent
            </li>
          </ul>

          <p className="mt-4">
            To exercise these rights, please contact us at{' '}
            <a href="mailto:contact@montimage.eu" className="text-green-900 hover:text-green-800 font-medium">
              contact@montimage.eu
            </a>
          </p>
        </div>
      </div>

      {/* Children's Privacy */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Children's Privacy</h2>
        <p className="text-gray-700 leading-relaxed">
          The Service is not intended for use by children under the age of 18. We do not knowingly
          collect personal information from children under 18. If you are a parent or guardian and
          believe your child has provided us with personal information, please contact us. If we
          discover that we have collected personal information from children under 18 without
          verification of parental consent, we will take steps to remove that information.
        </p>
      </div>

      {/* Changes to Policy */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Changes to This Privacy Policy</h2>
        <p className="text-gray-700 leading-relaxed">
          We may update our Privacy Policy from time to time. We will notify you of any changes by
          posting the new Privacy Policy on this page and updating the "Last Updated" date. You are
          advised to review this Privacy Policy periodically for any changes. Changes to this Privacy
          Policy are effective when they are posted on this page.
        </p>
      </div>

      {/* Contact */}
      <div className="bg-green-50 border-2 border-green-700 rounded-lg shadow-custom-md p-8 mb-8">
        <h2 className="text-2xl font-bold text-black mb-4">Contact Us</h2>
        <p className="text-gray-700 mb-4">
          If you have any questions about this Privacy Policy, please contact us:
        </p>
        <div className="space-y-2 text-gray-700">
          <p>
            <strong>Email:</strong>{' '}
            <a href="mailto:contact@montimage.eu" className="text-green-900 hover:text-green-800 font-medium">
              contact@montimage.eu
            </a>
          </p>
          <p>
            <strong>Address:</strong> 39 rue Bobillot, 75013 Paris, France
          </p>
          <p>
            <strong>Website:</strong>{' '}
            <a
              href="https://www.montimage.eu"
              target="_blank"
              rel="noopener noreferrer"
              className="text-green-900 hover:text-green-800 font-medium"
            >
              www.montimage.eu
            </a>
          </p>
        </div>
      </div>

      {/* Back to Home Button */}
      <div className="text-center">
        <Link
          to="/"
          className="inline-flex items-center space-x-2 bg-black text-white px-6 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors shadow-custom-md hover:shadow-custom-lg"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>
      </div>
    </div>
  )
}

export default Privacy
