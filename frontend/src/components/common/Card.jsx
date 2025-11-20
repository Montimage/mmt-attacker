function Card({
  children,
  hover = false,
  className = '',
  onClick,
  ...props
}) {
  const baseClasses = 'bg-white border-2 border-gray-200 rounded-lg shadow-custom p-6'
  const hoverClasses = hover ? 'hover:shadow-custom-lg hover:border-gray-300 transition-all duration-200 cursor-pointer' : ''
  const classes = `${baseClasses} ${hoverClasses} ${className}`

  return (
    <div className={classes} onClick={onClick} {...props}>
      {children}
    </div>
  )
}

export default Card
