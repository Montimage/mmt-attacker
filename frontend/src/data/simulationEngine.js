/**
 * MMT-Attacker Simulation Engine
 * Generates realistic attack simulation results based on user inputs
 */

import { getAttackById } from './attacksData'

/**
 * Generate random number between min and max
 */
const random = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min

/**
 * Generate random IP address
 */
const randomIp = () => `${random(1, 254)}.${random(1, 254)}.${random(1, 254)}.${random(1, 254)}`

/**
 * Format timestamp
 */
const timestamp = () => {
  const now = new Date()
  return now.toISOString().split('T')[1].split('.')[0]
}

/**
 * Simulate ARP Spoofing attack
 */
const simulateArpSpoofing = (scenarioId, params) => {
  const timeline = []
  const packetsSent = random(50, 200)
  const bytesIntercepted = random(10000, 100000)
  const packetsIntercepted = random(50, 500)

  timeline.push({ time: 0, message: 'Initializing ARP spoofing attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}`, type: 'info' })
  timeline.push({ time: 600, message: `Gateway: ${params.gateway}`, type: 'info' })
  timeline.push({ time: 700, message: `Interface: ${params.interface}`, type: 'info' })

  if (params.bidirectional) {
    timeline.push({ time: 1000, message: 'Setting up bidirectional poisoning...', type: 'progress' })
  }

  timeline.push({ time: 1500, message: 'Sending ARP poisoning packets...', type: 'progress' })
  timeline.push({ time: 2000, message: `ARP cache poisoned successfully`, type: 'success' })
  timeline.push({ time: 2500, message: `Packets sent: ${packetsSent}`, type: 'info' })
  timeline.push({ time: 3000, message: `Traffic interception active`, type: 'success' })
  timeline.push({ time: 3500, message: `Intercepted ${packetsIntercepted} packets (${bytesIntercepted} bytes)`, type: 'info' })

  if (params.verify) {
    timeline.push({ time: 4000, message: 'Verifying attack effectiveness...', type: 'progress' })
    timeline.push({ time: 4500, message: 'Verification: ARP poisoning successful', type: 'success' })
  }

  if (params.packetLog) {
    timeline.push({ time: 5000, message: `Packets logged to: ${params.packetLog}`, type: 'info' })
  }

  return {
    success: true,
    timeline,
    metrics: {
      arpPacketsSent: packetsSent,
      trafficIntercepted: `${(bytesIntercepted / 1024).toFixed(2)} KB`,
      packetsIntercepted: packetsIntercepted,
      duration: '5.0s',
      poisoningSuccess: true
    },
    explanation: {
      happening: 'ARP cache has been poisoned on both the victim and gateway. Traffic between them is now flowing through the attacker\'s machine, allowing full interception and monitoring.',
      highlights: [
        'ARP poisoning active',
        'Traffic successfully redirected',
        `${packetsIntercepted} packets intercepted`
      ],
      interpretation: `The attack successfully poisoned the ARP caches of both the target (${params.target}) and gateway (${params.gateway}). All traffic between them is now being intercepted. ${params.bidirectional ? 'Bidirectional interception is active.' : 'Unidirectional interception is active.'}`
    }
  }
}

/**
 * Simulate SYN Flood attack
 */
const simulateSynFlood = (scenarioId, params) => {
  const timeline = []
  const threads = params.threads || 4
  const packetsPerThread = random(1000, 5000)
  const totalPackets = threads * packetsPerThread
  const avgResponseTime = random(500, 3000)

  timeline.push({ time: 0, message: 'Initializing SYN flood attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}:${params.port || params.portRange}`, type: 'info' })
  timeline.push({ time: 700, message: `Threads: ${threads}`, type: 'info' })
  timeline.push({ time: 900, message: `Source IP: ${params.sourceIp || 'random'}`, type: 'info' })
  timeline.push({ time: 1200, message: 'Generating SYN packets...', type: 'progress' })
  timeline.push({ time: 1800, message: 'Flooding target with SYN packets...', type: 'progress' })
  timeline.push({ time: 2500, message: `Sent ${Math.floor(totalPackets * 0.3)} packets...`, type: 'info' })
  timeline.push({ time: 3500, message: `Sent ${Math.floor(totalPackets * 0.6)} packets...`, type: 'info' })
  timeline.push({ time: 4500, message: `Sent ${totalPackets} packets`, type: 'success' })
  timeline.push({ time: 5000, message: `Target response time increasing: ${avgResponseTime}ms`, type: 'warning' })
  timeline.push({ time: 5500, message: 'Connection table filling up...', type: 'warning' })
  timeline.push({ time: 6000, message: 'Service degradation detected', type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      totalPackets: totalPackets,
      threads: threads,
      avgResponseTime: `${avgResponseTime}ms`,
      targetPort: params.port || params.portRange,
      duration: '6.0s',
      connectionAttempts: random(500, 2000)
    },
    explanation: {
      happening: 'SYN packets are flooding the target server, filling up its connection table with half-open connections. Each SYN packet forces the server to allocate resources and wait for an ACK that never arrives.',
      highlights: [
        `${totalPackets} SYN packets sent`,
        'Connection table saturating',
        `Response time degraded to ${avgResponseTime}ms`
      ],
      interpretation: `The SYN flood successfully overwhelmed the target at ${params.target}. With ${threads} parallel threads, the attack sent ${totalPackets} SYN packets, causing the server's connection table to fill up. Response times increased to ${avgResponseTime}ms, indicating service degradation.`
    }
  }
}

/**
 * Simulate DNS Amplification attack
 */
const simulateDnsAmplification = (scenarioId, params) => {
  const timeline = []
  const dnsServers = scenarioId === 'distributed-amplification' ?
    (params.dnsServers?.split('\n').filter(s => s.trim()).length || 3) : 1
  const amplificationFactor = random(50, 100)
  const queriesSent = random(100, 500)
  const querySize = 60
  const responseSize = querySize * amplificationFactor
  const totalTraffic = (queriesSent * responseSize) / 1024 / 1024

  timeline.push({ time: 0, message: 'Initializing DNS amplification attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}`, type: 'info' })
  timeline.push({ time: 700, message: `DNS servers: ${dnsServers}`, type: 'info' })
  timeline.push({ time: 900, message: `Query domain: ${params.queryDomain || 'example.com'}`, type: 'info' })

  if (params.verifyAmplification) {
    timeline.push({ time: 1200, message: 'Verifying amplification factor...', type: 'progress' })
    timeline.push({ time: 1800, message: `Amplification factor: ${amplificationFactor}x`, type: 'success' })
  }

  timeline.push({ time: 2000, message: 'Sending DNS queries with spoofed source...', type: 'progress' })
  timeline.push({ time: 2800, message: `Query size: ${querySize} bytes`, type: 'info' })
  timeline.push({ time: 3000, message: `Response size: ${responseSize} bytes`, type: 'info' })
  timeline.push({ time: 3500, message: `Sent ${Math.floor(queriesSent * 0.5)} queries...`, type: 'info' })
  timeline.push({ time: 4500, message: `Sent ${queriesSent} queries`, type: 'success' })
  timeline.push({ time: 5000, message: `Amplified traffic: ${totalTraffic.toFixed(2)} MB`, type: 'success' })
  timeline.push({ time: 5500, message: `Responses converging on target`, type: 'warning' })

  return {
    success: true,
    timeline,
    metrics: {
      dnsServers: dnsServers,
      queriesSent: queriesSent,
      amplificationFactor: `${amplificationFactor}x`,
      querySize: `${querySize} bytes`,
      responseSize: `${responseSize} bytes`,
      totalTrafficAmplified: `${totalTraffic.toFixed(2)} MB`,
      duration: '5.5s'
    },
    explanation: {
      happening: `DNS servers are sending large responses to the victim's IP address. Each small query (${querySize} bytes) generates a large response (${responseSize} bytes), multiplying the attack traffic by ${amplificationFactor}x.`,
      highlights: [
        `${amplificationFactor}x amplification achieved`,
        `${totalTraffic.toFixed(2)} MB of traffic generated`,
        `Using ${dnsServers} DNS server(s)`
      ],
      interpretation: `The DNS amplification attack successfully leveraged ${dnsServers} DNS server(s) to amplify traffic toward ${params.target}. With an amplification factor of ${amplificationFactor}x, ${queriesSent} small queries generated ${totalTraffic.toFixed(2)} MB of response traffic directed at the victim.`
    }
  }
}

/**
 * Simulate Ping of Death attack
 */
const simulatePingOfDeath = (scenarioId, params) => {
  const timeline = []
  const targets = scenarioId === 'network-stress' ?
    (params.targets?.split('\n').filter(t => t.trim()).length || 1) : 1
  const packetSize = params.size || 65500
  const packetCount = params.count || 1
  const fragments = Math.ceil(packetSize / 1500)

  timeline.push({ time: 0, message: 'Initializing Ping of Death attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target(s): ${targets}`, type: 'info' })
  timeline.push({ time: 700, message: `Packet size: ${packetSize} bytes`, type: 'info' })
  timeline.push({ time: 900, message: `Fragments per packet: ${fragments}`, type: 'info' })
  timeline.push({ time: 1200, message: 'Generating oversized ICMP packets...', type: 'progress' })
  timeline.push({ time: 1800, message: 'Fragmenting packets...', type: 'progress' })

  for (let i = 1; i <= packetCount; i++) {
    const time = 2000 + (i * 800)
    timeline.push({ time, message: `Sending packet ${i}/${packetCount} (${fragments} fragments)...`, type: 'progress' })
  }

  if (params.verify) {
    timeline.push({ time: 3500, message: 'Testing target vulnerability...', type: 'progress' })
    const vulnerable = random(0, 100) > 70
    timeline.push({
      time: 4000,
      message: vulnerable ? 'Target appears vulnerable!' : 'Target appears patched/protected',
      type: vulnerable ? 'warning' : 'success'
    })
  }

  timeline.push({ time: 4500, message: `Sent ${packetCount} oversized packets`, type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      targets: targets,
      packetsSent: packetCount,
      packetSize: `${packetSize} bytes`,
      fragmentsPerPacket: fragments,
      totalFragments: packetCount * fragments,
      duration: '4.5s'
    },
    explanation: {
      happening: `Oversized ICMP packets (${packetSize} bytes) are being fragmented and sent to the target. When reassembled, these packets exceed the maximum allowed size, potentially causing buffer overflows or system crashes on vulnerable systems.`,
      highlights: [
        `${packetCount} oversized packets sent`,
        `${fragments} fragments per packet`,
        `Total size: ${packetSize} bytes`
      ],
      interpretation: `The attack sent ${packetCount} oversized ICMP packets to ${targets} target(s). Each packet was ${packetSize} bytes, requiring ${fragments} fragments for transmission. ${params.verify ? 'Vulnerability testing was performed.' : 'Use --verify to test for vulnerability.'}`
    }
  }
}

/**
 * Simulate HTTP DoS attack
 */
const simulateHttpDos = (scenarioId, params) => {
  const timeline = []
  const threads = params.threads || 10
  const requestsPerThread = random(100, 500)
  const totalRequests = threads * requestsPerThread
  const successRate = random(85, 98)
  const avgResponseTime = random(200, 2000)
  const statusCodes = {
    200: Math.floor(successRate),
    503: Math.floor((100 - successRate) * 0.7),
    500: Math.floor((100 - successRate) * 0.3)
  }

  timeline.push({ time: 0, message: 'Initializing HTTP DoS attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}`, type: 'info' })
  timeline.push({ time: 700, message: `Method: ${params.method || 'GET'}`, type: 'info' })
  timeline.push({ time: 900, message: `Threads: ${threads}`, type: 'info' })
  timeline.push({ time: 1200, message: 'Starting HTTP flood...', type: 'progress' })
  timeline.push({ time: 2000, message: `Sent ${Math.floor(totalRequests * 0.2)} requests...`, type: 'info' })
  timeline.push({ time: 3000, message: `Sent ${Math.floor(totalRequests * 0.5)} requests...`, type: 'info' })
  timeline.push({ time: 4000, message: `Response time increasing: ${avgResponseTime}ms`, type: 'warning' })
  timeline.push({ time: 5000, message: `Sent ${Math.floor(totalRequests * 0.8)} requests...`, type: 'info' })
  timeline.push({ time: 6000, message: `Sent ${totalRequests} requests`, type: 'success' })
  timeline.push({ time: 6500, message: `Success rate: ${successRate}%`, type: 'info' })
  timeline.push({ time: 7000, message: 'Server load significantly increased', type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      totalRequests: totalRequests,
      threads: threads,
      successRate: `${successRate}%`,
      avgResponseTime: `${avgResponseTime}ms`,
      statusCodes: statusCodes,
      duration: '7.0s'
    },
    explanation: {
      happening: `HTTP requests are flooding the web server from ${threads} parallel threads. The high volume is overwhelming the server's worker pools and consuming CPU/memory resources, causing response times to increase significantly.`,
      highlights: [
        `${totalRequests} HTTP requests sent`,
        `${successRate}% success rate`,
        `Response time: ${avgResponseTime}ms`
      ],
      interpretation: `The HTTP DoS attack sent ${totalRequests} ${params.method || 'GET'} requests to ${params.target} using ${threads} threads. The server's response time degraded to ${avgResponseTime}ms, with a success rate of ${successRate}%. ${statusCodes[503]} requests received 503 errors, indicating service overload.`
    }
  }
}

/**
 * Simulate Slowloris attack
 */
const simulateSlowloris = (scenarioId, params) => {
  const timeline = []
  const connections = params.connections || 100
  const connectionsEstablished = random(Math.floor(connections * 0.8), connections)
  const keepAliveInterval = params.interval || 30
  const serverLimit = random(150, 300)

  timeline.push({ time: 0, message: 'Initializing Slowloris attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}${params.ssl ? ' (HTTPS)' : ''}`, type: 'info' })
  timeline.push({ time: 700, message: `Target connections: ${connections}`, type: 'info' })
  timeline.push({ time: 900, message: `Keep-alive interval: ${keepAliveInterval}s`, type: 'info' })

  if (params.verifyVuln) {
    timeline.push({ time: 1200, message: 'Testing server vulnerability...', type: 'progress' })
    timeline.push({ time: 1800, message: `Server connection limit detected: ~${serverLimit}`, type: 'warning' })
    timeline.push({ time: 2000, message: 'Server appears vulnerable to Slowloris', type: 'success' })
  }

  timeline.push({ time: 2500, message: 'Opening connections...', type: 'progress' })
  timeline.push({ time: 3500, message: `Established ${Math.floor(connectionsEstablished * 0.5)} connections...`, type: 'info' })
  timeline.push({ time: 4500, message: `Established ${connectionsEstablished} connections`, type: 'success' })
  timeline.push({ time: 5000, message: 'Sending partial HTTP headers...', type: 'progress' })
  timeline.push({ time: 6000, message: 'Connections being held open...', type: 'info' })
  timeline.push({ time: 7000, message: `Sending keep-alive headers every ${keepAliveInterval}s`, type: 'info' })
  timeline.push({ time: 8000, message: `Connection pool filling: ${Math.floor((connectionsEstablished / serverLimit) * 100)}%`, type: 'warning' })
  timeline.push({ time: 9000, message: 'Server connection limit approaching', type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      targetConnections: connections,
      connectionsEstablished: connectionsEstablished,
      keepAliveInterval: `${keepAliveInterval}s`,
      serverConnectionLimit: serverLimit,
      connectionPoolUsage: `${Math.floor((connectionsEstablished / serverLimit) * 100)}%`,
      duration: '9.0s'
    },
    explanation: {
      happening: `${connectionsEstablished} partial HTTP connections are being held open by sending incomplete headers slowly. The server keeps these connections alive, waiting for the complete request. This exhausts the server's connection pool without completing any requests.`,
      highlights: [
        `${connectionsEstablished} connections held open`,
        `${Math.floor((connectionsEstablished / serverLimit) * 100)}% of server capacity used`,
        'Low bandwidth consumption'
      ],
      interpretation: `The Slowloris attack successfully established ${connectionsEstablished} partial connections to ${params.target}. These connections are consuming ${Math.floor((connectionsEstablished / serverLimit) * 100)}% of the server's connection pool (estimated limit: ${serverLimit}). The attack uses minimal bandwidth by sending keep-alive headers every ${keepAliveInterval} seconds.`
    }
  }
}

/**
 * Simulate SSH Brute Force attack
 */
const simulateSshBruteForce = (scenarioId, params) => {
  const timeline = []
  const passwords = scenarioId === 'multi-target' ?
    (params.passwords?.split('\n').filter(p => p.trim()).length || 10) :
    (params.wordlist?.split('\n').filter(p => p.trim()).length || 10)
  const targets = scenarioId === 'multi-target' ?
    (params.targets?.split('\n').filter(t => t.trim()).length || 1) : 1
  const totalAttempts = passwords * targets
  const successfulCracks = random(0, 100) > 85 ? random(1, targets) : 0
  const delay = params.delay || 2

  timeline.push({ time: 0, message: 'Initializing SSH brute force attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target(s): ${targets}`, type: 'info' })
  timeline.push({ time: 700, message: `Password list size: ${passwords}`, type: 'info' })
  timeline.push({ time: 900, message: `Delay between attempts: ${delay}s`, type: 'info' })
  timeline.push({ time: 1200, message: 'Starting brute force attempts...', type: 'progress' })

  let currentAttempt = 0
  for (let i = 0; i < Math.min(passwords, 5); i++) {
    currentAttempt++
    const time = 2000 + (i * 1000)
    timeline.push({ time, message: `Attempt ${currentAttempt}/${totalAttempts}: Testing password...`, type: 'progress' })
    timeline.push({ time: time + 300, message: 'Authentication failed', type: 'warning' })
  }

  if (successfulCracks > 0) {
    timeline.push({ time: 7000, message: `✓ Valid credentials found!`, type: 'success' })
    timeline.push({ time: 7500, message: `User: ${params.username || 'admin'} | Password: ********`, type: 'success' })
    if (params.stopOnSuccess) {
      timeline.push({ time: 8000, message: 'Stopping on successful crack', type: 'info' })
    }
  } else {
    timeline.push({ time: 7000, message: `Tested all ${totalAttempts} combinations`, type: 'info' })
    timeline.push({ time: 7500, message: 'No valid credentials found', type: 'warning' })
  }

  return {
    success: true,
    timeline,
    metrics: {
      targets: targets,
      totalAttempts: totalAttempts,
      successfulCracks: successfulCracks,
      attemptsDuration: `${totalAttempts * delay}s`,
      delay: `${delay}s`,
      duration: '8.0s'
    },
    explanation: {
      happening: `SSH authentication attempts are being made against ${targets} target(s) using a password wordlist. Each attempt tries to authenticate with the provided credentials, with a ${delay}-second delay between attempts to avoid triggering rate limits or account lockouts.`,
      highlights: [
        `${totalAttempts} authentication attempts`,
        successfulCracks > 0 ? `${successfulCracks} valid credential(s) found` : 'No credentials found',
        `${delay}s delay between attempts`
      ],
      interpretation: successfulCracks > 0 ?
        `The brute force attack successfully identified ${successfulCracks} valid credential(s) after ${totalAttempts} attempts across ${targets} target(s). The compromised accounts should be secured immediately with stronger passwords.` :
        `The brute force attack tested ${totalAttempts} password combinations across ${targets} target(s) but did not find valid credentials. The target systems appear to have strong passwords or the wordlist did not contain the correct passwords.`
    }
  }
}

/**
 * Simulate SQL Injection attack
 */
const simulateSqlInjection = (scenarioId, params) => {
  const timeline = []
  const riskLevel = params.risk || 1
  const level = params.level || 1
  const payloadsTested = riskLevel * level * random(10, 30)
  const vulnerable = random(0, 100) > (60 - (riskLevel * 10))
  const injectionType = vulnerable ? ['Error-based', 'Boolean-based', 'Time-based'][random(0, 2)] : null

  timeline.push({ time: 0, message: 'Initializing SQL injection scan...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}`, type: 'info' })
  timeline.push({ time: 700, message: `Parameter: ${params.parameter || 'auto-detect'}`, type: 'info' })
  timeline.push({ time: 900, message: `Database: ${params.dbms || 'mysql'}`, type: 'info' })
  timeline.push({ time: 1100, message: `Risk level: ${riskLevel}, Test level: ${level}`, type: 'info' })

  if (params.testForms) {
    timeline.push({ time: 1500, message: 'Scanning for injection points...', type: 'progress' })
    timeline.push({ time: 2000, message: `Found ${random(2, 5)} potential injection points`, type: 'info' })
  }

  timeline.push({ time: 2500, message: 'Testing SQL injection payloads...', type: 'progress' })
  timeline.push({ time: 3500, message: `Tested ${Math.floor(payloadsTested * 0.3)} payloads...`, type: 'info' })
  timeline.push({ time: 4500, message: `Tested ${Math.floor(payloadsTested * 0.6)} payloads...`, type: 'info' })
  timeline.push({ time: 5500, message: `Tested ${payloadsTested} payloads`, type: 'info' })

  if (vulnerable) {
    timeline.push({ time: 6000, message: '✓ SQL injection vulnerability detected!', type: 'success' })
    timeline.push({ time: 6500, message: `Injection type: ${injectionType}`, type: 'warning' })
    timeline.push({ time: 7000, message: 'Extracting database information...', type: 'progress' })
    timeline.push({ time: 7800, message: `Database: testdb, Tables: ${random(5, 20)}`, type: 'info' })
    timeline.push({ time: 8500, message: 'Sample data extracted successfully', type: 'success' })
  } else {
    timeline.push({ time: 6000, message: 'No SQL injection vulnerabilities detected', type: 'success' })
    timeline.push({ time: 6500, message: 'Input appears properly sanitized', type: 'info' })
  }

  return {
    success: true,
    timeline,
    metrics: {
      payloadsTested: payloadsTested,
      vulnerabilityFound: vulnerable,
      injectionType: injectionType || 'N/A',
      riskLevel: riskLevel,
      testLevel: level,
      dbms: params.dbms || 'mysql',
      duration: vulnerable ? '8.5s' : '6.5s'
    },
    explanation: {
      happening: vulnerable ?
        `SQL injection payloads successfully manipulated the database query. The ${injectionType} injection technique allowed extraction of database structure and data by injecting malicious SQL code into the ${params.parameter} parameter.` :
        `SQL injection payloads were tested but the application properly sanitizes user input. No vulnerabilities were detected in the tested parameters.`,
      highlights: vulnerable ? [
        `SQL injection vulnerability found!`,
        `Type: ${injectionType}`,
        `Database information extracted`
      ] : [
        'No vulnerabilities detected',
        `${payloadsTested} payloads tested`,
        'Input properly sanitized'
      ],
      interpretation: vulnerable ?
        `CRITICAL: SQL injection vulnerability discovered in the ${params.parameter} parameter. The ${injectionType} injection technique successfully bypassed input validation. Database structure and sample data were extracted. Immediate remediation required.` :
        `The application successfully defended against ${payloadsTested} SQL injection payloads. Input validation appears properly implemented for the tested parameters.`
    }
  }
}

/**
 * Simulate Credential Harvester attack
 */
const simulateCredentialHarvester = (scenarioId, params) => {
  const timeline = []
  const port = params.port || 8080
  const submissions = random(0, 15)
  const pageViews = random(submissions, submissions * 3)

  timeline.push({ time: 0, message: 'Initializing credential harvester...', type: 'info' })
  timeline.push({ time: 500, message: `Server port: ${port}`, type: 'info' })
  timeline.push({ time: 700, message: `SSL enabled: ${params.ssl ? 'Yes' : 'No'}`, type: 'info' })

  if (params.template) {
    timeline.push({ time: 1000, message: `Loading template: ${params.template}`, type: 'progress' })
  } else if (params.customForm) {
    timeline.push({ time: 1000, message: 'Loading custom form...', type: 'progress' })
  }

  timeline.push({ time: 1500, message: 'Starting web server...', type: 'progress' })
  timeline.push({ time: 2000, message: `Server running on ${params.ssl ? 'https' : 'http'}://localhost:${port}`, type: 'success' })
  timeline.push({ time: 2500, message: 'Phishing page active', type: 'success' })
  timeline.push({ time: 3000, message: 'Waiting for connections...', type: 'info' })

  if (submissions > 0) {
    for (let i = 1; i <= Math.min(submissions, 3); i++) {
      const time = 3500 + (i * 1500)
      timeline.push({ time, message: `Submission ${i}: Credentials captured`, type: 'success' })
      timeline.push({ time: time + 300, message: `  User redirected to: ${params.redirect || '[not set]'}`, type: 'info' })
    }

    if (params.logFile) {
      timeline.push({ time: 8000, message: `Credentials saved to: ${params.logFile}`, type: 'info' })
    }
  }

  timeline.push({ time: 9000, message: `Total page views: ${pageViews}`, type: 'info' })
  timeline.push({ time: 9500, message: `Total submissions: ${submissions}`, type: submissions > 0 ? 'success' : 'info' })

  return {
    success: true,
    timeline,
    metrics: {
      serverStatus: 'Running',
      port: port,
      ssl: params.ssl || false,
      pageViews: pageViews,
      submissions: submissions,
      successRate: pageViews > 0 ? `${((submissions / pageViews) * 100).toFixed(1)}%` : '0%',
      duration: '9.5s'
    },
    explanation: {
      happening: `A phishing server is running on port ${port}, hosting a ${params.template ? 'template-based' : 'custom'} credential harvesting page. When users submit the form, their credentials are captured${params.logFile ? ' and logged' : ''}${params.redirect ? ', then they are redirected to the legitimate site' : ''}.`,
      highlights: [
        `Server active on port ${port}`,
        `${submissions} credential submissions captured`,
        `${((submissions / Math.max(pageViews, 1)) * 100).toFixed(1)}% submission rate`
      ],
      interpretation: submissions > 0 ?
        `The phishing campaign captured ${submissions} credential submissions from ${pageViews} page views, achieving a ${((submissions / pageViews) * 100).toFixed(1)}% success rate. This demonstrates the effectiveness of social engineering attacks and highlights the need for user security awareness training.` :
        `The phishing page received ${pageViews} views but no credential submissions. This could indicate effective user awareness training or insufficient traffic to the phishing page.`
    }
  }
}

/**
 * Simulate PCAP Replay attack
 */
const simulatePcapReplay = (scenarioId, params) => {
  const timeline = []
  const packetsInFile = random(500, 5000)
  const packetsReplayed = params.filter ? Math.floor(packetsInFile * random(30, 80) / 100) : packetsInFile
  const loops = params.loop || 1
  const totalPackets = packetsReplayed * loops
  const speed = params.speed || 1.0
  const bandwidth = (totalPackets * random(500, 1500)) / 1024 / 1024

  timeline.push({ time: 0, message: 'Initializing PCAP replay...', type: 'info' })
  timeline.push({ time: 500, message: `PCAP file: ${params.file}`, type: 'info' })
  timeline.push({ time: 700, message: `Interface: ${params.interface}`, type: 'info' })
  timeline.push({ time: 900, message: `Speed multiplier: ${speed}x`, type: 'info' })

  if (params.filter) {
    timeline.push({ time: 1200, message: `Applying filter: ${params.filter}`, type: 'progress' })
  }

  timeline.push({ time: 1500, message: 'Loading PCAP file...', type: 'progress' })
  timeline.push({ time: 2000, message: `Loaded ${packetsInFile} packets from file`, type: 'info' })

  if (params.filter) {
    timeline.push({ time: 2300, message: `${packetsReplayed} packets match filter`, type: 'info' })
  }

  timeline.push({ time: 2500, message: 'Starting replay...', type: 'progress' })

  for (let loop = 1; loop <= Math.min(loops, 3); loop++) {
    const time = 3000 + ((loop - 1) * 2000)
    timeline.push({ time, message: `Loop ${loop}/${loops}: Replaying ${packetsReplayed} packets...`, type: 'progress' })
    timeline.push({ time: time + 1500, message: `Loop ${loop}/${loops}: Complete`, type: 'success' })
  }

  timeline.push({ time: 8000, message: `Total packets replayed: ${totalPackets}`, type: 'success' })
  timeline.push({ time: 8500, message: `Bandwidth used: ${bandwidth.toFixed(2)} MB`, type: 'info' })

  if (params.stats) {
    timeline.push({ time: 9000, message: 'Generating statistics...', type: 'progress' })
    timeline.push({ time: 9500, message: `Statistics saved to: ${params.output || '/tmp/replay_stats.json'}`, type: 'success' })
  }

  return {
    success: true,
    timeline,
    metrics: {
      pcapFile: params.file,
      packetsInFile: packetsInFile,
      packetsReplayed: packetsReplayed,
      loops: loops,
      totalPackets: totalPackets,
      speed: `${speed}x`,
      bandwidth: `${bandwidth.toFixed(2)} MB`,
      duration: '9.5s'
    },
    explanation: {
      happening: `Network traffic from the PCAP file is being replayed onto the network at ${speed}x speed. ${params.filter ? `Packets are filtered by "${params.filter}" before replay.` : 'All packets are being replayed.'} ${loops > 1 ? `The replay is looped ${loops} times.` : ''}`,
      highlights: [
        `${totalPackets} packets replayed`,
        `${speed}x replay speed`,
        `${bandwidth.toFixed(2)} MB bandwidth consumed`
      ],
      interpretation: `Successfully replayed ${totalPackets} packets from ${params.file} onto interface ${params.interface}. ${params.filter ? `Filter "${params.filter}" matched ${packetsReplayed} of ${packetsInFile} packets.` : `All ${packetsInFile} packets were replayed.`} ${loops > 1 ? `The traffic was looped ${loops} times.` : ''} The replay consumed ${bandwidth.toFixed(2)} MB of bandwidth at ${speed}x speed.`
    }
  }
}

/**
 * Main simulation function
 * Routes to appropriate attack simulator based on attack ID and scenario
 */
export const simulateAttack = async (attackId, scenarioId, parameters) => {
  // Validate attack exists
  const attack = getAttackById(attackId)
  if (!attack) {
    return {
      success: false,
      error: `Attack type '${attackId}' not found`
    }
  }

  // Validate scenario exists
  const scenario = attack.scenarios.find(s => s.id === scenarioId)
  if (!scenario) {
    return {
      success: false,
      error: `Scenario '${scenarioId}' not found for attack '${attackId}'`
    }
  }

  // Add simulation delay for realism
  await new Promise(resolve => setTimeout(resolve, 500))

  // Route to appropriate simulator
  switch (attackId) {
    case 'arp-spoofing':
      return simulateArpSpoofing(scenarioId, parameters)
    case 'syn-flood':
      return simulateSynFlood(scenarioId, parameters)
    case 'dns-amplification':
      return simulateDnsAmplification(scenarioId, parameters)
    case 'ping-of-death':
      return simulatePingOfDeath(scenarioId, parameters)
    case 'http-dos':
      return simulateHttpDos(scenarioId, parameters)
    case 'slowloris':
      return simulateSlowloris(scenarioId, parameters)
    case 'ssh-brute-force':
      return simulateSshBruteForce(scenarioId, parameters)
    case 'sql-injection':
      return simulateSqlInjection(scenarioId, parameters)
    case 'credential-harvester':
      return simulateCredentialHarvester(scenarioId, parameters)
    case 'pcap-replay':
      return simulatePcapReplay(scenarioId, parameters)
    case 'udp-flood':
      return simulateUdpFlood(scenarioId, parameters)
    case 'icmp-flood':
      return simulateIcmpFlood(scenarioId, parameters)
    case 'mitm':
      return simulateMitm(scenarioId, parameters)
    case 'dhcp-starvation':
      return simulateDhcpStarvation(scenarioId, parameters)
    case 'mac-flooding':
      return simulateMacFlooding(scenarioId, parameters)
    case 'vlan-hopping':
      return simulateVlanHopping(scenarioId, parameters)
    case 'http-flood':
      return simulateHttpFlood(scenarioId, parameters)
    case 'xss':
      return simulateXss(scenarioId, parameters)
    case 'directory-traversal':
      return simulateDirectoryTraversal(scenarioId, parameters)
    case 'xxe':
      return simulateXxe(scenarioId, parameters)
    case 'ssl-strip':
      return simulateSslStrip(scenarioId, parameters)
    case 'bgp-hijacking':
      return simulateBgpHijacking(scenarioId, parameters)
    case 'smurf-attack':
      return simulateSmurfAttack(scenarioId, parameters)
    case 'ntp-amplification':
      return simulateNtpAmplification(scenarioId, parameters)
    case 'ftp-brute-force':
      return simulateFtpBruteForce(scenarioId, parameters)
    case 'rdp-brute-force':
      return simulateRdpBruteForce(scenarioId, parameters)
    default:
      return {
        success: false,
        error: `No simulator implemented for attack '${attackId}'`
      }
  }
}

/**
 * Validate parameters before simulation
 */
export const validateParameters = (attackId, scenarioId, parameters) => {
  const attack = getAttackById(attackId)
  if (!attack) return { valid: false, errors: ['Invalid attack type'] }

  const scenario = attack.scenarios.find(s => s.id === scenarioId)
  if (!scenario) return { valid: false, errors: ['Invalid scenario'] }

  const errors = []

  // Check required parameters
  scenario.parameters.forEach(param => {
    if (param.required && !parameters[param.name]) {
      errors.push(`${param.label} is required`)
    }
  })

  return {
    valid: errors.length === 0,
    errors
  }
}


// UDP Flood simulation
const simulateUdpFlood = (scenarioId, params) => {
  const timeline = []
  const packets = params.count || 1000
  const rate = params.rate || 100
  const duration = (packets / rate).toFixed(1)

  timeline.push({ time: 0, message: 'Initializing UDP flood attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}:${params.port || 'random'}`, type: 'info' })
  timeline.push({ time: 700, message: `Packet rate: ${rate} packets/sec`, type: 'info' })
  timeline.push({ time: 1000, message: 'Generating UDP packets...', type: 'progress' })
  timeline.push({ time: 2000, message: `Sent ${Math.floor(packets * 0.5)} packets...`, type: 'info' })
  timeline.push({ time: 3000, message: `Sent ${packets} packets`, type: 'success' })
  timeline.push({ time: 3500, message: `Target bandwidth saturated`, type: 'warning' })

  return {
    success: true,
    timeline,
    metrics: {
      packetsSent: packets,
      bandwidth: `${(packets * 512 / 1024).toFixed(2)} KB`,
      duration: `${duration}s`,
      packetsPerSecond: rate
    },
    explanation: {
      happening: 'UDP flood is overwhelming the target with high-volume UDP packets.',
      highlights: [`${packets} packets sent`, `${rate} packets/sec`, 'Target saturated'],
      interpretation: `Successfully flooded ${params.target} with ${packets} UDP packets, consuming bandwidth and processing resources.`
    }
  }
}

// ICMP Flood simulation
const simulateIcmpFlood = (scenarioId, params) => {
  const timeline = []
  const packets = params.count || 1000
  
  timeline.push({ time: 0, message: 'Initializing ICMP flood...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Sending ICMP echo requests...', type: 'progress' })
  timeline.push({ time: 2000, message: `Sent ${packets} ICMP packets`, type: 'success' })
  timeline.push({ time: 2500, message: 'Target processing overhead increased', type: 'warning' })

  return {
    success: true,
    timeline,
    metrics: {
      packetsSent: packets,
      icmpReplies: Math.floor(packets * 0.9),
      bandwidth: `${(packets * 64 / 1024).toFixed(2)} KB`
    },
    explanation: {
      happening: 'ICMP flood is overwhelming target with ping requests.',
      highlights: [`${packets} ICMP packets`, 'Target responding', 'Resources consumed'],
      interpretation: `ICMP flood attack sent ${packets} ping packets to ${params.target}, forcing the target to process and respond to each one.`
    }
  }
}

// MITM simulation  
const simulateMitm = (scenarioId, params) => {
  const timeline = []
  
  timeline.push({ time: 0, message: 'Initializing MITM attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.target}`, type: 'info' })
  timeline.push({ time: 700, message: `Gateway: ${params.gateway}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Resolving MAC addresses...', type: 'progress' })
  timeline.push({ time: 1500, message: 'Sending ARP poison packets...', type: 'progress' })
  timeline.push({ time: 2000, message: 'ARP caches poisoned', type: 'success' })
  timeline.push({ time: 2500, message: 'Traffic interception active', type: 'success' })
  timeline.push({ time: 3000, message: 'Intercepting packets...', type: 'info' })

  return {
    success: true,
    timeline,
    metrics: {
      poisonPackets: 20,
      interceptedPackets: random(50, 200),
      duration: '3.0s'
    },
    explanation: {
      happening: 'Traffic between victim and gateway is being intercepted.',
      highlights: ['ARP poisoning active', 'Packets intercepted', 'IP forwarding enabled'],
      interpretation: `Successfully positioned between ${params.target} and ${params.gateway}. All traffic is flowing through attacker's machine.`
    }
  }
}

/**
 * Simulate DHCP Starvation attack
 */
const simulateDhcpStarvation = (scenarioId, params) => {
  const timeline = []
  const count = params.count || 200
  const rate = params.rate || 10

  timeline.push({ time: 0, message: 'Initializing DHCP starvation attack...', type: 'info' })
  timeline.push({ time: 500, message: `Interface: ${params.interface}`, type: 'info' })
  timeline.push({ time: 700, message: `Generating ${count} DHCP requests...`, type: 'progress' })
  timeline.push({ time: 1500, message: 'Sending DHCP DISCOVER packets...', type: 'progress' })
  timeline.push({ time: 2500, message: `Sent ${Math.floor(count * 0.5)} requests...`, type: 'info' })
  timeline.push({ time: 3500, message: `Sent ${count} requests`, type: 'success' })
  timeline.push({ time: 4000, message: 'DHCP pool exhaustion in progress', type: 'warning' })

  return {
    success: true,
    timeline,
    metrics: {
      requestsSent: count,
      rate: `${rate}/sec`,
      poolStatus: 'Depleted',
      duration: '4.0s'
    },
    explanation: {
      happening: 'DHCP server IP pool is being exhausted with spoofed MAC addresses.',
      highlights: [`${count} requests sent`, 'Random MAC addresses', 'Pool depletion'],
      interpretation: `The attack generated ${count} DHCP DISCOVER requests with random MAC addresses, exhausting the server's available IP pool.`
    }
  }
}

/**
 * Simulate MAC Flooding attack
 */
const simulateMacFlooding = (scenarioId, params) => {
  const timeline = []
  const count = params.count || 10000
  const rate = params.rate || 500

  timeline.push({ time: 0, message: 'Initializing MAC flooding attack...', type: 'info' })
  timeline.push({ time: 500, message: `Interface: ${params.interface}`, type: 'info' })
  timeline.push({ time: 700, message: 'Generating random MAC addresses...', type: 'progress' })
  timeline.push({ time: 1500, message: 'Flooding switch with frames...', type: 'progress' })
  timeline.push({ time: 2500, message: `Sent ${Math.floor(count * 0.3)} frames...`, type: 'info' })
  timeline.push({ time: 3500, message: `Sent ${Math.floor(count * 0.7)} frames...`, type: 'info' })
  timeline.push({ time: 4500, message: `Sent ${count} frames`, type: 'success' })
  timeline.push({ time: 5000, message: 'Switch MAC table overflowed - entering fail-open mode', type: 'warning' })

  return {
    success: true,
    timeline,
    metrics: {
      framesSent: count,
      rate: `${rate}/sec`,
      switchStatus: 'Fail-open',
      duration: '5.0s'
    },
    explanation: {
      happening: 'Switch MAC address table is overflowed, causing it to broadcast all traffic.',
      highlights: [`${count} frames sent`, 'Random MACs', 'Fail-open mode'],
      interpretation: `The switch's MAC table was overwhelmed with ${count} random MAC addresses, forcing it into fail-open mode where it broadcasts all traffic.`
    }
  }
}

/**
 * Simulate VLAN Hopping attack
 */
const simulateVlanHopping = (scenarioId, params) => {
  const timeline = []
  const count = params.count || 100

  timeline.push({ time: 0, message: 'Initializing VLAN hopping attack...', type: 'info' })
  timeline.push({ time: 500, message: `Interface: ${params.interface}`, type: 'info' })
  timeline.push({ time: 700, message: `Outer VLAN: ${params.outerVlan}`, type: 'info' })
  timeline.push({ time: 900, message: `Inner VLAN: ${params.innerVlan}`, type: 'info' })
  timeline.push({ time: 1200, message: 'Crafting double-tagged packets...', type: 'progress' })
  timeline.push({ time: 2000, message: 'Sending packets to target...', type: 'progress' })
  timeline.push({ time: 3000, message: `${count} packets sent successfully`, type: 'success' })
  timeline.push({ time: 3500, message: 'VLAN isolation bypassed', type: 'warning' })

  return {
    success: true,
    timeline,
    metrics: {
      packetsSent: count,
      outerVlan: params.outerVlan,
      innerVlan: params.innerVlan,
      target: params.target,
      duration: '3.5s'
    },
    explanation: {
      happening: 'Double-tagged packets are bypassing VLAN isolation.',
      highlights: ['VLAN hopping successful', 'Double tagging', 'Isolation bypassed'],
      interpretation: `Successfully hopped from VLAN ${params.outerVlan} to VLAN ${params.innerVlan} using double VLAN tagging, reaching ${params.target}.`
    }
  }
}

/**
 * Simulate HTTP Flood attack
 */
const simulateHttpFlood = (scenarioId, params) => {
  const timeline = []
  const count = params.count || 1000
  const threads = params.threads || 10

  timeline.push({ time: 0, message: 'Initializing HTTP flood attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target URL: ${params.url}`, type: 'info' })
  timeline.push({ time: 700, message: `Threads: ${threads}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Starting multi-threaded flood...', type: 'progress' })
  timeline.push({ time: 2000, message: `Sent ${Math.floor(count * 0.3)} requests...`, type: 'info' })
  timeline.push({ time: 3000, message: `Sent ${Math.floor(count * 0.6)} requests...`, type: 'info' })
  timeline.push({ time: 4000, message: `Sent ${count} requests`, type: 'success' })
  timeline.push({ time: 4500, message: 'Server response time degraded', type: 'warning' })

  return {
    success: true,
    timeline,
    metrics: {
      requestsSent: count,
      threads: threads,
      avgResponseTime: `${random(500, 3000)}ms`,
      errors: random(10, 50),
      duration: '4.5s'
    },
    explanation: {
      happening: 'Web server is being overwhelmed with HTTP requests.',
      highlights: [`${count} requests sent`, `${threads} threads`, 'Server degraded'],
      interpretation: `Flooded ${params.url} with ${count} HTTP requests using ${threads} parallel threads. Server response time has increased significantly.`
    }
  }
}

/**
 * Simulate XSS attack
 */
const simulateXss = (scenarioId, params) => {
  const timeline = []
  const payloads = random(5, 15)
  const vulnerable = random(1, 3)

  timeline.push({ time: 0, message: 'Initializing XSS vulnerability scan...', type: 'info' })
  timeline.push({ time: 500, message: `Target URL: ${params.url}`, type: 'info' })
  timeline.push({ time: 700, message: `Testing parameter: ${params.param}`, type: 'info' })
  timeline.push({ time: 1000, message: `Testing ${payloads} XSS payloads...`, type: 'progress' })
  timeline.push({ time: 2000, message: 'Analyzing responses...', type: 'progress' })
  timeline.push({ time: 3000, message: `Found ${vulnerable} potential vulnerabilities`, type: vulnerable > 0 ? 'warning' : 'success' })
  timeline.push({ time: 3500, message: 'Scan complete', type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      payloadsTested: payloads,
      vulnerabilitiesFound: vulnerable,
      parameter: params.param,
      duration: '3.5s'
    },
    explanation: {
      happening: 'XSS payloads are being tested against the target application.',
      highlights: [`${payloads} payloads tested`, `${vulnerable} vulnerabilities`, 'Response analysis'],
      interpretation: `Tested ${payloads} XSS payloads against parameter '${params.param}' at ${params.url}. ${vulnerable > 0 ? `Found ${vulnerable} potential XSS vulnerabilities.` : 'No vulnerabilities found.'}`
    }
  }
}

/**
 * Simulate Directory Traversal attack
 */
const simulateDirectoryTraversal = (scenarioId, params) => {
  const timeline = []
  const payloads = random(8, 20)
  const vulnerable = random(0, 2)

  timeline.push({ time: 0, message: 'Initializing directory traversal scan...', type: 'info' })
  timeline.push({ time: 500, message: `Target URL: ${params.url}`, type: 'info' })
  timeline.push({ time: 700, message: `Testing parameter: ${params.param}`, type: 'info' })
  timeline.push({ time: 1000, message: `Testing ${payloads} traversal payloads...`, type: 'progress' })
  timeline.push({ time: 2500, message: 'Analyzing file access patterns...', type: 'progress' })
  timeline.push({ time: 3500, message: `${vulnerable > 0 ? 'Vulnerability detected!' : 'No vulnerabilities found'}`, type: vulnerable > 0 ? 'warning' : 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      payloadsTested: payloads,
      vulnerabilitiesFound: vulnerable,
      parameter: params.param,
      duration: '3.5s'
    },
    explanation: {
      happening: 'Testing for directory traversal vulnerabilities using various path manipulation techniques.',
      highlights: [`${payloads} payloads`, `${vulnerable} vulnerabilities`, 'Path analysis'],
      interpretation: `Tested ${payloads} directory traversal payloads against '${params.param}'. ${vulnerable > 0 ? `Found ${vulnerable} potential vulnerabilities allowing file access outside web root.` : 'Application appears secure.'}`
    }
  }
}

/**
 * Simulate XXE attack
 */
const simulateXxe = (scenarioId, params) => {
  const timeline = []
  const payloads = random(5, 10)
  const vulnerable = random(0, 1)

  timeline.push({ time: 0, message: 'Initializing XXE vulnerability scan...', type: 'info' })
  timeline.push({ time: 500, message: `Target URL: ${params.url}`, type: 'info' })
  timeline.push({ time: 1000, message: `Testing ${payloads} XXE payloads...`, type: 'progress' })
  timeline.push({ time: 2000, message: 'Analyzing XML parser behavior...', type: 'progress' })
  timeline.push({ time: 3000, message: `${vulnerable > 0 ? 'XXE vulnerability detected!' : 'No vulnerabilities found'}`, type: vulnerable > 0 ? 'warning' : 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      payloadsTested: payloads,
      vulnerabilitiesFound: vulnerable,
      xxeType: vulnerable > 0 ? 'File read' : 'None',
      duration: '3.0s'
    },
    explanation: {
      happening: 'Testing XML parser for external entity injection vulnerabilities.',
      highlights: [`${payloads} payloads`, `${vulnerable} vulnerabilities`, 'Parser analysis'],
      interpretation: `Tested ${payloads} XXE payloads against ${params.url}. ${vulnerable > 0 ? 'XML parser is vulnerable to external entity injection, allowing file reads.' : 'XML parser properly validates external entities.'}`
    }
  }
}

/**
 * Simulate SSL Strip attack
 */
const simulateSslStrip = (scenarioId, params) => {
  const timeline = []
  const connections = random(5, 20)

  timeline.push({ time: 0, message: 'Initializing SSL strip attack (simulation)...', type: 'info' })
  timeline.push({ time: 500, message: `Interface: ${params.interface}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Setting up transparent proxy...', type: 'progress' })
  timeline.push({ time: 2000, message: 'Intercepting HTTPS traffic...', type: 'progress' })
  timeline.push({ time: 3000, message: `Downgraded ${connections} connections to HTTP`, type: 'warning' })
  timeline.push({ time: 3500, message: 'SSL stripping active (simulation)', type: 'info' })

  return {
    success: true,
    timeline,
    metrics: {
      connectionsDowngraded: connections,
      interface: params.interface,
      mode: 'Simulation',
      duration: '3.5s'
    },
    explanation: {
      happening: 'HTTPS connections are being downgraded to HTTP (educational simulation).',
      highlights: [`${connections} connections`, 'HTTPS downgrade', 'Simulation mode'],
      interpretation: `Simulated SSL stripping attack downgrading ${connections} HTTPS connections to HTTP. In reality, this requires MITM position and is detectable by HSTS.`
    }
  }
}

/**
 * Simulate BGP Hijacking attack
 */
const simulateBgpHijacking = (scenarioId, params) => {
  const timeline = []

  timeline.push({ time: 0, message: 'Initializing BGP hijacking simulation...', type: 'info' })
  timeline.push({ time: 500, message: `Target prefix: ${params.prefix}`, type: 'info' })
  timeline.push({ time: 700, message: `AS Number: ${params.asNumber}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Simulating route announcement...', type: 'progress' })
  timeline.push({ time: 2000, message: 'Route propagation simulated', type: 'info' })
  timeline.push({ time: 2500, message: 'BGP hijacking simulation complete', type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      prefix: params.prefix,
      asNumber: params.asNumber,
      mode: 'Educational simulation',
      duration: '2.5s'
    },
    explanation: {
      happening: 'Simulating BGP route hijacking for educational purposes.',
      highlights: ['Route announcement', 'AS path manipulation', 'Simulation only'],
      interpretation: `Educational simulation of BGP hijacking for prefix ${params.prefix} using AS ${params.asNumber}. Real BGP hijacking requires router access and is highly regulated.`
    }
  }
}

/**
 * Simulate Smurf Attack
 */
const simulateSmurfAttack = (scenarioId, params) => {
  const timeline = []
  const count = params.count || 100
  const amplification = random(10, 50)

  timeline.push({ time: 0, message: 'Initializing Smurf attack...', type: 'info' })
  timeline.push({ time: 500, message: `Victim: ${params.victim}`, type: 'info' })
  timeline.push({ time: 700, message: `Broadcast: ${params.broadcast}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Sending ICMP to broadcast address...', type: 'progress' })
  timeline.push({ time: 2000, message: `Sent ${count} packets`, type: 'info' })
  timeline.push({ time: 3000, message: `Amplification factor: ${amplification}x`, type: 'warning' })
  timeline.push({ time: 3500, message: 'Traffic amplification complete', type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      packetsSent: count,
      amplificationFactor: `${amplification}x`,
      victim: params.victim,
      broadcast: params.broadcast,
      duration: '3.5s'
    },
    explanation: {
      happening: 'ICMP broadcast is amplifying attack traffic toward victim.',
      highlights: [`${count} packets`, `${amplification}x amplification`, 'Broadcast exploitation'],
      interpretation: `Sent ${count} spoofed ICMP packets to ${params.broadcast}, resulting in ${amplification}x amplification toward victim ${params.victim}.`
    }
  }
}

/**
 * Simulate NTP Amplification attack
 */
const simulateNtpAmplification = (scenarioId, params) => {
  const timeline = []
  const count = params.count || 100
  const amplification = random(200, 500)

  timeline.push({ time: 0, message: 'Initializing NTP amplification attack...', type: 'info' })
  timeline.push({ time: 500, message: `Victim: ${params.victim}`, type: 'info' })
  timeline.push({ time: 700, message: `NTP Servers: ${params.ntpServers}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Sending NTP queries with spoofed source...', type: 'progress' })
  timeline.push({ time: 2500, message: `Sent ${count} queries`, type: 'info' })
  timeline.push({ time: 3500, message: `Amplification factor: ${amplification}x`, type: 'warning' })
  timeline.push({ time: 4000, message: 'NTP amplification attack complete', type: 'success' })

  return {
    success: true,
    timeline,
    metrics: {
      queriesSent: count,
      amplificationFactor: `${amplification}x`,
      victim: params.victim,
      ntpServers: params.ntpServers.split(',').length,
      duration: '4.0s'
    },
    explanation: {
      happening: 'NTP servers are amplifying traffic toward victim using monlist queries.',
      highlights: [`${count} queries`, `${amplification}x amplification`, 'Multiple NTP servers'],
      interpretation: `Sent ${count} spoofed NTP queries, achieving ${amplification}x amplification factor toward victim ${params.victim}. Modern NTP servers are typically patched against this.`
    }
  }
}

/**
 * Simulate FTP Brute Force attack
 */
const simulateFtpBruteForce = (scenarioId, params) => {
  const timeline = []
  const passwords = params.passwords.split('\n').filter(p => p.trim())
  const success = random(0, 1) === 1
  const attempts = success ? random(5, passwords.length) : passwords.length

  timeline.push({ time: 0, message: 'Initializing FTP brute force attack...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.host}:${params.port || 21}`, type: 'info' })
  timeline.push({ time: 700, message: `Username: ${params.username}`, type: 'info' })
  timeline.push({ time: 1000, message: `Testing ${passwords.length} passwords...`, type: 'progress' })
  timeline.push({ time: 2000, message: `Attempted ${Math.floor(attempts * 0.5)} passwords...`, type: 'info' })
  timeline.push({ time: 3000, message: `Attempted ${attempts} passwords`, type: 'info' })
  timeline.push({ time: 3500, message: success ? 'Valid credentials found!' : 'No valid credentials found', type: success ? 'warning' : 'info' })

  return {
    success: true,
    timeline,
    metrics: {
      attempts: attempts,
      totalPasswords: passwords.length,
      credentialsFound: success,
      duration: '3.5s'
    },
    explanation: {
      happening: 'Testing password combinations against FTP server.',
      highlights: [`${attempts} attempts`, success ? 'Credentials found' : 'No success', `User: ${params.username}`],
      interpretation: `Attempted ${attempts} passwords for user '${params.username}' on ${params.host}. ${success ? 'Found valid credentials!' : 'No valid credentials discovered.'}`
    }
  }
}

/**
 * Simulate RDP Brute Force attack
 */
const simulateRdpBruteForce = (scenarioId, params) => {
  const timeline = []
  const passwords = params.passwords.split('\n').filter(p => p.trim())
  const success = random(0, 1) === 1
  const attempts = success ? random(3, Math.min(10, passwords.length)) : Math.min(10, passwords.length)

  timeline.push({ time: 0, message: 'Initializing RDP brute force simulation...', type: 'info' })
  timeline.push({ time: 500, message: `Target: ${params.host}:${params.port || 3389}`, type: 'info' })
  timeline.push({ time: 700, message: `Username: ${params.username}`, type: 'info' })
  timeline.push({ time: 1000, message: 'Simulating connection attempts...', type: 'progress' })
  timeline.push({ time: 2500, message: `Attempted ${attempts} passwords`, type: 'info' })
  timeline.push({ time: 3000, message: success ? 'Simulation complete - credentials found' : 'Simulation complete - no success', type: 'info' })

  return {
    success: true,
    timeline,
    metrics: {
      attempts: attempts,
      credentialsFound: success,
      mode: 'Educational simulation',
      duration: '3.0s'
    },
    explanation: {
      happening: 'Simulating RDP brute force attack (educational).',
      highlights: [`${attempts} attempts`, 'Simulation mode', success ? 'Success simulated' : 'No success'],
      interpretation: `Educational simulation of RDP brute force against ${params.host} for user '${params.username}'. Real RDP brute force requires specialized libraries and has high detection rates.`
    }
  }
}

