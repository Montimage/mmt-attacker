import { Info, AlertTriangle, CheckCircle, XCircle } from 'lucide-react'

function Alert({
  children,
  variant = 'info',
  className = '',
  ...props
}) {
  const variants = {
    info: {
      containerClass: 'bg-gray-50 border-gray-300 text-gray-800',
      icon: <Info className="w-5 h-5 text-gray-700" />,
    },
    warning: {
      containerClass: 'bg-gray-100 border-gray-400 text-gray-900',
      icon: <AlertTriangle className="w-5 h-5 text-gray-800" />,
    },
    success: {
      containerClass: 'bg-green-50 border-green-700 text-gray-900',
      icon: <CheckCircle className="w-5 h-5 text-green-900" />,
    },
    error: {
      containerClass: 'bg-gray-50 border-gray-600 text-gray-900',
      icon: <XCircle className="w-5 h-5 text-gray-700" />,
    },
  }

  const { containerClass, icon } = variants[variant]

  return (
    <div
      className={`flex items-start space-x-3 p-4 border-2 rounded-lg ${containerClass} ${className}`}
      {...props}
    >
      <div className="flex-shrink-0 mt-0.5">{icon}</div>
      <div className="flex-1">{children}</div>
    </div>
  )
}

export default Alert
