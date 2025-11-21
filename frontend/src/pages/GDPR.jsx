import { Link } from 'react-router-dom'
import { ArrowLeft, Scale, UserCheck, Database, Clock, Globe, AlertCircle } from 'lucide-react'

function GDPR() {
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
          <Scale className="w-16 h-16 text-black" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-black mb-4">GDPR Compliance</h1>
        <p className="text-lg text-gray-600">
          General Data Protection Regulation Compliance Information
        </p>
      </div>

      {/* Introduction */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Our Commitment to GDPR</h2>
        <p className="text-gray-700 leading-relaxed mb-4">
          Montimage EURL is committed to ensuring compliance with the General Data Protection Regulation
          (GDPR) (EU) 2016/679. As the data controller for the MMT-Attacker demonstration platform, we
          take our data protection responsibilities seriously and have implemented appropriate technical
          and organizational measures to protect your personal data.
        </p>
        <p className="text-gray-700 leading-relaxed">
          This page provides information about how we comply with GDPR requirements and your rights as
          a data subject under GDPR.
        </p>
      </div>

      {/* Data Controller */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <UserCheck className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">Data Controller</h2>
        </div>

        <div className="space-y-3 text-gray-700">
          <p>
            <strong>Entity:</strong> Montimage EURL
          </p>
          <p>
            <strong>Address:</strong> 39 rue Bobillot, 75013 Paris, France
          </p>
          <p>
            <strong>Contact:</strong>{' '}
            <a href="mailto:contact@montimage.eu" className="text-green-900 hover:text-green-800 font-medium">
              contact@montimage.eu
            </a>
          </p>
          <p>
            <strong>Data Protection Officer:</strong>{' '}
            <a href="mailto:dpo@montimage.eu" className="text-green-900 hover:text-green-800 font-medium">
              dpo@montimage.eu
            </a>
          </p>
        </div>
      </div>

      {/* Legal Basis */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Legal Basis for Processing</h2>

        <div className="space-y-4 text-gray-700">
          <p>
            We process personal data based on the following legal grounds under GDPR Article 6:
          </p>

          <div className="space-y-3">
            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">1. Legitimate Interest (Article 6(1)(f))</h3>
              <p className="text-sm">
                We process certain data based on our legitimate interests in providing, maintaining,
                and improving the demonstration platform, ensuring security, and analyzing usage patterns.
                We have conducted legitimate interest assessments to ensure our interests do not override
                your rights and freedoms.
              </p>
            </div>

            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">2. Consent (Article 6(1)(a))</h3>
              <p className="text-sm">
                Where required, we obtain your explicit consent before processing your personal data.
                You have the right to withdraw your consent at any time.
              </p>
            </div>

            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">3. Legal Obligation (Article 6(1)(c))</h3>
              <p className="text-sm">
                We may process your data when necessary to comply with legal obligations, such as
                responding to lawful requests from public authorities.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Data Subject Rights */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <Database className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">Your GDPR Rights</h2>
        </div>

        <div className="space-y-3 text-gray-700">
          <p>Under the GDPR, you have the following rights regarding your personal data:</p>

          <div className="grid md:grid-cols-2 gap-4 mt-4">
            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">✓ Right of Access (Article 15)</h3>
              <p className="text-sm">
                You have the right to obtain confirmation as to whether your personal data is being
                processed and, if so, access to that data and information about the processing.
              </p>
            </div>

            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">✓ Right to Rectification (Article 16)</h3>
              <p className="text-sm">
                You have the right to request correction of inaccurate personal data and to have
                incomplete data completed.
              </p>
            </div>

            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">✓ Right to Erasure (Article 17)</h3>
              <p className="text-sm">
                Also known as the "right to be forgotten," you can request deletion of your personal
                data in certain circumstances.
              </p>
            </div>

            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">✓ Right to Restriction (Article 18)</h3>
              <p className="text-sm">
                You have the right to request restriction of processing of your personal data in
                certain situations.
              </p>
            </div>

            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">✓ Right to Data Portability (Article 20)</h3>
              <p className="text-sm">
                You have the right to receive your personal data in a structured, commonly used, and
                machine-readable format and to transmit that data to another controller.
              </p>
            </div>

            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
              <h3 className="font-bold text-black mb-2">✓ Right to Object (Article 21)</h3>
              <p className="text-sm">
                You have the right to object to processing of your personal data based on legitimate
                interests or for direct marketing purposes.
              </p>
            </div>
          </div>

          <div className="bg-green-50 border-2 border-green-700 rounded-lg p-4 mt-6">
            <p className="font-semibold text-black mb-2">How to Exercise Your Rights</p>
            <p className="text-sm">
              To exercise any of these rights, please contact us at{' '}
              <a href="mailto:dpo@montimage.eu" className="text-green-900 hover:text-green-800 font-medium">
                dpo@montimage.eu
              </a>
              . We will respond to your request within one month of receipt.
            </p>
          </div>
        </div>
      </div>

      {/* Data Retention */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <Clock className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">Data Retention</h2>
        </div>

        <div className="space-y-3 text-gray-700">
          <p>
            We retain personal data only for as long as necessary to fulfill the purposes for which it
            was collected, including:
          </p>

          <ul className="list-disc list-inside ml-4 space-y-2">
            <li>
              <strong>Service Data:</strong> Retained while you actively use the Service and for up to
              90 days after your last interaction
            </li>
            <li>
              <strong>Analytics Data:</strong> Anonymized and aggregated within 180 days; personal
              identifiers removed
            </li>
            <li>
              <strong>Security Logs:</strong> Retained for up to 12 months for security and fraud
              prevention purposes
            </li>
            <li>
              <strong>Legal Compliance:</strong> Some data may be retained longer where required by law
              or for legitimate legal purposes
            </li>
          </ul>

          <p className="mt-4">
            After the retention period expires, personal data is securely deleted or anonymized in
            accordance with our data retention schedule.
          </p>
        </div>
      </div>

      {/* International Transfers */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <Globe className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">International Data Transfers</h2>
        </div>

        <div className="space-y-3 text-gray-700">
          <p>
            Your personal data may be transferred to and processed in countries outside the European
            Economic Area (EEA). When we transfer data internationally, we ensure appropriate safeguards
            are in place, including:
          </p>

          <ul className="list-disc list-inside ml-4 space-y-2">
            <li>
              <strong>Standard Contractual Clauses (SCCs):</strong> We use EU-approved Standard
              Contractual Clauses for transfers to third countries
            </li>
            <li>
              <strong>Adequacy Decisions:</strong> We transfer data to countries deemed by the European
              Commission to provide adequate data protection
            </li>
            <li>
              <strong>Binding Corporate Rules:</strong> For transfers within corporate groups, we rely
              on approved Binding Corporate Rules
            </li>
          </ul>

          <p className="mt-4">
            You may request copies of the safeguards we use by contacting our Data Protection Officer.
          </p>
        </div>
      </div>

      {/* Security Measures */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Security Measures</h2>

        <div className="space-y-3 text-gray-700">
          <p>
            In compliance with GDPR Article 32, we have implemented appropriate technical and
            organizational measures to ensure a level of security appropriate to the risk, including:
          </p>

          <div className="grid md:grid-cols-2 gap-4 mt-4">
            <ul className="list-disc list-inside space-y-2 text-sm">
              <li>Pseudonymization and encryption of personal data</li>
              <li>Regular security testing and assessments</li>
              <li>Access controls and authentication</li>
              <li>Secure data transmission (HTTPS/TLS)</li>
            </ul>
            <ul className="list-disc list-inside space-y-2 text-sm">
              <li>Data backup and recovery procedures</li>
              <li>Incident response and breach notification procedures</li>
              <li>Employee training on data protection</li>
              <li>Regular review and updating of security measures</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Data Breach Notification */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <div className="flex items-center space-x-3 mb-4">
          <AlertCircle className="w-6 h-6 text-black" />
          <h2 className="text-2xl font-bold text-black">Data Breach Notification</h2>
        </div>

        <div className="space-y-3 text-gray-700">
          <p>
            In accordance with GDPR Article 33 and 34, in the event of a personal data breach that is
            likely to result in a risk to your rights and freedoms, we will:
          </p>

          <ul className="list-disc list-inside ml-4 space-y-2">
            <li>
              Notify the relevant supervisory authority without undue delay and, where feasible, within
              72 hours of becoming aware of the breach
            </li>
            <li>
              Notify affected data subjects without undue delay if the breach is likely to result in a
              high risk to their rights and freedoms
            </li>
            <li>
              Document the breach, including its facts, effects, and remedial actions taken
            </li>
          </ul>
        </div>
      </div>

      {/* Cookies */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Cookies and Tracking</h2>

        <div className="space-y-3 text-gray-700">
          <p>
            We use cookies and similar tracking technologies in compliance with GDPR and the ePrivacy
            Directive. For detailed information about the cookies we use and your choices, please refer
            to our{' '}
            <Link to="/privacy" className="text-green-900 hover:text-green-800 font-medium">
              Privacy Policy
            </Link>
            .
          </p>

          <p className="mt-3">
            You can control cookie preferences through your browser settings. However, blocking certain
            cookies may affect the functionality of the Service.
          </p>
        </div>
      </div>

      {/* Supervisory Authority */}
      <div className="bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-8 mb-6">
        <h2 className="text-2xl font-bold text-black mb-4">Right to Lodge a Complaint</h2>

        <div className="space-y-3 text-gray-700">
          <p>
            You have the right to lodge a complaint with a supervisory authority, in particular in the
            EU member state of your habitual residence, place of work, or place of the alleged
            infringement, if you believe that the processing of your personal data violates GDPR.
          </p>

          <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4 mt-4">
            <p className="font-semibold text-black mb-2">French Supervisory Authority (CNIL)</p>
            <p className="text-sm">
              <strong>Commission Nationale de l'Informatique et des Libertés (CNIL)</strong>
            </p>
            <p className="text-sm">3 Place de Fontenoy - TSA 80715</p>
            <p className="text-sm">75334 PARIS CEDEX 07, France</p>
            <p className="text-sm">
              Website:{' '}
              <a
                href="https://www.cnil.fr"
                target="_blank"
                rel="noopener noreferrer"
                className="text-green-900 hover:text-green-800 font-medium"
              >
                www.cnil.fr
              </a>
            </p>
          </div>
        </div>
      </div>

      {/* Contact */}
      <div className="bg-green-50 border-2 border-green-700 rounded-lg shadow-custom-md p-8 mb-8">
        <h2 className="text-2xl font-bold text-black mb-4">Contact Us</h2>
        <p className="text-gray-700 mb-4">
          For any questions about our GDPR compliance or to exercise your rights, please contact:
        </p>
        <div className="space-y-2 text-gray-700">
          <p>
            <strong>Data Protection Officer:</strong>{' '}
            <a href="mailto:dpo@montimage.eu" className="text-green-900 hover:text-green-800 font-medium">
              dpo@montimage.eu
            </a>
          </p>
          <p>
            <strong>General Inquiries:</strong>{' '}
            <a href="mailto:contact@montimage.eu" className="text-green-900 hover:text-green-800 font-medium">
              contact@montimage.eu
            </a>
          </p>
          <p>
            <strong>Address:</strong> 39 rue Bobillot, 75013 Paris, France
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

export default GDPR
