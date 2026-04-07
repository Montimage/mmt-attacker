/**
 * Parameter Validation Utilities
 * Provides validation functions for attack parameters
 */

/**
 * Validate IPv4 address
 */
export const validateIPv4 = (ip) => {
  if (!ip || typeof ip !== 'string') {
    return { valid: false, error: 'IP address is required' }
  }

  const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/

  if (!ipv4Regex.test(ip.trim())) {
    return { valid: false, error: 'Invalid IPv4 address format' }
  }

  return { valid: true }
}

/**
 * Validate IPv6 address
 */
export const validateIPv6 = (ip) => {
  if (!ip || typeof ip !== 'string') {
    return { valid: false, error: 'IPv6 address is required' }
  }

  // Simplified IPv6 validation
  const ipv6Regex = /^(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))$/

  if (!ipv6Regex.test(ip.trim())) {
    return { valid: false, error: 'Invalid IPv6 address format' }
  }

  return { valid: true }
}

/**
 * Validate port number (1-65535)
 */
export const validatePort = (port) => {
  const portNum = parseInt(port, 10)

  if (isNaN(portNum)) {
    return { valid: false, error: 'Port must be a number' }
  }

  if (portNum < 1 || portNum > 65535) {
    return { valid: false, error: 'Port must be between 1 and 65535' }
  }

  return { valid: true }
}

/**
 * Validate URL
 */
export const validateURL = (url) => {
  if (!url || typeof url !== 'string') {
    return { valid: false, error: 'URL is required' }
  }

  try {
    const urlObj = new URL(url)
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      return { valid: false, error: 'URL must use HTTP or HTTPS protocol' }
    }
    return { valid: true }
  } catch (e) {
    return { valid: false, error: 'Invalid URL format' }
  }
}

/**
 * Validate file path
 */
export const validateFilePath = (path) => {
  if (!path || typeof path !== 'string') {
    return { valid: false, error: 'File path is required' }
  }

  // Basic path validation
  const trimmedPath = path.trim()

  if (trimmedPath.length === 0) {
    return { valid: false, error: 'File path cannot be empty' }
  }

  // Check for invalid characters (simplified)
  const invalidChars = /[<>"|?*\x00-\x1F]/
  if (invalidChars.test(trimmedPath)) {
    return { valid: false, error: 'File path contains invalid characters' }
  }

  return { valid: true }
}

/**
 * Validate JSON string
 */
export const validateJSON = (jsonString) => {
  if (!jsonString || typeof jsonString !== 'string') {
    return { valid: true } // Empty JSON is valid
  }

  const trimmed = jsonString.trim()
  if (trimmed.length === 0) {
    return { valid: true } // Empty is valid
  }

  try {
    JSON.parse(trimmed)
    return { valid: true }
  } catch (e) {
    return { valid: false, error: 'Invalid JSON format: ' + e.message }
  }
}

/**
 * Validate number within range
 */
export const validateNumberRange = (value, min, max) => {
  const num = parseFloat(value)

  if (isNaN(num)) {
    return { valid: false, error: 'Must be a valid number' }
  }

  if (min !== undefined && num < min) {
    return { valid: false, error: `Must be at least ${min}` }
  }

  if (max !== undefined && num > max) {
    return { valid: false, error: `Must be at most ${max}` }
  }

  return { valid: true }
}

/**
 * Validate required field
 */
export const validateRequired = (value) => {
  if (value === null || value === undefined || value === '') {
    return { valid: false, error: 'This field is required' }
  }

  if (typeof value === 'string' && value.trim().length === 0) {
    return { valid: false, error: 'This field cannot be empty' }
  }

  return { valid: true }
}

/**
 * Validate email address
 */
export const validateEmail = (email) => {
  if (!email || typeof email !== 'string') {
    return { valid: false, error: 'Email address is required' }
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!emailRegex.test(email.trim())) {
    return { valid: false, error: 'Invalid email address format' }
  }

  return { valid: true }
}

/**
 * Validate hostname
 */
export const validateHostname = (hostname) => {
  if (!hostname || typeof hostname !== 'string') {
    return { valid: false, error: 'Hostname is required' }
  }

  // Allow hostnames and IP addresses
  const hostnameRegex = /^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$/

  const trimmed = hostname.trim()

  // Check if it's an IP address
  const ipValidation = validateIPv4(trimmed)
  if (ipValidation.valid) {
    return { valid: true }
  }

  // Check if it's a valid hostname
  if (!hostnameRegex.test(trimmed)) {
    return { valid: false, error: 'Invalid hostname format' }
  }

  return { valid: true }
}

/**
 * Validate interface name (e.g., eth0, wlan0)
 */
export const validateInterface = (interfaceName) => {
  if (!interfaceName || typeof interfaceName !== 'string') {
    return { valid: false, error: 'Interface name is required' }
  }

  const interfaceRegex = /^[a-zA-Z0-9_-]+$/

  if (!interfaceRegex.test(interfaceName.trim())) {
    return { valid: false, error: 'Invalid interface name' }
  }

  return { valid: true }
}

/**
 * Validate MAC address
 */
export const validateMAC = (mac) => {
  if (!mac || typeof mac !== 'string') {
    return { valid: false, error: 'MAC address is required' }
  }

  // Supports formats: 00:11:22:33:44:55, 00-11-22-33-44-55, 001122334455
  const macRegex = /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|^([0-9A-Fa-f]{12})$/

  if (!macRegex.test(mac.trim())) {
    return { valid: false, error: 'Invalid MAC address format' }
  }

  return { valid: true }
}

/**
 * Validate port range (e.g., "80-443")
 */
export const validatePortRange = (portRange) => {
  if (!portRange || typeof portRange !== 'string') {
    return { valid: false, error: 'Port range is required' }
  }

  const trimmed = portRange.trim()

  // Check if it's a single port
  if (/^\d+$/.test(trimmed)) {
    return validatePort(trimmed)
  }

  // Check if it's a range
  const rangeMatch = trimmed.match(/^(\d+)-(\d+)$/)
  if (!rangeMatch) {
    return { valid: false, error: 'Invalid port range format (use: 80-443)' }
  }

  const [, startPort, endPort] = rangeMatch
  const startValidation = validatePort(startPort)
  const endValidation = validatePort(endPort)

  if (!startValidation.valid) {
    return { valid: false, error: `Start port: ${startValidation.error}` }
  }

  if (!endValidation.valid) {
    return { valid: false, error: `End port: ${endValidation.error}` }
  }

  if (parseInt(startPort) >= parseInt(endPort)) {
    return { valid: false, error: 'Start port must be less than end port' }
  }

  return { valid: true }
}

/**
 * Main validation function that routes to appropriate validator
 */
export const validateParameter = (value, validationType, paramConfig = {}) => {
  // Handle required check first
  if (paramConfig.required) {
    const requiredCheck = validateRequired(value)
    if (!requiredCheck.valid) {
      return requiredCheck
    }
  }

  // If value is empty and not required, it's valid
  if (!paramConfig.required && (value === '' || value === null || value === undefined)) {
    return { valid: true }
  }

  // Route to appropriate validator
  switch (validationType) {
    case 'ipv4':
      return validateIPv4(value)
    case 'ipv6':
      return validateIPv6(value)
    case 'port':
      return validatePort(value)
    case 'url':
      return validateURL(value)
    case 'filepath':
      return validateFilePath(value)
    case 'json':
      return validateJSON(value)
    case 'email':
      return validateEmail(value)
    case 'hostname':
      return validateHostname(value)
    case 'interface':
      return validateInterface(value)
    case 'mac':
      return validateMAC(value)
    case 'portrange':
      return validatePortRange(value)
    case 'number':
      return validateNumberRange(value, paramConfig.min, paramConfig.max)
    default:
      // No specific validation, just check if required
      return { valid: true }
  }
}

/**
 * Validate all parameters for a form
 */
export const validateForm = (parameters, parameterDefinitions) => {
  const errors = {}
  let isValid = true

  parameterDefinitions.forEach(paramDef => {
    const value = parameters[paramDef.name]
    const validation = validateParameter(value, paramDef.validation, {
      required: paramDef.required,
      min: paramDef.min,
      max: paramDef.max
    })

    if (!validation.valid) {
      errors[paramDef.name] = validation.error
      isValid = false
    }
  })

  return {
    isValid,
    errors
  }
}

/**
 * Generate error message for validation
 */
export const getErrorMessage = (fieldName, validationResult) => {
  if (validationResult.valid) {
    return null
  }
  return validationResult.error || `${fieldName} is invalid`
}
