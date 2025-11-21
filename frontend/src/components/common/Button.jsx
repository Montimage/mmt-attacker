function Button({
  children,
  variant = 'primary',
  onClick,
  disabled = false,
  loading = false,
  type = 'button',
  className = '',
  ...props
}) {
  const baseClasses = 'px-6 py-3 rounded-lg border-2 font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed'

  const variants = {
    primary: 'bg-white text-black border-black shadow-custom-md hover:shadow-custom-lg hover:-translate-y-0.5 active:translate-y-0 active:shadow-custom',
    secondary: 'bg-white text-gray-900 border-gray-400 shadow-custom hover:border-gray-600 hover:shadow-custom-md hover:-translate-y-0.5 active:translate-y-0 active:shadow-custom',
    outline: 'bg-white text-gray-900 border-gray-300 shadow-custom hover:border-gray-500 hover:shadow-custom-md hover:-translate-y-0.5 active:translate-y-0'
  }

  const classes = `${baseClasses} ${variants[variant]} ${className}`

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={classes}
      {...props}
    >
      {loading ? (
        <span className="flex items-center justify-center">
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </span>
      ) : children}
    </button>
  )
}

export default Button
