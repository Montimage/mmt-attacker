/**
 * MMT-Attacker Simulation Engine
 * Log messages and metrics match the real mag CLI output format.
 */

import { getAttackById } from './attacksData'

const random = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min

const ts = () => {
  const now = new Date()
  return now.toISOString().replace('T', ' ').substring(0, 23)
}

const logInfo  = (msg) => ({ level: 'INFO',    message: msg })
const logWarn  = (msg) => ({ level: 'WARNING', message: msg })
const logError = (msg) => ({ level: 'ERROR',   message: msg })

// Convert a log entry to a timeline event compatible with the existing UI
const toEvent = (t, entry, type = null) => ({
  time: t,
  message: `${ts()} - ${entry.level} - ${entry.message}`,
  type: type || (entry.level === 'ERROR' ? 'error' : entry.level === 'WARNING' ? 'warning' : 'info')
})

// ─── Packet-flood helpers ────────────────────────────────────────────────────

const floodTimeline = ({ initMsg, summaryLines, packetCount, rate = 100, extraInit = [] }) => {
  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(initMsg)))
  t += 50
  for (const line of extraInit) {
    events.push(toEvent(t, logInfo(line)))
    t += 30
  }
  events.push(toEvent(t, logInfo(`Sending ${packetCount} packets at ${rate} packets/second`)))
  t += 50

  // Progress milestones: 20%, 40%, 60%, 80%, 100%
  for (let pct of [0.2, 0.4, 0.6, 0.8, 1.0]) {
    const sent = Math.round(packetCount * pct)
    events.push(toEvent(t, logInfo(`Progress: ${(pct * 100).toFixed(1)}% (${sent}/${packetCount} packets)`)))
    t += 60
  }

  events.push(toEvent(t, logInfo('Attack completed successfully'), 'success'))
  t += 30
  for (const line of summaryLines) {
    events.push(toEvent(t, logInfo(line)))
    t += 30
  }
  return { events, durationMs: t }
}

// ─── ARP Spoof ───────────────────────────────────────────────────────────────

const simulateArpSpoofing = (scenarioId, params) => {
  const interval = params.interval || 1.0
  const packetsSent = random(20, 60)
  const durationSec = (packetsSent * interval).toFixed(2)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo('Initialized ARP spoofing attack simulation')))
  t += 50
  events.push(toEvent(t, logInfo(`Target: ${params.targetIp}, Gateway: ${params.gatewayIp}, Interface: ${params.interface}`)))
  t += 50
  events.push(toEvent(t, logInfo('Setting up ARP spoofing attack...')))
  t += 100
  events.push(toEvent(t, logInfo(`Resolving MAC address for target ${params.targetIp}...`)))
  t += 200
  events.push(toEvent(t, logInfo(`Resolving MAC address for gateway ${params.gatewayIp}...`)))
  t += 200
  events.push(toEvent(t, logInfo('MAC addresses resolved — starting ARP poisoning loop')))
  t += 100
  for (let i = 1; i <= Math.min(packetsSent, 5); i++) {
    events.push(toEvent(t, logInfo(`Sent ARP reply ${i}: ${params.targetIp} → attacker MAC`)))
    t += Math.round(interval * 80)
    events.push(toEvent(t, logInfo(`Sent ARP reply ${i}: ${params.gatewayIp} → attacker MAC`)))
    t += Math.round(interval * 80)
  }
  if (packetsSent > 5) {
    events.push(toEvent(t, logInfo(`... (${packetsSent - 5} more ARP pairs sent)`)))
    t += 100
  }
  events.push(toEvent(t, logInfo(`ARP-SPOOF complete — target=${params.targetIp}  packets=${packetsSent}  duration=${durationSec}s`), 'success'))

  return {
    success: true,
    timeline: events,
    metrics: {
      targetIp: params.targetIp,
      gatewayIp: params.gatewayIp,
      interface: params.interface,
      interval: `${interval}s`,
      arpPairsSent: packetsSent,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `ARP poisoning packets are being sent every ${interval}s to both the target and gateway, redirecting all traffic between them through the attacker's machine.`,
      highlights: [
        `${packetsSent} ARP pairs sent`,
        `Target ${params.targetIp} and gateway ${params.gatewayIp} poisoned`,
        `Interval: ${interval}s between spoofed packets`
      ],
      interpretation: `The attack associated the attacker's MAC address with both ${params.targetIp} and ${params.gatewayIp}. All traffic between them now flows through the attacker. Run with sudo on a real network to actually intercept traffic.`
    }
  }
}

// ─── SYN Flood ───────────────────────────────────────────────────────────────

const simulateSynFlood = (scenarioId, params) => {
  const count = params.count || 1000
  const rate = 100
  const durationSec = (count / rate).toFixed(4)
  const actualRate = (count / parseFloat(durationSec) * random(60, 90) / 100).toFixed(4)
  const trafficBytes = `${(count * 60 / 1024).toFixed(2)} KB`

  const { events } = floodTimeline({
    initMsg: 'Initialized SYN flood attack simulation',
    extraInit: [
      `Target: ${params.targetIp}, Ports: ${params.targetPort}`,
      `Starting SYN flood attack against ${params.targetIp}`,
    ],
    summaryLines: [
      `SYN Flood complete — target=${params.targetIp}  packets=${count}  duration=${durationSec}s`,
      `Target Ip: ${params.targetIp}`,
      `Ports: ${params.targetPort}`,
      `Packets Sent: ${count}`,
      `Duration Seconds: ${durationSec}`,
      `Configured Rate: ${rate}`,
      `Actual Rate: ${actualRate}`,
      `Estimated Traffic: ${trafficBytes}`
    ],
    packetCount: count,
    rate
  })

  return {
    success: true,
    timeline: events,
    metrics: {
      targetIp: params.targetIp,
      targetPort: params.targetPort,
      packetsSent: count,
      configuredRate: rate,
      actualRate: parseFloat(actualRate),
      estimatedTraffic: trafficBytes,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `${count} TCP SYN packets are sent to ${params.targetIp}:${params.targetPort} with spoofed source IPs. Each forces the target to allocate a half-open connection and wait for an ACK that never arrives, exhausting the connection table.`,
      highlights: [
        `${count} SYN packets sent`,
        `Port ${params.targetPort} targeted`,
        `${trafficBytes} estimated traffic`
      ],
      interpretation: `Sent ${count} SYN packets to ${params.targetIp}:${params.targetPort} at ~${actualRate} pkt/s. In a real attack this fills the server's connection table, preventing legitimate TCP connections. Requires root/sudo to send raw packets.`
    }
  }
}

// ─── DNS Amplification ───────────────────────────────────────────────────────

const simulateDnsAmplification = (scenarioId, params) => {
  const queryCount = params.queryCount || 1000
  const amplificationFactor = 50
  const querySize = 60
  const responseSize = querySize * amplificationFactor
  const queryTrafficKb = ((queryCount * querySize) / 1024).toFixed(2)
  const responseTrafficKb = ((queryCount * responseSize) / 1024).toFixed(2)
  const durationSec = (queryCount * 0.002).toFixed(3)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo('Initialized DNS amplification attack simulation')))
  t += 50
  events.push(toEvent(t, logInfo(`Target: ${params.targetIp}, Domain: ${params.domain || 'example.com'}, Query type: ANY`)))
  t += 50
  events.push(toEvent(t, logInfo('Using 1 DNS servers')))
  t += 50
  events.push(toEvent(t, logInfo(`Starting DNS amplification attack against ${params.targetIp}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Sending ${queryCount} queries of type ANY for domain ${params.domain || 'example.com'}`)))
  t += 50

  for (let i = 1; i <= Math.min(queryCount, 5); i++) {
    events.push(toEvent(t, logInfo(`Sending query ${i}/${queryCount}`)))
    t += 50
  }
  if (queryCount > 5) {
    events.push(toEvent(t, logInfo(`... (${queryCount - 5} more queries sent)`)))
    t += 80
  }

  events.push(toEvent(t, logInfo('DNS amplification attack completed successfully'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Target: ${params.targetIp}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Domain queried: ${params.domain || 'example.com'}`)))
  t += 20
  events.push(toEvent(t, logInfo(`DNS servers used: 1`)))
  t += 20
  events.push(toEvent(t, logInfo(`Packets sent: ${queryCount}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Duration: ${durationSec} seconds`)))
  t += 20
  events.push(toEvent(t, logInfo(`Amplification factor: ${amplificationFactor}x`)))
  t += 20
  events.push(toEvent(t, logInfo(`Query traffic: ${queryTrafficKb} KB`)))
  t += 20
  events.push(toEvent(t, logInfo(`Estimated response traffic: ${responseTrafficKb} KB`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      targetIp: params.targetIp,
      domain: params.domain || 'example.com',
      queryType: 'ANY',
      dnsServersUsed: 1,
      packetsSent: queryCount,
      durationSeconds: durationSec,
      amplificationFactor: `${amplificationFactor}x`,
      queryTraffic: `${queryTrafficKb} KB`,
      estimatedResponseTraffic: `${responseTrafficKb} KB`
    },
    explanation: {
      happening: `${queryCount} small DNS queries (${querySize} bytes each) with spoofed source IP (${params.targetIp}) are sent to ${params.dnsServers}. The resolver returns large ANY responses (~${responseSize} bytes) directed at the victim, achieving ${amplificationFactor}x amplification.`,
      highlights: [
        `${amplificationFactor}x amplification factor`,
        `${queryCount} queries → ${responseTrafficKb} KB response traffic`,
        `Domain: ${params.domain || 'example.com'}`
      ],
      interpretation: `DNS amplification sent ${queryCount} spoofed queries generating ${responseTrafficKb} KB of traffic toward ${params.targetIp}. Requires raw socket access (root/sudo) and a network path that allows UDP spoofing.`
    }
  }
}

// ─── Ping of Death ───────────────────────────────────────────────────────────

const simulatePingOfDeath = (scenarioId, params) => {
  const packetCount = params.packetCount || 100
  const payloadSize = 65500
  const fragmentSize = 1400
  const fragmentsPerPacket = Math.ceil(payloadSize / fragmentSize)
  const totalFragments = packetCount * fragmentsPerPacket
  const durationSec = (packetCount * 0.12).toFixed(2)
  const fragmentsPerSec = (totalFragments / parseFloat(durationSec)).toFixed(4)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized Ping of Death attack against ${params.targetIp}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting Ping of Death attack against ${params.targetIp}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Parameters: ${packetCount} packets, ${payloadSize} bytes payload, ${fragmentSize} bytes fragment size, 0.1 seconds interval`)))
  t += 50

  for (let i = 1; i <= Math.min(packetCount, 5); i++) {
    events.push(toEvent(t, logInfo(`Sending packet ${i}/${packetCount}`)))
    t += 60
    events.push(toEvent(t, logInfo(`Sending ${fragmentsPerPacket} fragments`)))
    t += 60
  }
  if (packetCount > 5) {
    events.push(toEvent(t, logInfo(`... (${packetCount - 5} more packets sent)`)))
    t += 80
  }

  events.push(toEvent(t, logInfo('Ping of Death attack completed successfully'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Target: ${params.targetIp}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Packets sent: ${packetCount}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Fragments sent: ${totalFragments}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Payload size: ${payloadSize} bytes`)))
  t += 20
  events.push(toEvent(t, logInfo(`Fragment size: ${fragmentSize} bytes`)))
  t += 20
  events.push(toEvent(t, logInfo(`Duration: ${durationSec} seconds`)))
  t += 20
  events.push(toEvent(t, logInfo(`Rate: ${fragmentsPerSec} fragments/second`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      target: params.targetIp,
      packetsSent: packetCount,
      fragmentsSent: totalFragments,
      payloadSize: `${payloadSize} bytes`,
      fragmentSize: `${fragmentSize} bytes`,
      durationSeconds: durationSec,
      fragmentsPerSecond: fragmentsPerSec
    },
    explanation: {
      happening: `Each oversized ICMP packet (${payloadSize} bytes) is split into ${fragmentsPerPacket} fragments. When the target reassembles them, the resulting packet exceeds the 65,535-byte IP maximum, potentially causing buffer overflows on unpatched systems.`,
      highlights: [
        `${packetCount} oversized packets (${payloadSize} bytes each)`,
        `${fragmentsPerPacket} fragments per packet`,
        `${totalFragments} total fragments sent`
      ],
      interpretation: `Sent ${packetCount} Ping of Death packets to ${params.targetIp} generating ${totalFragments} fragments. Modern systems are patched, but legacy embedded devices may still be vulnerable. Requires raw socket access.`
    }
  }
}

// ─── HTTP DoS ────────────────────────────────────────────────────────────────

const simulateHttpDos = (scenarioId, params) => {
  const connections = params.numConnections || 10
  const durationSec = 60
  const requestsSent = random(connections * 5, connections * 20)
  const method = 'get'

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo('Initialized HTTP DoS attack simulation')))
  t += 50
  events.push(toEvent(t, logInfo(`Target: ${params.targetUrl}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Attack method: ${method}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Starting HTTP DoS attack against ${params.targetUrl}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Attack method: ${method}, Connections: ${connections}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Duration: ${durationSec} seconds`)))
  t += 30
  events.push(toEvent(t, logInfo(`Using HTTP GET flood attack method`)))
  t += 80
  events.push(toEvent(t, logInfo(`Started ${connections} attack threads`)))
  t += 100

  const progressSteps = [0, 10, 25, 50, 75, 90]
  for (const pct of progressSteps) {
    const reqs = Math.round(requestsSent * pct / 100)
    events.push(toEvent(t, logInfo(`Progress: ${pct}.0%, Active connections: ${connections}, Requests: ${reqs}`)))
    t += 120
  }
  events.push(toEvent(t, logInfo(`HTTP DoS attack completed`), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Total requests sent: ${requestsSent}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      targetUrl: params.targetUrl,
      method,
      connections,
      requestsSent,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `${connections} concurrent threads continuously send HTTP GET requests to ${params.targetUrl}. Malformed or resource-intensive requests exhaust server worker pools and memory, degrading or denying service to legitimate users.`,
      highlights: [
        `${connections} concurrent connections`,
        `${requestsSent} requests sent`,
        `HTTP GET flood method`
      ],
      interpretation: `The DoS attack opened ${connections} concurrent connections to ${params.targetUrl} sending ${requestsSent} requests total. Server-side resource exhaustion (CPU / connection pool) is the primary impact. Effectiveness depends on server capacity.`
    }
  }
}

// ─── Slowloris ───────────────────────────────────────────────────────────────

const simulateSlowloris = (scenarioId, params) => {
  const sockets = params.sockets || 150
  const openedSockets = random(Math.floor(sockets * 0.85), sockets)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo('Initialized Slowloris attack simulation')))
  t += 50
  events.push(toEvent(t, logInfo(`Target: ${params.targetUrl}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Opening ${sockets} sockets...`)))
  t += 80

  for (let i = 1; i <= Math.min(openedSockets, 5); i++) {
    events.push(toEvent(t, logInfo(`Socket ${i}: partial HTTP request sent, connection held open`)))
    t += 40
  }
  if (openedSockets > 5) {
    events.push(toEvent(t, logInfo(`... (${openedSockets - 5} more sockets opened)`)))
    t += 60
  }

  events.push(toEvent(t, logInfo(`${openedSockets}/${sockets} sockets established`), 'success'))
  t += 60
  events.push(toEvent(t, logInfo('Sending keep-alive headers to maintain connections...')))
  t += 100
  events.push(toEvent(t, logInfo(`Connection pool usage: ${Math.floor((openedSockets / sockets) * 100)}%`), 'warning'))
  t += 60
  events.push(toEvent(t, logInfo('Server connection limit approaching — legitimate requests being rejected')))

  return {
    success: true,
    timeline: events,
    metrics: {
      targetUrl: params.targetUrl,
      socketsRequested: sockets,
      socketsOpened: openedSockets,
      connectionPoolUsage: `${Math.floor((openedSockets / sockets) * 100)}%`
    },
    explanation: {
      happening: `${openedSockets} partial HTTP connections are held open by sending only the beginning of an HTTP request and then dribbling keep-alive headers. The server waits for each request to complete, exhausting its connection pool with minimal bandwidth.`,
      highlights: [
        `${openedSockets} sockets held open`,
        `${Math.floor((openedSockets / sockets) * 100)}% server connection pool consumed`,
        'Low bandwidth — hard to detect by volume'
      ],
      interpretation: `Slowloris held ${openedSockets} connections open against ${params.targetUrl}. Apache and similar thread-per-connection servers are highly vulnerable; event-loop servers (nginx, Node.js) are generally resistant.`
    }
  }
}

// ─── SSH Brute Force ─────────────────────────────────────────────────────────

const simulateSshBruteForce = (scenarioId, params) => {
  const passwordCount = random(5, 20)
  const success = random(0, 100) > 85
  const crackedAt = success ? random(1, passwordCount) : null

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized SSH brute force attack simulation against ${params.targetIp}:${params.targetPort || 22}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting SSH brute force attack simulation against ${params.targetIp}:${params.targetPort || 22}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Using username: ${params.username}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Loaded ${passwordCount} passwords to try`)))
  t += 50

  for (let i = 1; i <= passwordCount; i++) {
    events.push(toEvent(t, logInfo(`Trying password ${i}/${passwordCount}`)))
    t += 80
    if (success && i === crackedAt) {
      events.push(toEvent(t, logInfo(`Authentication SUCCESS — ${params.username} on ${params.targetIp}`), 'success'))
      t += 30
      break
    } else {
      events.push(toEvent(t, logInfo(`Authentication failed for attempt ${i}`), 'warning'))
      t += 30
    }
  }

  if (!success) {
    events.push(toEvent(t, logInfo(`Brute force completed — no valid credentials found`)))
  }

  return {
    success: true,
    timeline: events,
    metrics: {
      targetIp: params.targetIp,
      targetPort: params.targetPort || 22,
      username: params.username,
      passwordsTried: success ? crackedAt : passwordCount,
      credentialsFound: success
    },
    explanation: {
      happening: `SSH login attempts are made with each password from the wordlist at ${params.passwords}. A successful attempt gives shell access to ${params.targetIp}.`,
      highlights: [
        success ? `Credentials found after ${crackedAt} attempts` : `${passwordCount} passwords tried — no match`,
        `Username: ${params.username}`,
        `Target: ${params.targetIp}:${params.targetPort || 22}`
      ],
      interpretation: success
        ? `Valid SSH credentials found for '${params.username}' on ${params.targetIp}. The account should be secured immediately with a stronger password or key-based auth.`
        : `No valid credentials found in the wordlist. Consider a larger wordlist or verify the target is reachable on port ${params.targetPort || 22}.`
    }
  }
}

// ─── SQL Injection ───────────────────────────────────────────────────────────

const simulateSqlInjection = (scenarioId, params) => {
  const payloadsTested = 5
  const vulnerabilitiesFound = random(0, 1) === 1 ? random(1, 2) : 0

  const payloads = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' UNION SELECT NULL--",
    "'; DROP TABLE users--",
    "1' AND SLEEP(2)--"
  ]

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Validating target URL: ${params.targetUrl}`)))
  t += 100
  if (vulnerabilitiesFound === 0) {
    events.push(toEvent(t, logWarn('Target validation failed (target may not have SQL endpoint) — running probes anyway')))
  }
  t += 50

  for (let i = 0; i < payloadsTested; i++) {
    events.push(toEvent(t, logInfo(`Executing attack with payload: ${payloads[i]}`)))
    t += 80
    if (i < vulnerabilitiesFound) {
      events.push(toEvent(t, logWarn(`Potential SQL injection vulnerability found with payload: ${payloads[i]}`), 'warning'))
    } else {
      events.push(toEvent(t, logInfo(`Payload ${i + 1} — no injection detected`)))
    }
    t += 60
  }

  events.push(toEvent(t, logInfo(`SQL injection probe completed: ${payloadsTested} payloads tested against ${params.targetUrl}`), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Payloads Tested: ${payloadsTested}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Successful Attacks: ${vulnerabilitiesFound}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Failed Attacks: ${payloadsTested - vulnerabilitiesFound}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      targetUrl: params.targetUrl,
      controlName: params.controlName,
      payloadsTested,
      vulnerabilitiesFound,
      failedAttacks: payloadsTested - vulnerabilitiesFound
    },
    explanation: {
      happening: vulnerabilitiesFound > 0
        ? `SQL injection payloads successfully manipulated the query via the '${params.controlName}' parameter, returning unexpected data or triggering error messages that confirm vulnerability.`
        : `${payloadsTested} SQL injection payloads were tested against '${params.controlName}' but the application returned no indicators of vulnerability.`,
      highlights: vulnerabilitiesFound > 0
        ? [`${vulnerabilitiesFound} vulnerability confirmed`, `Parameter: ${params.controlName}`, `${payloadsTested} payloads tested`]
        : ['No vulnerabilities detected', `${payloadsTested} payloads tested`, 'Input appears sanitized'],
      interpretation: vulnerabilitiesFound > 0
        ? `CRITICAL: SQL injection found in '${params.controlName}' at ${params.targetUrl}. An attacker can read, modify, or delete database content. Apply parameterised queries immediately.`
        : `No SQL injection detected. Ensure parameterised queries or prepared statements are used throughout the application.`
    }
  }
}

// ─── Credential Harvester ────────────────────────────────────────────────────

const simulateCredentialHarvester = (scenarioId, params) => {
  const port = params.port || 8080
  const template = params.template || 'login-form'
  const capturedCount = random(0, 5)
  const outputFile = `/captured/credentials_${new Date().toISOString().replace(/[-:.TZ]/g, '').substring(0, 15)}.json`

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo('Initialized credential harvester')))
  t += 50
  events.push(toEvent(t, logInfo(`Template: ${template}, Port: ${port}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Starting credential harvester on port ${port}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Cloning website: ${template}`)))
  t += 100
  events.push(toEvent(t, logInfo('Creating custom login template')))
  t += 100
  events.push(toEvent(t, logInfo('Custom template created successfully')))
  t += 80
  events.push(toEvent(t, logInfo(`Server listening on http://0.0.0.0:${port}`), 'success'))
  t += 200

  for (let i = 1; i <= capturedCount; i++) {
    events.push(toEvent(t, logInfo(`Credentials captured (submission ${i})`), 'success'))
    t += 300
  }

  events.push(toEvent(t, logInfo('Server stopped')))
  t += 30
  events.push(toEvent(t, logInfo(`Template: ${template}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Server port: ${port}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Credentials captured: ${capturedCount}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Output file: ${outputFile}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      template,
      port,
      credentialsCaptured: capturedCount,
      outputFile
    },
    explanation: {
      happening: `A phishing server clones a '${template}' login page and listens on port ${port}. When a user submits the form their credentials are captured and written to ${outputFile}.`,
      highlights: [
        `${capturedCount} credential set(s) captured`,
        `Served on http://localhost:${port}`,
        `Saved to ${outputFile}`
      ],
      interpretation: capturedCount > 0
        ? `Phishing page captured ${capturedCount} credential set(s). All captured data is stored in ${outputFile}. Delete sensitive data after testing and notify affected users.`
        : `No submissions received. Send the phishing link to test users during an authorised awareness exercise.`
    }
  }
}

// ─── PCAP Replay ─────────────────────────────────────────────────────────────

const simulatePcapReplay = (scenarioId, params) => {
  const rate = params.rate || 1.0
  const packetsInFile = random(500, 5000)
  const durationSec = (packetsInFile / (100 * rate)).toFixed(2)
  const bandwidthMb = ((packetsInFile * random(500, 1500)) / 1024 / 1024 * rate).toFixed(2)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo('Initialized PCAP replay')))
  t += 50
  events.push(toEvent(t, logInfo(`PCAP file: ${params.pcapFile}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Interface: ${params.interface}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Replay rate multiplier: ${rate}x`)))
  t += 50
  events.push(toEvent(t, logInfo(`Loading PCAP file: ${params.pcapFile}`)))
  t += 100
  events.push(toEvent(t, logInfo(`Loaded ${packetsInFile} packets`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting replay on ${params.interface} at ${rate}x speed`)))
  t += 80

  const milestones = [0.25, 0.5, 0.75, 1.0]
  for (const pct of milestones) {
    const sent = Math.round(packetsInFile * pct)
    events.push(toEvent(t, logInfo(`Progress: ${(pct * 100).toFixed(0)}% — ${sent}/${packetsInFile} packets replayed`)))
    t += 80
  }

  events.push(toEvent(t, logInfo('PCAP replay completed'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Packets replayed: ${packetsInFile}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Duration: ${durationSec}s`)))
  t += 20
  events.push(toEvent(t, logInfo(`Bandwidth used: ${bandwidthMb} MB`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      pcapFile: params.pcapFile,
      interface: params.interface,
      rateMultiplier: `${rate}x`,
      packetsReplayed: packetsInFile,
      durationSeconds: durationSec,
      bandwidthUsed: `${bandwidthMb} MB`
    },
    explanation: {
      happening: `All ${packetsInFile} packets from ${params.pcapFile} are re-injected onto ${params.interface} at ${rate}x the original capture speed, reproducing the exact traffic pattern for testing defensive controls.`,
      highlights: [
        `${packetsInFile} packets replayed`,
        `${rate}x speed`,
        `${bandwidthMb} MB transmitted`
      ],
      interpretation: `Replayed ${params.pcapFile} (${packetsInFile} packets) at ${rate}x speed consuming ${bandwidthMb} MB. Use this to reproduce specific attack traffic and verify detection rules. Requires raw socket access.`
    }
  }
}

// ─── UDP Flood ───────────────────────────────────────────────────────────────

const simulateUdpFlood = (scenarioId, params) => {
  const packetCount = params.packetCount || 1000
  const rate = 100
  const payloadSize = 512
  const durationSec = (packetCount / rate).toFixed(4)
  const actualRate = (packetCount / parseFloat(durationSec) * random(60, 90) / 100).toFixed(4)
  const trafficKb = ((packetCount * payloadSize) / 1024).toFixed(2)

  const { events } = floodTimeline({
    initMsg: 'Initialized UDP flood attack simulation',
    extraInit: [
      `Target: ${params.targetIp}`,
      `Ports: ${params.ports}`,
      `Starting UDP flood attack against ${params.targetIp}`,
    ],
    summaryLines: [
      `Target: ${params.targetIp}`,
      `Ports: ${params.ports}`,
      `Packets sent: ${packetCount}`,
      `Duration: ${durationSec} seconds`,
      `Configured rate: ${rate} packets/second`,
      `Actual rate: ${actualRate} packets/second`,
      `Rate efficiency: ${(parseFloat(actualRate) / rate * 100).toFixed(2)}%`,
      `Payload size: ${payloadSize} bytes`,
      `Estimated traffic: ${trafficKb} KB`
    ],
    packetCount,
    rate
  })

  return {
    success: true,
    timeline: events,
    metrics: {
      targetIp: params.targetIp,
      ports: params.ports,
      packetsSent: packetCount,
      payloadSizeBytes: payloadSize,
      configuredRate: rate,
      actualRate: parseFloat(actualRate),
      estimatedTraffic: `${trafficKb} KB`,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `${packetCount} UDP packets (${payloadSize} bytes each) are sent to ${params.targetIp}:${params.ports}. UDP is connectionless, so each packet forces the target to check for a listening service and often emit an ICMP Unreachable reply, consuming both inbound and outbound bandwidth.`,
      highlights: [
        `${packetCount} UDP packets sent`,
        `Port ${params.ports} targeted`,
        `${trafficKb} KB estimated traffic`
      ],
      interpretation: `UDP flood sent ${packetCount} packets to ${params.targetIp}:${params.ports} at ~${actualRate} pkt/s, generating ${trafficKb} KB. In a real attack, payload size and rate should be increased to saturate the link. Requires raw socket access.`
    }
  }
}

// ─── ICMP Flood ──────────────────────────────────────────────────────────────

const simulateIcmpFlood = (scenarioId, params) => {
  const packetCount = params.packetCount || 1000
  const packetSize = params.packetSize || 64
  const rate = 100
  const durationSec = (packetCount / rate).toFixed(4)
  const actualRate = (packetCount / parseFloat(durationSec) * random(60, 90) / 100).toFixed(4)
  const trafficKb = ((packetCount * packetSize) / 1024).toFixed(2)

  const { events } = floodTimeline({
    initMsg: 'Initialized ICMP flood attack simulation',
    extraInit: [
      `Target: ${params.targetIp}`,
      `Starting ICMP flood attack against ${params.targetIp}`,
    ],
    summaryLines: [
      `Target: ${params.targetIp}`,
      `Packets sent: ${packetCount}`,
      `Duration: ${durationSec} seconds`,
      `Configured rate: ${rate} packets/second`,
      `Actual rate: ${actualRate} packets/second`,
      `Rate efficiency: ${(parseFloat(actualRate) / rate * 100).toFixed(2)}%`,
      `Packet size: ${packetSize} bytes`,
      `Estimated traffic: ${trafficKb} KB`
    ],
    packetCount,
    rate
  })

  return {
    success: true,
    timeline: events,
    metrics: {
      targetIp: params.targetIp,
      packetsSent: packetCount,
      packetSizeBytes: packetSize,
      configuredRate: rate,
      actualRate: parseFloat(actualRate),
      estimatedTraffic: `${trafficKb} KB`,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `${packetCount} ICMP Echo Request packets (${packetSize} bytes each) are sent to ${params.targetIp}. Each forces the target to process the request and emit an Echo Reply, doubling the effective load on the target's network stack.`,
      highlights: [
        `${packetCount} ICMP packets sent`,
        `Packet size: ${packetSize} bytes`,
        `${trafficKb} KB estimated traffic`
      ],
      interpretation: `ICMP flood sent ${packetCount} × ${packetSize}-byte ping packets to ${params.targetIp} at ~${actualRate} pkt/s. Increase packet size and count to saturate the link. Requires raw socket access (root/sudo).`
    }
  }
}

// ─── MITM ────────────────────────────────────────────────────────────────────

const simulateMitm = (scenarioId, params) => {
  const packetsSent = random(20, 60)
  const durationSec = (packetsSent * 1.0).toFixed(2)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo('Initialized ARP-based MITM attack simulation')))
  t += 50
  events.push(toEvent(t, logInfo(`Target: ${params.targetIp}, Gateway: ${params.gatewayIp}, Interface: ${params.interface}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Resolving MAC address for ${params.targetIp}...`)))
  t += 200
  events.push(toEvent(t, logInfo(`Resolving MAC address for ${params.gatewayIp}...`)))
  t += 200
  events.push(toEvent(t, logInfo('MAC addresses resolved')))
  t += 50
  events.push(toEvent(t, logInfo('Enabling IP forwarding')))
  t += 50
  events.push(toEvent(t, logInfo('Starting ARP poisoning loop')))
  t += 50
  events.push(toEvent(t, logInfo(`Poisoning ${params.targetIp} ← attacker MAC for ${params.gatewayIp}`)))
  t += 80
  events.push(toEvent(t, logInfo(`Poisoning ${params.gatewayIp} ← attacker MAC for ${params.targetIp}`)))
  t += 80
  events.push(toEvent(t, logInfo('ARP poisoning active — traffic intercepted'), 'success'))
  if (params.captureFile) {
    t += 50
    events.push(toEvent(t, logInfo(`Writing captured packets to ${params.captureFile}`)))
  }
  t += 100
  events.push(toEvent(t, logInfo(`MITM complete — packets sent: ${packetsSent}, duration: ${durationSec}s`), 'success'))

  return {
    success: true,
    timeline: events,
    metrics: {
      targetIp: params.targetIp,
      gatewayIp: params.gatewayIp,
      interface: params.interface,
      captureFile: params.captureFile || null,
      arpPairsSent: packetsSent,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `ARP replies poison both ${params.targetIp} and ${params.gatewayIp} to associate the attacker's MAC with each other's IP. All traffic between them now passes through the attacker's machine (IP forwarding is enabled to avoid disruption).`,
      highlights: [
        'Bidirectional ARP poisoning active',
        `Traffic between ${params.targetIp} ↔ ${params.gatewayIp} intercepted`,
        params.captureFile ? `Packets written to ${params.captureFile}` : 'No capture file specified'
      ],
      interpretation: `MITM positioned between ${params.targetIp} and ${params.gatewayIp}. With IP forwarding enabled, traffic is relayed transparently. Use the captureFile option to write intercepted packets to a PCAP for analysis.`
    }
  }
}

// ─── DHCP Starvation ─────────────────────────────────────────────────────────

const simulateDhcpStarvation = (scenarioId, params) => {
  const count = params.count || 1000
  const rate = 10
  const durationSec = (count / rate).toFixed(2)
  const actualRate = (rate * random(85, 100) / 100).toFixed(4)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized DHCP starvation attack on ${params.interface}`)))
  t += 50
  events.push(toEvent(t, logInfo('Starting DHCP starvation attack')))
  t += 30
  events.push(toEvent(t, logInfo(`Sending ${count} requests at ${rate}/sec`)))
  t += 50

  for (let i = 1; i <= Math.min(count, 5); i++) {
    events.push(toEvent(t, logInfo(`Progress: ${i}/${count} requests sent`)))
    t += 60
  }
  if (count > 5) {
    events.push(toEvent(t, logInfo(`... (${count - 5} more requests sent)`)))
    t += 80
  }

  events.push(toEvent(t, logInfo('DHCP starvation attack completed'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`DHCP requests sent: ${count}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Duration: ${durationSec} seconds`)))
  t += 20
  events.push(toEvent(t, logInfo(`Actual rate: ${actualRate} requests/second`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      interface: params.interface,
      requestsSent: count,
      configuredRate: rate,
      actualRate: parseFloat(actualRate),
      durationSeconds: durationSec
    },
    explanation: {
      happening: `${count} DHCP DISCOVER packets are sent with random spoofed MAC addresses on ${params.interface}. Each causes the DHCP server to reserve an IP address, exhausting the available pool so legitimate devices cannot obtain an IP.`,
      highlights: [
        `${count} DHCP DISCOVER packets sent`,
        `Random source MACs used`,
        `Interface: ${params.interface}`
      ],
      interpretation: `DHCP starvation sent ${count} packets at ${actualRate} req/s, consuming ${durationSec}s. Once the pool is exhausted, new devices on the network will fail DHCP and be unable to connect. Requires Layer 2 access to the target VLAN.`
    }
  }
}

// ─── MAC Flooding ────────────────────────────────────────────────────────────

const simulateMacFlooding = (scenarioId, params) => {
  const count = params.count || 10000
  const durationSec = (count / 1000).toFixed(4)
  const actualRate = (count / parseFloat(durationSec) * random(70, 95) / 100).toFixed(1)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized MAC flooding attack on ${params.interface}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting MAC flooding attack: ${count} frames at 100/sec`)))
  t += 50

  for (let i = 1; i <= Math.min(count, 5); i++) {
    events.push(toEvent(t, logInfo(`Progress: ${i}/${count} frames`)))
    t += 30
  }
  if (count > 5) {
    events.push(toEvent(t, logInfo(`... (${count - 5} more frames sent)`)))
    t += 60
  }

  events.push(toEvent(t, logInfo('MAC flooding completed'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Sent ${count} frames in ${durationSec}s`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      interface: params.interface,
      framesSent: count,
      durationSeconds: durationSec,
      actualRate: `${actualRate} frames/s`
    },
    explanation: {
      happening: `${count} Ethernet frames with random source MAC addresses are injected on ${params.interface}. When the switch's CAM table overflows, it enters fail-open (hub) mode and broadcasts all subsequent frames to every port.`,
      highlights: [
        `${count} frames with random MACs`,
        `Interface: ${params.interface}`,
        `Switch enters fail-open / flooding mode`
      ],
      interpretation: `MAC flooding sent ${count} frames in ${durationSec}s. On a vulnerable managed switch this causes CAM table exhaustion. Modern switches with MAC address limiting or port security are not affected.`
    }
  }
}

// ─── VLAN Hopping ────────────────────────────────────────────────────────────

const simulateVlanHopping = (scenarioId, params) => {
  const packetsSent = 10
  const durationSec = '0.007'

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized VLAN hopping: outer=${params.outerVlan}, inner=${params.innerVlan}`)))
  t += 50
  events.push(toEvent(t, logInfo('Starting VLAN hopping with double tagging')))
  t += 50
  events.push(toEvent(t, logInfo(`Crafting double-tagged frames: outer VLAN ${params.outerVlan} / inner VLAN ${params.innerVlan}`)))
  t += 60

  for (let i = 1; i <= packetsSent; i++) {
    events.push(toEvent(t, logInfo(`Sending double-tagged frame ${i}/${packetsSent}`)))
    t += 30
  }

  events.push(toEvent(t, logInfo('VLAN hopping completed'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Sent ${packetsSent} packets in ${durationSec}s`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      interface: params.interface,
      outerVlan: params.outerVlan,
      innerVlan: params.innerVlan,
      targetIp: params.targetIp || null,
      packetsSent,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `Double-tagged 802.1Q frames are injected on ${params.interface}. The switch strips the outer tag (VLAN ${params.outerVlan}) and forwards the frame with the inner tag (VLAN ${params.innerVlan}) to the target VLAN, bypassing VLAN isolation.`,
      highlights: [
        `Outer VLAN ${params.outerVlan} → inner VLAN ${params.innerVlan}`,
        `${packetsSent} double-tagged frames sent`,
        'One-way bypass — requires trunk port misconfiguration'
      ],
      interpretation: `VLAN hopping sent ${packetsSent} double-tagged frames. This attack is one-directional (replies cannot traverse back) and requires the attacker to be on a port that has the native VLAN matching the outer tag. Mitigated by disabling auto-trunking (DTP) and not using VLAN 1 as the native VLAN.`
    }
  }
}

// ─── HTTP Flood ──────────────────────────────────────────────────────────────

const simulateHttpFlood = (scenarioId, params) => {
  const count = params.count || 1000
  const threads = params.threads || 10
  const requestsSent = random(Math.floor(count * 0.9), count)
  const durationSec = (count / (threads * 60)).toFixed(4)
  const rps = (requestsSent / parseFloat(durationSec)).toFixed(4)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized HTTP flood attack on ${params.url}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting HTTP flood: ${count} requests with ${threads} threads`)))
  t += 80

  for (let pct of [0.25, 0.5, 0.75, 1.0]) {
    const sent = Math.round(requestsSent * pct)
    events.push(toEvent(t, logInfo(`Progress: ${Math.round(pct * 100)}% — ${sent}/${count} requests sent`)))
    t += 80
  }

  events.push(toEvent(t, logInfo('HTTP flood completed'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Sent ${requestsSent} requests in ${durationSec}s`)))
  t += 20
  events.push(toEvent(t, logInfo(`Requests Sent: ${requestsSent}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Duration Seconds: ${durationSec}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Requests Per Second: ${rps}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      url: params.url,
      threads,
      requestsSent,
      durationSeconds: durationSec,
      requestsPerSecond: rps
    },
    explanation: {
      happening: `${threads} threads simultaneously send HTTP GET requests to ${params.url}, targeting the application layer. Unlike a SYN flood, each request completes the TCP handshake, making it harder to filter at the network level.`,
      highlights: [
        `${requestsSent} HTTP requests sent`,
        `${threads} parallel threads`,
        `${rps} requests/second`
      ],
      interpretation: `HTTP flood sent ${requestsSent} requests to ${params.url} at ${rps} req/s using ${threads} threads. Application-layer filtering (WAF, rate limiting) is the primary defence.`
    }
  }
}

// ─── XSS ─────────────────────────────────────────────────────────────────────

const simulateXss = (scenarioId, params) => {
  const payloads = 4
  const vulnerabilitiesFound = random(0, payloads)

  const xssPayloads = [
    "<script>alert('XSS')</script>",
    '"><img src=x onerror=alert(1)>',
    "javascript:alert(document.cookie)",
    "<svg/onload=alert('XSS')>"
  ]

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized XSS testing on ${params.url}, parameter: ${params.param}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting XSS testing with ${payloads} payloads`)))
  t += 50

  for (let i = 0; i < payloads; i++) {
    events.push(toEvent(t, logInfo(`Testing payload ${i + 1}/${payloads}`)))
    t += 60
    if (i < vulnerabilitiesFound) {
      events.push(toEvent(t, logWarn(`Potential XSS vulnerability found with payload: ${xssPayloads[i]}`), 'warning'))
    }
    t += 40
  }

  if (vulnerabilitiesFound === 0) {
    events.push(toEvent(t, logInfo('No XSS vulnerabilities detected'), 'success'))
  } else {
    events.push(toEvent(t, logWarn(`Found ${vulnerabilitiesFound} potential vulnerabilities`), 'warning'))
  }
  t += 30
  events.push(toEvent(t, logInfo(`Attempts: ${payloads}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Vulnerabilities Found: ${vulnerabilitiesFound}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      url: params.url,
      param: params.param,
      payloadsTested: payloads,
      vulnerabilitiesFound
    },
    explanation: {
      happening: `${payloads} XSS payloads are injected into the '${params.param}' parameter of ${params.url}. If the application reflects user input without escaping, the injected script executes in the victim's browser.`,
      highlights: [
        vulnerabilitiesFound > 0 ? `${vulnerabilitiesFound} potential XSS vulnerability found` : 'No vulnerabilities detected',
        `${payloads} payloads tested`,
        `Parameter: ${params.param}`
      ],
      interpretation: vulnerabilitiesFound > 0
        ? `XSS vulnerability in '${params.param}' at ${params.url}. An attacker can steal cookies, hijack sessions, or redirect users. Apply output encoding and Content-Security-Policy headers.`
        : `No XSS detected for '${params.param}'. Verify the application encodes all user-controlled output.`
    }
  }
}

// ─── Directory Traversal ─────────────────────────────────────────────────────

const simulateDirectoryTraversal = (scenarioId, params) => {
  const payloads = 5
  const vulnerabilitiesFound = random(0, 1)

  const traversalPayloads = [
    '../../../etc/passwd',
    '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
    '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    '....//....//....//etc/passwd',
    '/etc/passwd%00'
  ]

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized directory traversal testing on ${params.url}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting directory traversal testing with ${payloads} payloads`)))
  t += 50

  for (let i = 0; i < payloads; i++) {
    events.push(toEvent(t, logInfo(`Testing payload ${i + 1}/${payloads}`)))
    t += 80
    if (i < vulnerabilitiesFound) {
      events.push(toEvent(t, logWarn(`Vulnerability found: ${params.url}?${params.param}=${traversalPayloads[i]}`), 'warning'))
    }
    t += 40
  }

  if (vulnerabilitiesFound === 0) {
    events.push(toEvent(t, logInfo('No vulnerabilities detected'), 'success'))
  }
  t += 30
  events.push(toEvent(t, logInfo(`Attempts: ${payloads}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Vulnerabilities Found: ${vulnerabilitiesFound}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      url: params.url,
      param: params.param,
      payloadsTested: payloads,
      vulnerabilitiesFound
    },
    explanation: {
      happening: `${payloads} path traversal payloads are inserted into '${params.param}' to attempt to read files outside the web root, such as /etc/passwd or Windows system files.`,
      highlights: [
        vulnerabilitiesFound > 0 ? `${vulnerabilitiesFound} traversal vulnerability found` : 'No vulnerabilities detected',
        `${payloads} payloads tested`,
        `Parameter: ${params.param}`
      ],
      interpretation: vulnerabilitiesFound > 0
        ? `Directory traversal in '${params.param}' at ${params.url}. An attacker can read arbitrary files. Sanitise file paths and use a chroot jail or allow-list for accessible paths.`
        : `No traversal vulnerability detected. Ensure path components are validated and canonicalised before file access.`
    }
  }
}

// ─── XXE ─────────────────────────────────────────────────────────────────────

const simulateXxe = (scenarioId, params) => {
  const payloads = 2
  const vulnerabilitiesFound = random(0, payloads)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized XXE testing on ${params.url}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting XXE testing with ${payloads} payloads`)))
  t += 50

  for (let i = 0; i < payloads; i++) {
    events.push(toEvent(t, logInfo(`Testing payload ${i + 1}/${payloads}`)))
    t += 60
    if (i < vulnerabilitiesFound) {
      events.push(toEvent(t, logWarn('Potential XXE vulnerability found'), 'warning'))
    }
    t += 40
  }

  if (vulnerabilitiesFound > 0) {
    events.push(toEvent(t, logWarn(`Found ${vulnerabilitiesFound} potential vulnerabilities`), 'warning'))
  } else {
    events.push(toEvent(t, logInfo('No XXE vulnerabilities detected'), 'success'))
  }
  t += 30
  events.push(toEvent(t, logInfo(`Attempts: ${payloads}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Vulnerabilities Found: ${vulnerabilitiesFound}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      url: params.url,
      payloadsTested: payloads,
      vulnerabilitiesFound
    },
    explanation: {
      happening: `${payloads} XML payloads with external entity declarations are POSTed to ${params.url}. If the XML parser resolves external entities, the attacker can read local files or trigger SSRF.`,
      highlights: [
        vulnerabilitiesFound > 0 ? `${vulnerabilitiesFound} potential XXE vulnerability found` : 'No vulnerabilities detected',
        `${payloads} payloads tested`,
        `Endpoint: ${params.url}`
      ],
      interpretation: vulnerabilitiesFound > 0
        ? `XXE vulnerability at ${params.url}. The parser resolves external entities — disable entity expansion in the XML library (e.g., set FEATURE_DISALLOW_DOCTYPE_DECL or equivalent).`
        : `No XXE detected. Ensure external entity processing is disabled in all XML parsers used by the application.`
    }
  }
}

// ─── SSL Strip ───────────────────────────────────────────────────────────────

const simulateSslStrip = (scenarioId, params) => {
  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized SSL Strip simulation on ${params.interface}`)))
  t += 50
  events.push(toEvent(t, logWarn('Note: This is a simplified simulation for educational purposes')))
  t += 30
  events.push(toEvent(t, logInfo('SSL Strip simulation would:')))
  t += 30
  events.push(toEvent(t, logInfo('1. Enable IP forwarding')))
  t += 20
  events.push(toEvent(t, logInfo('2. Setup iptables to redirect traffic')))
  t += 20
  events.push(toEvent(t, logInfo('3. Run MITM proxy to strip HTTPS')))
  t += 20
  events.push(toEvent(t, logInfo('4. Downgrade HTTPS to HTTP')))
  t += 20
  events.push(toEvent(t, logWarn('Real implementation requires mitmproxy or similar tools')))
  t += 30
  events.push(toEvent(t, logInfo('Simulation complete'), 'success'))

  return {
    success: true,
    timeline: events,
    metrics: {
      interface: params.interface,
      mode: 'Educational simulation'
    },
    explanation: {
      happening: 'SSL stripping intercepts HTTPS upgrade redirects, replacing them with HTTP. The victim communicates in plain text with the attacker while the attacker maintains the HTTPS session with the real server.',
      highlights: [
        `Interface: ${params.interface}`,
        'Requires prior MITM position',
        'Simulation only — no real traffic modified'
      ],
      interpretation: `Real SSL stripping requires: (1) MITM position via ARP poisoning, (2) iptables redirect of port 80 to a proxy, (3) proxy intercepts HTTP 301/302 redirects and rewrites https:// to http://. HSTS preloading prevents this attack on protected domains.`
    }
  }
}

// ─── BGP Hijacking ───────────────────────────────────────────────────────────

const simulateBgpHijacking = (scenarioId, params) => {
  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized BGP hijacking simulation for prefix ${params.targetPrefix}`)))
  t += 50
  events.push(toEvent(t, logInfo('BGP hijacking simulation would:')))
  t += 30
  events.push(toEvent(t, logInfo(`1. Announce prefix ${params.targetPrefix} from AS${params.asNumber}`)))
  t += 20
  events.push(toEvent(t, logInfo('2. Advertise more specific route')))
  t += 20
  events.push(toEvent(t, logInfo('3. Attract traffic meant for legitimate AS')))
  t += 20
  events.push(toEvent(t, logWarn('Real implementation requires BGP router access and configuration')))
  t += 30
  events.push(toEvent(t, logInfo('Simulation complete'), 'success'))

  return {
    success: true,
    timeline: events,
    metrics: {
      targetPrefix: params.targetPrefix,
      asNumber: params.asNumber,
      mode: 'Educational simulation'
    },
    explanation: {
      happening: `A BGP UPDATE is simulated announcing ${params.targetPrefix} from AS${params.asNumber} with a more-specific route than the legitimate holder. Routers following the longest-prefix rule would prefer the hijacked route, diverting traffic.`,
      highlights: [
        `Prefix: ${params.targetPrefix}`,
        `Spoofed AS: ${params.asNumber}`,
        'Simulation only — no real BGP session'
      ],
      interpretation: `Real BGP hijacking requires access to a BGP-speaking router with an active peering session. Mitigations include RPKI route origin validation and BGPsec path validation. Highly regulated — illegal without authorisation.`
    }
  }
}

// ─── Smurf Attack ────────────────────────────────────────────────────────────

const simulateSmurfAttack = (scenarioId, params) => {
  const count = params.count || 1000
  const amplification = random(10, 50)
  const durationSec = (count * 2.0 / 100).toFixed(2)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized Smurf attack: victim=${params.victimIp}, broadcast=${params.broadcastIp}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting Smurf attack: sending ${count} packets`)))
  t += 50

  for (let i = 1; i <= Math.min(count, 5); i++) {
    events.push(toEvent(t, logInfo(`Progress: ${i}/${count} packets`)))
    t += 80
  }
  if (count > 5) {
    events.push(toEvent(t, logInfo(`... (${count - 5} more packets sent)`)))
    t += 80
  }

  events.push(toEvent(t, logInfo('Smurf attack completed'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Victim: ${params.victimIp}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Broadcast: ${params.broadcastIp}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Packets sent: ${count}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Estimated amplification factor: ~${amplification}x`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      victimIp: params.victimIp,
      broadcastIp: params.broadcastIp,
      packetsSent: count,
      estimatedAmplification: `~${amplification}x`,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `${count} ICMP Echo Request packets are sent to broadcast address ${params.broadcastIp} with source IP spoofed to ${params.victimIp}. Every host on the broadcast domain replies to the victim, amplifying traffic by ~${amplification}x.`,
      highlights: [
        `${count} packets to broadcast ${params.broadcastIp}`,
        `~${amplification}x amplification toward ${params.victimIp}`,
        'Spoofed source IP'
      ],
      interpretation: `Smurf sent ${count} spoofed ICMP packets. Modern networks block directed broadcasts (RFC 2644) making this largely historical, but useful for understanding amplification principles. Requires raw socket and IP spoofing capability.`
    }
  }
}

// ─── NTP Amplification ───────────────────────────────────────────────────────

const simulateNtpAmplification = (scenarioId, params) => {
  const count = params.count || 1000
  const amplification = random(200, 500)
  const durationSec = (count * 0.002).toFixed(3)

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized NTP amplification attack: victim=${params.victimIp}`)))
  t += 50
  events.push(toEvent(t, logInfo(`NTP server: ${params.ntpServers}`)))
  t += 30
  events.push(toEvent(t, logInfo(`Starting NTP amplification: ${count} queries`)))
  t += 50

  for (let i = 1; i <= Math.min(count, 5); i++) {
    events.push(toEvent(t, logInfo(`Sending NTP monlist query ${i}/${count} (spoofed source: ${params.victimIp})`)))
    t += 50
  }
  if (count > 5) {
    events.push(toEvent(t, logInfo(`... (${count - 5} more queries sent)`)))
    t += 80
  }

  events.push(toEvent(t, logInfo('NTP amplification attack completed'), 'success'))
  t += 30
  events.push(toEvent(t, logInfo(`Victim: ${params.victimIp}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Queries sent: ${count}`)))
  t += 20
  events.push(toEvent(t, logInfo(`Estimated amplification factor: ~${amplification}x`)))
  t += 20
  events.push(toEvent(t, logInfo(`Duration: ${durationSec} seconds`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      victimIp: params.victimIp,
      ntpServer: params.ntpServers,
      queriesSent: count,
      estimatedAmplification: `~${amplification}x`,
      durationSeconds: durationSec
    },
    explanation: {
      happening: `${count} NTP monlist requests are sent with source IP spoofed to ${params.victimIp}. NTP responds with a list of the last 600 clients (~${amplification}x larger than the query), flooding the victim with amplified UDP traffic.`,
      highlights: [
        `${count} NTP monlist queries`,
        `~${amplification}x amplification toward ${params.victimIp}`,
        `NTP server: ${params.ntpServers}`
      ],
      interpretation: `NTP amplification sent ${count} queries achieving ~${amplification}x amplification. Most modern NTP servers have monlist disabled (CVE-2013-5211), but unpatched servers still exist. Requires raw UDP and source IP spoofing.`
    }
  }
}

// ─── FTP Brute Force ─────────────────────────────────────────────────────────

const simulateFtpBruteForce = (scenarioId, params) => {
  const passwordCount = random(5, 20)
  const success = random(0, 100) > 80
  const crackedAt = success ? random(1, passwordCount) : null

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized FTP brute force attack on ${params.host}:${params.port || 21}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting FTP brute force for user '${params.username}' with ${passwordCount} passwords`)))
  t += 50

  for (let i = 1; i <= passwordCount; i++) {
    events.push(toEvent(t, logInfo(`Trying password ${i}/${passwordCount}`)))
    t += 50
    if (success && i === crackedAt) {
      events.push(toEvent(t, logInfo(`Authentication SUCCESS — ${params.username} on ${params.host}`), 'success'))
      t += 30
      break
    }
  }

  if (!success) {
    events.push(toEvent(t, logInfo('Brute force completed - no valid credentials found')))
  }
  t += 30
  events.push(toEvent(t, logInfo(`Attempts: ${success ? crackedAt : passwordCount}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      host: params.host,
      port: params.port || 21,
      username: params.username,
      passwordsTried: success ? crackedAt : passwordCount,
      credentialsFound: success
    },
    explanation: {
      happening: `FTP login attempts are made for user '${params.username}' at ${params.host}:${params.port || 21} using each password from the wordlist at ${params.passwords}.`,
      highlights: [
        success ? `Credentials found after ${crackedAt} attempts` : `${passwordCount} passwords tried — no match`,
        `Username: ${params.username}`,
        `Target: ${params.host}:${params.port || 21}`
      ],
      interpretation: success
        ? `Valid FTP credentials found for '${params.username}' on ${params.host}. Disable FTP (use SFTP/FTPS) and enforce strong passwords or key-based auth.`
        : `No valid credentials found. FTP transfers credentials in cleartext — consider migrating to SFTP regardless.`
    }
  }
}

// ─── RDP Brute Force ─────────────────────────────────────────────────────────

const simulateRdpBruteForce = (scenarioId, params) => {
  const passwordCount = random(5, 15)
  const success = random(0, 100) > 85
  const crackedAt = success ? random(1, passwordCount) : null

  const events = []
  let t = 0
  events.push(toEvent(t, logInfo(`Initialized RDP brute force simulation against ${params.host}:${params.port || 3389}`)))
  t += 50
  events.push(toEvent(t, logInfo(`Starting RDP brute force for user '${params.username}' with ${passwordCount} passwords`)))
  t += 50

  for (let i = 1; i <= passwordCount; i++) {
    events.push(toEvent(t, logInfo(`Trying password ${i}/${passwordCount} (simulated RDP connection)`)))
    t += 60
    if (success && i === crackedAt) {
      events.push(toEvent(t, logInfo(`Authentication SUCCESS — ${params.username} on ${params.host}`), 'success'))
      t += 30
      break
    } else {
      events.push(toEvent(t, logInfo(`Authentication failed for attempt ${i}`), 'warning'))
      t += 30
    }
  }

  if (!success) {
    events.push(toEvent(t, logInfo('Simulation complete - no valid credentials (simulation)')))
  }
  t += 30
  events.push(toEvent(t, logInfo(`Attempts: ${success ? crackedAt : passwordCount}`)))

  return {
    success: true,
    timeline: events,
    metrics: {
      host: params.host,
      port: params.port || 3389,
      username: params.username,
      passwordsTried: success ? crackedAt : passwordCount,
      credentialsFound: success,
      mode: 'Educational simulation'
    },
    explanation: {
      happening: `RDP authentication attempts are simulated for '${params.username}' at ${params.host}:${params.port || 3389}. Real RDP brute force uses the RDP protocol directly and has high detection rates due to Windows event log entries.`,
      highlights: [
        success ? `Credentials found after ${crackedAt} attempts (simulated)` : `${passwordCount} passwords tried — no match`,
        `Username: ${params.username}`,
        'Educational simulation — no real RDP connection made'
      ],
      interpretation: success
        ? `Valid RDP credentials simulated for '${params.username}'. In reality, enable Network Level Authentication (NLA), account lockout policies, and restrict RDP access with firewall rules or a VPN.`
        : `No credentials found. Protect RDP with NLA, strong passwords, geo-IP filtering, and rate-limiting.`
    }
  }
}

// ─── Main dispatcher ─────────────────────────────────────────────────────────

export const simulateAttack = async (attackId, scenarioId, parameters) => {
  const attack = getAttackById(attackId)
  if (!attack) {
    return { success: false, error: `Attack type '${attackId}' not found` }
  }

  const scenario = attack.scenarios.find(s => s.id === scenarioId)
  if (!scenario) {
    return { success: false, error: `Scenario '${scenarioId}' not found for attack '${attackId}'` }
  }

  await new Promise(resolve => setTimeout(resolve, 500))

  switch (attackId) {
    case 'arp-spoof':           return simulateArpSpoofing(scenarioId, parameters)
    case 'syn-flood':           return simulateSynFlood(scenarioId, parameters)
    case 'dns-amplification':   return simulateDnsAmplification(scenarioId, parameters)
    case 'ping-of-death':       return simulatePingOfDeath(scenarioId, parameters)
    case 'http-dos':            return simulateHttpDos(scenarioId, parameters)
    case 'slowloris':           return simulateSlowloris(scenarioId, parameters)
    case 'ssh-brute-force':     return simulateSshBruteForce(scenarioId, parameters)
    case 'sql-injection':       return simulateSqlInjection(scenarioId, parameters)
    case 'credential-harvester': return simulateCredentialHarvester(scenarioId, parameters)
    case 'pcap-replay':         return simulatePcapReplay(scenarioId, parameters)
    case 'udp-flood':           return simulateUdpFlood(scenarioId, parameters)
    case 'icmp-flood':          return simulateIcmpFlood(scenarioId, parameters)
    case 'mitm':                return simulateMitm(scenarioId, parameters)
    case 'dhcp-starvation':     return simulateDhcpStarvation(scenarioId, parameters)
    case 'mac-flooding':        return simulateMacFlooding(scenarioId, parameters)
    case 'vlan-hopping':        return simulateVlanHopping(scenarioId, parameters)
    case 'http-flood':          return simulateHttpFlood(scenarioId, parameters)
    case 'xss':                 return simulateXss(scenarioId, parameters)
    case 'directory-traversal': return simulateDirectoryTraversal(scenarioId, parameters)
    case 'xxe':                 return simulateXxe(scenarioId, parameters)
    case 'ssl-strip':           return simulateSslStrip(scenarioId, parameters)
    case 'bgp-hijacking':       return simulateBgpHijacking(scenarioId, parameters)
    case 'smurf-attack':        return simulateSmurfAttack(scenarioId, parameters)
    case 'ntp-amplification':   return simulateNtpAmplification(scenarioId, parameters)
    case 'ftp-brute-force':     return simulateFtpBruteForce(scenarioId, parameters)
    case 'rdp-brute-force':     return simulateRdpBruteForce(scenarioId, parameters)
    default:
      return { success: false, error: `No simulator implemented for attack '${attackId}'` }
  }
}

export const validateParameters = (attackId, scenarioId, parameters) => {
  const attack = getAttackById(attackId)
  if (!attack) return { valid: false, errors: ['Invalid attack type'] }

  const scenario = attack.scenarios.find(s => s.id === scenarioId)
  if (!scenario) return { valid: false, errors: ['Invalid scenario'] }

  const errors = []
  scenario.parameters.forEach(param => {
    if (param.required && !parameters[param.name]) {
      errors.push(`${param.label} is required`)
    }
  })

  return { valid: errors.length === 0, errors }
}
