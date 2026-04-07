function Badge({
  children,
  variant = 'default',
  className = '',
  ...props
}) {
  const variants = {
    default: 'bg-gray-800 text-gray-200 border-gray-600',
    primary: 'bg-green-700 text-white border-green-600',
    secondary: 'bg-gray-700 text-gray-100 border-gray-600',
    outline: 'bg-gray-900 text-gray-300 border-gray-600',
    success: 'bg-green-950 text-green-400 border-green-700',
  }

  const classes = `inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full border ${variants[variant]} ${className}`

  return (
    <span className={classes} {...props}>
      {children}
    </span>
  )
}

export default Badge
