function Input({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  error,
  helpText,
  className = '',
  ...props
}) {
  const inputClasses = `w-full px-4 py-2 border-2 rounded-lg shadow-custom focus:outline-none focus:shadow-custom-md focus:border-black transition-all bg-white ${
    error ? 'border-gray-500 focus:border-black' : 'border-gray-400 focus:border-black'
  } ${className}`

  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-semibold text-gray-900 mb-2">
          {label}
          {required && <span className="text-black ml-1">*</span>}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={inputClasses}
        {...props}
      />
      {helpText && (
        <p className="mt-1 text-sm text-gray-600">{helpText}</p>
      )}
      {error && (
        <p className="mt-1 text-sm text-black font-semibold">{error}</p>
      )}
    </div>
  )
}

export default Input
