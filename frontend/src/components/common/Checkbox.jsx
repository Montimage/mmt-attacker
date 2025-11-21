function Checkbox({
  label,
  checked,
  onChange,
  helpText,
  className = '',
  ...props
}) {
  return (
    <div className={`mb-4 ${className}`}>
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          className="w-5 h-5 mt-0.5 border-2 border-gray-300 rounded focus:ring-2 focus:ring-green-200 text-green-900 transition-colors"
          {...props}
        />
        {label && (
          <label className="ml-3 text-sm font-medium text-gray-700 cursor-pointer select-none">
            {label}
          </label>
        )}
      </div>
      {helpText && (
        <p className="mt-1 ml-8 text-sm text-gray-500">{helpText}</p>
      )}
    </div>
  )
}

export default Checkbox
