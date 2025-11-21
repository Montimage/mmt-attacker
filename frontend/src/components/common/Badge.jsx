function Badge({
  children,
  variant = 'default',
  className = '',
  ...props
}) {
  const variants = {
    default: 'bg-gray-100 text-gray-800 border-gray-400',
    primary: 'bg-black text-white border-black',
    secondary: 'bg-gray-700 text-white border-gray-800',
    outline: 'bg-white text-gray-900 border-gray-400',
    success: 'bg-white text-green-600 border-gray-400',
  }

  const classes = `inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full border ${variants[variant]} ${className}`

  return (
    <span className={classes} {...props}>
      {children}
    </span>
  )
}

export default Badge
