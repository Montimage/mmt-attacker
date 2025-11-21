/**
 * Command Generator Utility
 * Generates Python CLI commands for MMT-Attacker from attack parameters
 */

/**
 * Convert camelCase to kebab-case for CLI arguments
 * @param {string} str - Parameter name in camelCase
 * @returns {string} - Parameter name in kebab-case
 */
const camelToKebab = (str) => {
  return str.replace(/([A-Z])/g, '-$1').toLowerCase()
}

/**
 * Format a parameter value based on its type
 * @param {Object} param - Parameter definition
 * @param {*} value - Parameter value
 * @returns {string|null} - Formatted CLI argument or null if should be omitted
 */
const formatParameter = (param, value) => {
  const argName = `--${camelToKebab(param.name)}`

  // Handle checkbox/boolean parameters
  if (param.type === 'checkbox') {
    return value ? argName : null
  }

  // Skip empty values (except for number 0)
  if (value === undefined || value === null || value === '' ||
      (Array.isArray(value) && value.length === 0)) {
    return null
  }

  // Handle number parameters
  if (param.type === 'number') {
    return `${argName} ${value}`
  }

  // Handle textarea (multi-line text)
  if (param.type === 'textarea') {
    // For multi-line content, we'll format it as a string with escaped newlines
    const escapedValue = value.replace(/\n/g, '\\n').replace(/"/g, '\\"')
    return `${argName} "${escapedValue}"`
  }

  // Handle select and text parameters
  // Escape quotes in the value
  const escapedValue = String(value).replace(/"/g, '\\"')
  return `${argName} "${escapedValue}"`
}

/**
 * Generate Python command for executing an attack
 * @param {string} attackId - Attack identifier (e.g., 'arp-spoofing')
 * @param {Object} scenario - Scenario object with parameters
 * @param {Object} parameterValues - Current parameter values
 * @returns {string} - Complete Python command
 */
export const generatePythonCommand = (attackId, scenario, parameterValues = {}) => {
  // Start with base command
  let command = `python src/cli.py ${attackId}`

  // Process each parameter
  const args = []

  if (scenario && scenario.parameters) {
    scenario.parameters.forEach(param => {
      // Get value from user input or default value
      const value = parameterValues[param.name] !== undefined
        ? parameterValues[param.name]
        : param.defaultValue

      // Format the parameter
      const formattedArg = formatParameter(param, value)

      // Add to args if not null
      if (formattedArg !== null) {
        args.push(formattedArg)
      }
    })
  }

  // Format command with line breaks for readability if there are multiple args
  if (args.length > 0) {
    if (args.length <= 2) {
      // Short commands on one line
      command += ' ' + args.join(' ')
    } else {
      // Long commands with line continuations
      command += ' \\\n    ' + args.join(' \\\n    ')
    }
  }

  return command
}

/**
 * Generate example command with placeholder values
 * @param {string} attackId - Attack identifier
 * @param {Object} scenario - Scenario object with parameters
 * @returns {string} - Example Python command with placeholders
 */
export const generateExampleCommand = (attackId, scenario) => {
  const exampleValues = {}

  if (scenario && scenario.parameters) {
    scenario.parameters.forEach(param => {
      // Use placeholder or default value
      if (param.placeholder) {
        exampleValues[param.name] = param.placeholder
      } else if (param.defaultValue !== undefined) {
        exampleValues[param.name] = param.defaultValue
      } else {
        // Generate appropriate placeholder based on type
        switch (param.type) {
          case 'text':
            exampleValues[param.name] = param.validation === 'ipv4'
              ? '192.168.1.100'
              : param.validation === 'url'
              ? 'http://example.com'
              : 'value'
            break
          case 'number':
            exampleValues[param.name] = 100
            break
          case 'checkbox':
            exampleValues[param.name] = true
            break
          case 'textarea':
            exampleValues[param.name] = 'line1\nline2'
            break
          case 'select':
            exampleValues[param.name] = param.options?.[0]?.value || 'value'
            break
          default:
            exampleValues[param.name] = 'value'
        }
      }
    })
  }

  return generatePythonCommand(attackId, scenario, exampleValues)
}

/**
 * Get parameter mapping explanation
 * @param {Object} scenario - Scenario object with parameters
 * @returns {Array} - Array of parameter mappings
 */
export const getParameterMapping = (scenario) => {
  if (!scenario || !scenario.parameters) {
    return []
  }

  return scenario.parameters.map(param => ({
    uiName: param.label,
    cliArg: `--${camelToKebab(param.name)}`,
    type: param.type,
    required: param.required || false,
    description: param.helpText || ''
  }))
}
