function Badge({
  children,
  variant = 'default',
  className = '',
  ...props
}) {
  const variants = {
    default: 'bg-gray-100 text-gray-800 border-gray-300',
    primary: 'bg-green-900 text-white border-green-800',
    secondary: 'bg-gray-700 text-white border-gray-600',
    outline: 'bg-transparent text-green-900 border-green-900',
  }

  const classes = `inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full border ${variants[variant]} ${className}`

  return (
    <span className={classes} {...props}>
      {children}
    </span>
  )
}

export default Badge
