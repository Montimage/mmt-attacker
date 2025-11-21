import { Info, AlertTriangle, CheckCircle, XCircle } from 'lucide-react'

function Alert({
  children,
  variant = 'info',
  className = '',
  ...props
}) {
  const variants = {
    info: {
      containerClass: 'bg-gray-50 border-gray-400 text-gray-900 shadow-custom',
      icon: <Info className="w-5 h-5 text-gray-700" />,
    },
    warning: {
      containerClass: 'bg-white border-gray-500 text-gray-900 shadow-custom-md',
      icon: <AlertTriangle className="w-5 h-5 text-black" />,
    },
    success: {
      containerClass: 'bg-white border-gray-400 text-gray-900 shadow-custom',
      icon: <CheckCircle className="w-5 h-5 text-green-600" />,
    },
    error: {
      containerClass: 'bg-white border-gray-500 text-gray-900 shadow-custom-md',
      icon: <XCircle className="w-5 h-5 text-black" />,
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
