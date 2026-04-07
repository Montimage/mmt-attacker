import { HelpCircle } from 'lucide-react'
import Input from '../common/Input'
import Select from '../common/Select'
import Checkbox from '../common/Checkbox'
import { validateParameter } from '../../utils/parameterValidator'

function AttackParameters({ parameters, values, onChange, errors = {} }) {
  const handleChange = (paramName, value) => {
    onChange(paramName, value)
  }

  const handleBlur = (param) => {
    // Validate on blur
    const validation = validateParameter(values[param.name], param.validation, {
      required: param.required,
      min: param.min,
      max: param.max
    })

    if (!validation.valid) {
      onChange(param.name, values[param.name], validation.error)
    }
  }

  const renderParameter = (param) => {
    const commonProps = {
      label: param.label,
      value: values[param.name] || param.defaultValue || '',
      onChange: (e) => handleChange(param.name, e.target.value),
      onBlur: () => handleBlur(param),
      required: param.required,
      placeholder: param.placeholder,
      helpText: param.helpText,
      error: errors[param.name]
    }

    switch (param.type) {
      case 'select':
        return (
          <Select
            key={param.name}
            {...commonProps}
            options={param.options || []}
          />
        )

      case 'textarea':
        return (
          <div key={param.name} className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {param.label}
              {param.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            <textarea
              value={values[param.name] || param.defaultValue || ''}
              onChange={(e) => handleChange(param.name, e.target.value)}
              onBlur={() => handleBlur(param)}
              placeholder={param.placeholder}
              rows={4}
              className={`w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-200 transition-all ${
                errors[param.name] ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-green-700'
              }`}
            />
            {param.helpText && (
              <p className="mt-1 text-sm text-gray-500">{param.helpText}</p>
            )}
            {errors[param.name] && (
              <p className="mt-1 text-sm text-red-600">{errors[param.name]}</p>
            )}
          </div>
        )

      case 'checkbox':
        return (
          <Checkbox
            key={param.name}
            label={param.label}
            checked={values[param.name] === true || values[param.name] === 'true'}
            onChange={(e) => handleChange(param.name, e.target.checked)}
            helpText={param.helpText}
          />
        )

      case 'number':
        return (
          <Input
            key={param.name}
            {...commonProps}
            type="number"
            min={param.min}
            max={param.max}
          />
        )

      default:
        return <Input key={param.name} {...commonProps} type={param.type || 'text'} />
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-lg font-semibold text-black">Parameters</h4>
        <div className="flex items-center text-sm text-gray-500">
          <span className="text-red-500 mr-1">*</span>
          <span>Required field</span>
        </div>
      </div>

      {parameters.map(renderParameter)}
    </div>
  )
}

export default AttackParameters
