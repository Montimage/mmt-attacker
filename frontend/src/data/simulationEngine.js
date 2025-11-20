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
