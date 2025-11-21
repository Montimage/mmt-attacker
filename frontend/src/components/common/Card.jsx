function Card({
  children,
  hover = false,
  className = '',
  onClick,
  ...props
}) {
  const baseClasses = 'bg-white border-2 border-gray-300 rounded-lg shadow-custom-md p-6'
  const hoverClasses = hover ? 'hover:shadow-custom-lg hover:border-gray-400 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer' : ''
  const classes = `${baseClasses} ${hoverClasses} ${className}`

  return (
    <div className={classes} onClick={onClick} {...props}>
      {children}
    </div>
  )
}

export default Card
