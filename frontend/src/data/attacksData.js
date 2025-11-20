/**
 * MMT-Attacker Attack Data Structure
 * Contains all attack definitions, parameters, and scenarios
 */

export const attacksData = {
  'arp-spoofing': {
    id: 'arp-spoofing',
    name: 'ARP Spoofing',
    category: 'Network-Layer',
    description: 'ARP spoofing manipulates the Address Resolution Protocol to intercept network traffic between targets.',
    theory: {
      description: 'ARP spoofing is a technique that manipulates the Address Resolution Protocol (ARP) to intercept network traffic between targets. The attacker sends falsified ARP messages to link their MAC address with the IP of a legitimate network resource (like the gateway), causing traffic to be redirected through the attacker\'s machine.',
      mechanism: 'The attack works by sending fake ARP replies to both the victim and the gateway, associating the attacker\'s MAC address with their IP addresses. This causes all traffic between the victim and gateway to flow through the attacker\'s system.',
      impact: 'Enables man-in-the-middle attacks, allowing the attacker to intercept, modify, or block network communications between the victim and other network devices.'
    },
    keyFeatures: [
      'Bidirectional traffic interception',
      'MAC address spoofing',
      'Automatic network restoration',
      'Real-time traffic monitoring'
    ],
    mermaidDiagram: `sequenceDiagram
    participant A as Attacker
    participant V as Victim
    participant G as Gateway
    A->>V: Fake ARP: "I am Gateway"
    A->>G: Fake ARP: "I am Victim"
    V->>A: Traffic meant for Gateway
    A->>G: Forward traffic
    G->>A: Response
    A->>V: Forward response`,
    scenarios: [
      {
        id: 'network-monitoring',
        name: 'Network Traffic Monitoring',
        description: 'Monitor all traffic between target and gateway',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to intercept traffic from'
          },
          {
            name: 'gateway',
            label: 'Gateway IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.1',
            validation: 'ipv4',
            helpText: 'Gateway IP address to impersonate'
          },
          {
            name: 'interface',
            label: 'Network Interface',
            type: 'text',
            required: true,
            placeholder: 'eth0',
            helpText: 'Network interface to use (e.g., eth0, wlan0)'
          },
          {
            name: 'bidirectional',
            label: 'Bidirectional',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Intercept traffic in both directions'
          },
          {
            name: 'packetLog',
            label: 'Packet Log Path',
            type: 'text',
            placeholder: '/tmp/captured_traffic.pcap',
            helpText: 'Path to save intercepted packets'
          }
        ]
      },
      {
        id: 'selective-interception',
        name: 'Selective Traffic Interception',
        description: 'Target specific host with verification',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to intercept traffic from'
          },
          {
            name: 'gateway',
            label: 'Gateway IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.1',
            validation: 'ipv4',
            helpText: 'Gateway IP address to impersonate'
          },
          {
            name: 'interface',
            label: 'Network Interface',
            type: 'text',
            required: true,
            placeholder: 'eth0',
            helpText: 'Network interface to use'
          },
          {
            name: 'verify',
            label: 'Verify Attack',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Verify the attack is working'
          },
          {
            name: 'restoreOnExit',
            label: 'Restore on Exit',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Restore original ARP tables on exit'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Always use --restore-on-exit to prevent network disruption',
      'Monitor network stability during the attack',
      'Be cautious with --aggressive mode as it may flood the network',
      'Keep logs for analysis and troubleshooting'
    ]
  },

  'syn-flood': {
    id: 'syn-flood',
    name: 'SYN Flood',
    category: 'Network-Layer',
    description: 'SYN Flood exploits the TCP three-way handshake to exhaust target connection resources.',
    theory: {
      description: 'SYN Flood is a denial-of-service attack that exploits the TCP three-way handshake. The attacker sends multiple SYN packets with spoofed source addresses, causing the target to exhaust its connection resources waiting for responses that will never come.',
      mechanism: 'The attack floods the target with TCP SYN packets. Each SYN packet causes the target to allocate resources for a half-open connection and send a SYN-ACK response. Since the source addresses are spoofed, no ACK is ever sent back, leaving connections in a half-open state until timeout.',
      impact: 'Exhausts server connection tables, preventing legitimate users from establishing connections. Can render services completely unavailable.'
    },
    keyFeatures: [
      'Randomized source IP addresses',
      'Customizable packet parameters',
      'Port range targeting',
      'Multi-threaded operation'
    ],
    mermaidDiagram: `graph LR
    A[Attacker] -->|SYN| T[Target]
    T -->|SYN-ACK| D1[Drop]
    A -->|SYN| T
    T -->|SYN-ACK| D2[Drop]
    A -->|SYN| T
    T -->|SYN-ACK| D3[Drop]`,
    scenarios: [
      {
        id: 'basic-disruption',
        name: 'Basic Service Disruption',
        description: 'Target web server with moderate load',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to flood'
          },
          {
            name: 'port',
            label: 'Target Port',
            type: 'number',
            required: true,
            defaultValue: 80,
            placeholder: '80',
            helpText: 'Single port to target'
          },
          {
            name: 'threads',
            label: 'Number of Threads',
            type: 'number',
            defaultValue: 8,
            placeholder: '8',
            helpText: 'Number of parallel attack threads'
          },
          {
            name: 'randomizeSource',
            label: 'Randomize Source',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Randomize source IP addresses'
          }
        ]
      },
      {
        id: 'multi-service',
        name: 'Multi-Service Attack',
        description: 'Target multiple services with custom parameters',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to flood'
          },
          {
            name: 'portRange',
            label: 'Port Range',
            type: 'text',
            required: true,
            placeholder: '80-443',
            helpText: 'Range of ports to target (e.g., 80-443)'
          },
          {
            name: 'threads',
            label: 'Number of Threads',
            type: 'number',
            defaultValue: 4,
            placeholder: '4',
            helpText: 'Number of parallel threads'
          },
          {
            name: 'sourceIp',
            label: 'Source IP',
            type: 'text',
            defaultValue: 'random',
            placeholder: 'random',
            helpText: 'Source IP or "random" for spoofing'
          },
          {
            name: 'payloadSize',
            label: 'Payload Size (bytes)',
            type: 'number',
            defaultValue: 100,
            placeholder: '100',
            helpText: 'Size of TCP payload'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Start with low thread count and increase gradually',
      'Monitor target\'s response and network congestion',
      'Be cautious with payload size to avoid network saturation',
      'Use packet logging for analysis and troubleshooting',
      'Consider impact on intermediate network devices'
    ]
  },

  'dns-amplification': {
    id: 'dns-amplification',
    name: 'DNS Amplification',
    category: 'Amplification',
    description: 'DNS Amplification exploits DNS resolvers to overwhelm a target with amplified traffic.',
    theory: {
      description: 'DNS Amplification is a DDoS attack that exploits DNS resolvers to overwhelm a target with amplified traffic. The attacker sends DNS queries with a spoofed source IP (the victim\'s IP) to multiple DNS servers. The responses are much larger than the queries, creating an amplification effect that floods the target.',
      mechanism: 'Small DNS queries (typically 60-80 bytes) are sent with the victim\'s IP as the source. DNS servers respond with much larger responses (up to 4000+ bytes), all directed at the victim. The amplification factor can be 50-100x or more.',
      impact: 'Can generate massive amounts of traffic toward the victim, completely saturating their network bandwidth and making services unreachable.'
    },
    keyFeatures: [
      'Multiple DNS server support',
      'Query type selection',
      'Amplification factor verification',
      'Traffic volume monitoring'
    ],
    mermaidDiagram: `sequenceDiagram
    participant A as Attacker
    participant D as DNS Servers
    participant V as Victim
    Note over A,D: Small DNS query with spoofed source IP
    A->>D: Query type ANY for example.com (50 bytes)
    Note over D,V: Large DNS response (4000+ bytes)
    D->>V: Complete DNS record set
    Note over V: Amplification factor: ~80x`,
    scenarios: [
      {
        id: 'basic-amplification',
        name: 'Basic Amplification Test',
        description: 'Test with single DNS server',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to attack'
          },
          {
            name: 'dnsServer',
            label: 'DNS Server',
            type: 'text',
            required: true,
            defaultValue: '8.8.8.8',
            placeholder: '8.8.8.8',
            validation: 'ipv4',
            helpText: 'DNS server to use'
          },
          {
            name: 'queryDomain',
            label: 'Query Domain',
            type: 'text',
            defaultValue: 'example.com',
            placeholder: 'example.com',
            helpText: 'Domain to query'
          },
          {
            name: 'verifyAmplification',
            label: 'Verify Amplification',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Verify amplification ratio'
          }
        ]
      },
      {
        id: 'distributed-amplification',
        name: 'Distributed Amplification',
        description: 'Use multiple DNS servers with rotation',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to attack'
          },
          {
            name: 'dnsServers',
            label: 'DNS Servers (one per line)',
            type: 'textarea',
            required: true,
            placeholder: '8.8.8.8\n8.8.4.4\n1.1.1.1',
            helpText: 'List of DNS servers, one per line'
          },
          {
            name: 'queryType',
            label: 'Query Type',
            type: 'select',
            options: [
              { value: 'ANY', label: 'ANY (Maximum amplification)' },
              { value: 'TXT', label: 'TXT' },
              { value: 'MX', label: 'MX' },
              { value: 'A', label: 'A' }
            ],
            defaultValue: 'ANY',
            helpText: 'DNS query type'
          },
          {
            name: 'rotateDns',
            label: 'Rotate DNS Servers',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Rotate through DNS servers'
          },
          {
            name: 'threads',
            label: 'Number of Threads',
            type: 'number',
            defaultValue: 4,
            placeholder: '4',
            helpText: 'Number of parallel threads'
          },
          {
            name: 'interval',
            label: 'Interval (seconds)',
            type: 'number',
            defaultValue: 0.5,
            placeholder: '0.5',
            helpText: 'Delay between queries'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Verify DNS server responses before attack',
      'Monitor network bandwidth consumption',
      'Be cautious with number of parallel threads',
      'Consider impact on DNS infrastructure',
      'Use appropriate intervals between queries',
      'Regularly update DNS server list'
    ]
  },

  'ping-of-death': {
    id: 'ping-of-death',
    name: 'Ping of Death',
    category: 'Network-Layer',
    description: 'Ping of Death sends oversized ICMP packets that can cause buffer overflows and system crashes.',
    theory: {
      description: 'Ping of Death (PoD) is a denial of service attack that sends oversized or malformed ICMP echo request (ping) packets to a target system. When these packets are fragmented and reassembled at the target, they can cause buffer overflows and system crashes in vulnerable systems.',
      mechanism: 'The attack generates ICMP packets larger than the maximum allowed size (65,535 bytes). These packets are fragmented during transmission. When the target attempts to reassemble them, the oversized packet can overflow buffers, crash network stacks, or cause system instability.',
      impact: 'Can cause system crashes, kernel panics, or service disruptions on vulnerable systems. Modern systems are generally protected, but legacy systems remain vulnerable.'
    },
    keyFeatures: [
      'Oversized packet generation',
      'IP fragmentation handling',
      'Custom packet size control',
      'System impact analysis'
    ],
    mermaidDiagram: `sequenceDiagram
    participant A as Attacker
    participant T as Target
    Note over A: Generate Oversized Packet
    A->>T: Fragment 1 (ICMP Echo Request)
    A->>T: Fragment 2
    A->>T: Fragment N
    Note over T: Buffer Overflow on Reassembly
    Note over T: System Crash`,
    scenarios: [
      {
        id: 'basic-testing',
        name: 'Basic System Testing',
        description: 'Test single system for vulnerability',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to test'
          },
          {
            name: 'size',
            label: 'Packet Size (bytes)',
            type: 'number',
            defaultValue: 65500,
            placeholder: '65500',
            helpText: 'Size of the ping packet'
          },
          {
            name: 'count',
            label: 'Packet Count',
            type: 'number',
            defaultValue: 1,
            placeholder: '1',
            helpText: 'Number of packets to send'
          },
          {
            name: 'verify',
            label: 'Verify Vulnerability',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Test for vulnerability'
          }
        ]
      },
      {
        id: 'network-stress',
        name: 'Network Stress Test',
        description: 'Test multiple systems with varied packet sizes',
        parameters: [
          {
            name: 'targets',
            label: 'Target IPs (one per line)',
            type: 'textarea',
            required: true,
            placeholder: '192.168.1.100\n192.168.1.101\n192.168.1.102',
            helpText: 'List of target IPs, one per line'
          },
          {
            name: 'size',
            label: 'Packet Size (bytes)',
            type: 'number',
            defaultValue: 65500,
            placeholder: '65500',
            helpText: 'Size of the ping packet'
          },
          {
            name: 'count',
            label: 'Packet Count',
            type: 'number',
            defaultValue: 50,
            placeholder: '50',
            helpText: 'Number of packets to send'
          },
          {
            name: 'interval',
            label: 'Interval (seconds)',
            type: 'number',
            defaultValue: 0.5,
            placeholder: '0.5',
            helpText: 'Delay between packets'
          },
          {
            name: 'fragmentSize',
            label: 'Fragment Size (bytes)',
            type: 'number',
            defaultValue: 1500,
            placeholder: '1500',
            helpText: 'Size of IP fragments'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Test on isolated systems first',
      'Monitor target system stability',
      'Start with minimal packet sizes',
      'Use appropriate intervals',
      'Have system recovery procedures ready',
      'Document all testing activities'
    ]
  },

  'http-dos': {
    id: 'http-dos',
    name: 'HTTP DoS',
    category: 'Application-Layer',
    description: 'HTTP DoS overwhelms web applications with a high volume of HTTP requests.',
    theory: {
      description: 'HTTP DoS (Denial of Service) attack targets web applications by overwhelming them with a high volume of HTTP requests. This attack can exhaust server resources, bandwidth, or application worker pools, making the service unavailable to legitimate users.',
      mechanism: 'Multiple threads send continuous HTTP requests to the target server. The requests can be customized with different methods (GET, POST), headers, paths, and data. The volume overwhelms the server\'s ability to process legitimate requests.',
      impact: 'Exhausts server CPU, memory, or connection pools. Can make web applications completely unavailable or significantly degraded for legitimate users.'
    },
    keyFeatures: [
      'Multiple HTTP methods support',
      'Custom headers and cookies',
      'Random path generation',
      'Multi-threaded operation'
    ],
    mermaidDiagram: `sequenceDiagram
    participant A as Attacker
    participant W as Web Server
    loop Multiple Threads
        A->>+W: HTTP Request
        W-->>-A: HTTP Response
    end`,
    scenarios: [
      {
        id: 'web-server-stress',
        name: 'Basic Web Server Stress Test',
        description: 'High-volume GET requests',
        parameters: [
          {
            name: 'target',
            label: 'Target URL',
            type: 'text',
            required: true,
            placeholder: 'http://example.com',
            validation: 'url',
            helpText: 'Target URL to attack'
          },
          {
            name: 'threads',
            label: 'Number of Threads',
            type: 'number',
            defaultValue: 20,
            placeholder: '20',
            helpText: 'Number of parallel threads'
          },
          {
            name: 'timeout',
            label: 'Timeout (seconds)',
            type: 'number',
            defaultValue: 5,
            placeholder: '5',
            helpText: 'Request timeout in seconds'
          },
          {
            name: 'rateLimit',
            label: 'Rate Limit (req/sec/thread)',
            type: 'number',
            defaultValue: 100,
            placeholder: '100',
            helpText: 'Requests per second per thread'
          }
        ]
      },
      {
        id: 'api-endpoint',
        name: 'API Endpoint Testing',
        description: 'Target specific API with authentication',
        parameters: [
          {
            name: 'target',
            label: 'Target URL',
            type: 'text',
            required: true,
            placeholder: 'http://example.com/api',
            validation: 'url',
            helpText: 'API endpoint to target'
          },
          {
            name: 'method',
            label: 'HTTP Method',
            type: 'select',
            options: [
              { value: 'GET', label: 'GET' },
              { value: 'POST', label: 'POST' },
              { value: 'PUT', label: 'PUT' },
              { value: 'DELETE', label: 'DELETE' }
            ],
            defaultValue: 'POST',
            helpText: 'HTTP method to use'
          },
          {
            name: 'headers',
            label: 'Custom Headers (JSON)',
            type: 'textarea',
            placeholder: '{"Authorization": "Bearer token", "Content-Type": "application/json"}',
            validation: 'json',
            helpText: 'Custom HTTP headers as JSON'
          },
          {
            name: 'data',
            label: 'POST Data (JSON)',
            type: 'textarea',
            placeholder: '{"test": "data"}',
            validation: 'json',
            helpText: 'Request body as JSON'
          },
          {
            name: 'threads',
            label: 'Number of Threads',
            type: 'number',
            defaultValue: 5,
            placeholder: '5',
            helpText: 'Number of parallel threads'
          },
          {
            name: 'verifySuccess',
            label: 'Verify Success',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Verify successful requests'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Start with low thread count and rate limits',
      'Monitor server response times and error rates',
      'Be cautious with random path generation',
      'Verify impact on application resources',
      'Consider effects on shared hosting environments'
    ]
  },

  'slowloris': {
    id: 'slowloris',
    name: 'Slowloris',
    category: 'Application-Layer',
    description: 'Slowloris maintains many partial HTTP connections to exhaust server connection pools.',
    theory: {
      description: 'Slowloris is a low-bandwidth denial of service attack that works by maintaining many partial HTTP connections to the target web server. It sends HTTP requests in pieces very slowly, keeping connections open for as long as possible. This exhausts the server\'s connection pool, preventing legitimate users from connecting.',
      mechanism: 'Opens many connections and sends partial HTTP headers slowly. Periodically sends additional headers to keep connections alive. The server keeps these connections open, waiting for the complete request that never comes.',
      impact: 'Exhausts server connection pools with minimal bandwidth. Can make web servers completely unavailable while using very little attacker resources. Difficult to detect as traffic appears legitimate.'
    },
    keyFeatures: [
      'Connection pool management',
      'Customizable timing intervals',
      'SSL/TLS support',
      'Low bandwidth consumption'
    ],
    mermaidDiagram: `graph TB
    A[Attacker] -->|Partial HTTP Request 1| S[Server]
    A -->|Partial HTTP Request 2| S
    A -->|Partial HTTP Request 3| S
    A -->|Keep-Alive Headers| S
    A -->|Periodic Headers| S
    Note["Keep connections open<br/>by sending periodic<br/>partial headers"] --> A`,
    scenarios: [
      {
        id: 'basic-web-test',
        name: 'Basic Web Server Test',
        description: 'Test with minimal connections',
        parameters: [
          {
            name: 'target',
            label: 'Target Hostname',
            type: 'text',
            required: true,
            placeholder: 'example.com',
            helpText: 'Target hostname or IP'
          },
          {
            name: 'connections',
            label: 'Number of Connections',
            type: 'number',
            defaultValue: 100,
            placeholder: '100',
            helpText: 'Number of connections to maintain'
          },
          {
            name: 'verifyVuln',
            label: 'Verify Vulnerability',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Test if target is vulnerable'
          },
          {
            name: 'interval',
            label: 'Keep-Alive Interval (seconds)',
            type: 'number',
            defaultValue: 30,
            placeholder: '30',
            helpText: 'Interval between sending headers'
          }
        ]
      },
      {
        id: 'secure-server',
        name: 'Secure Server Testing',
        description: 'Test SSL with custom configuration',
        parameters: [
          {
            name: 'target',
            label: 'Target Hostname',
            type: 'text',
            required: true,
            placeholder: 'example.com',
            helpText: 'Target hostname'
          },
          {
            name: 'ssl',
            label: 'Use SSL/TLS',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Use HTTPS connection'
          },
          {
            name: 'port',
            label: 'Port',
            type: 'number',
            defaultValue: 443,
            placeholder: '443',
            helpText: 'Target port'
          },
          {
            name: 'connections',
            label: 'Number of Connections',
            type: 'number',
            defaultValue: 150,
            placeholder: '150',
            helpText: 'Number of connections to maintain'
          },
          {
            name: 'userAgent',
            label: 'User-Agent',
            type: 'text',
            placeholder: 'Mozilla/5.0',
            helpText: 'Custom User-Agent string'
          },
          {
            name: 'proxy',
            label: 'Proxy',
            type: 'text',
            placeholder: 'socks5://127.0.0.1:9050',
            helpText: 'HTTP/SOCKS proxy for connections'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Start with a low number of connections',
      'Monitor server\'s response time and error logs',
      'Be aware of server\'s connection timeout settings',
      'Use --verify-vuln before full attack',
      'Consider impact on shared hosting environments',
      'Monitor local resource usage'
    ]
  },

  'ssh-brute-force': {
    id: 'ssh-brute-force',
    name: 'SSH Brute Force',
    category: 'Credential',
    description: 'SSH Brute Force attempts to gain unauthorized access by systematically trying username/password combinations.',
    theory: {
      description: 'SSH Brute Force attack attempts to gain unauthorized access to SSH servers by systematically trying various username and password combinations. The attack can target a single host or multiple hosts, using wordlists for both usernames and passwords, with options for parallel attempts and rate limiting.',
      mechanism: 'Iterates through lists of usernames and passwords, attempting to authenticate to SSH servers. Uses parallel connections to speed up the process while respecting rate limits to avoid detection or account lockouts.',
      impact: 'Can compromise systems with weak credentials. Successful attacks provide command-line access to the target system. May trigger account lockouts or intrusion detection systems.'
    },
    keyFeatures: [
      'Username/password list support',
      'Connection rate limiting',
      'Success detection',
      'Multi-threading support'
    ],
    mermaidDiagram: `graph TB
    Start[Start Attack] --> Config[Configure Attack]
    Config --> Load[Load Wordlists]
    Load --> Init[Initialize Connections]
    Init --> Loop[Try Credentials]
    Loop --> Check{Success?}
    Check -->|No| Rate[Rate Limit]
    Rate --> NextCred[Next Credentials]
    NextCred --> Loop
    Check -->|Yes| Log[Log Success]
    Log --> Continue{Continue?}
    Continue -->|Yes| NextCred
    Continue -->|No| End[End Attack]`,
    scenarios: [
      {
        id: 'single-user',
        name: 'Single User Testing',
        description: 'Test specific user account',
        parameters: [
          {
            name: 'target',
            label: 'Target IP Address',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'SSH server IP address'
          },
          {
            name: 'username',
            label: 'Username',
            type: 'text',
            required: true,
            placeholder: 'root',
            helpText: 'Username to test'
          },
          {
            name: 'wordlist',
            label: 'Password Wordlist (one per line)',
            type: 'textarea',
            required: true,
            placeholder: 'password123\nadmin\nletmein',
            helpText: 'List of passwords to try'
          },
          {
            name: 'delay',
            label: 'Delay (seconds)',
            type: 'number',
            defaultValue: 2,
            placeholder: '2',
            helpText: 'Delay between attempts'
          },
          {
            name: 'stopOnSuccess',
            label: 'Stop on Success',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Stop after finding valid credentials'
          }
        ]
      },
      {
        id: 'multi-target',
        name: 'Multiple Target Scan',
        description: 'Scan network range with common credentials',
        parameters: [
          {
            name: 'targets',
            label: 'Target IPs (one per line)',
            type: 'textarea',
            required: true,
            placeholder: '192.168.1.100\n192.168.1.101\n192.168.1.102',
            helpText: 'List of SSH server IPs'
          },
          {
            name: 'usernames',
            label: 'Usernames (one per line)',
            type: 'textarea',
            required: true,
            placeholder: 'root\nadmin\nuser',
            helpText: 'List of usernames to try'
          },
          {
            name: 'passwords',
            label: 'Passwords (one per line)',
            type: 'textarea',
            required: true,
            placeholder: 'password\nadmin123\ndefault',
            helpText: 'List of passwords to try'
          },
          {
            name: 'threads',
            label: 'Number of Threads',
            type: 'number',
            defaultValue: 2,
            placeholder: '2',
            helpText: 'Number of parallel attempts'
          },
          {
            name: 'timeout',
            label: 'Connection Timeout (seconds)',
            type: 'number',
            defaultValue: 10,
            placeholder: '10',
            helpText: 'SSH connection timeout'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Use appropriate delays to avoid account lockouts',
      'Monitor for security system alerts',
      'Be cautious with thread count to avoid DoS',
      'Keep logs of all testing activities',
      'Respect target system\'s security policies',
      'Consider impact on legitimate users'
    ]
  },

  'sql-injection': {
    id: 'sql-injection',
    name: 'SQL Injection',
    category: 'Credential',
    description: 'SQL Injection identifies vulnerabilities where user input is improperly sanitized in SQL queries.',
    theory: {
      description: 'SQL Injection testing identifies vulnerabilities in web applications where user input is improperly sanitized before being used in SQL queries. The tool systematically tests various injection points with different payloads, analyzing responses to detect successful injections and potential database exposure.',
      mechanism: 'Injects SQL code into application inputs (forms, URLs, cookies). Analyzes error messages and response patterns to identify vulnerabilities. Can extract database schema, data, and potentially gain administrative access.',
      impact: 'Can expose entire databases, bypass authentication, modify or delete data, and potentially compromise the entire application and underlying system.'
    },
    keyFeatures: [
      'Multiple DBMS support',
      'Form field detection',
      'Error pattern recognition',
      'Automated exploitation'
    ],
    mermaidDiagram: `graph TB
    Start[Start Scan] --> Config[Configure Test]
    Config --> Analyze[Analyze Target]
    Analyze --> Points[Identify Injection Points]
    Points --> Test[Test Injection]
    Test --> Detect{Vulnerable?}
    Detect -->|Yes| Verify[Verify Exploit]
    Detect -->|No| Next[Next Payload]
    Next --> Test
    Verify --> Report[Generate Report]
    Verify --> Extract[Extract Data]
    Extract --> Cleanup[Cleanup]`,
    scenarios: [
      {
        id: 'auth-bypass',
        name: 'Basic Authentication Bypass',
        description: 'Test login form',
        parameters: [
          {
            name: 'target',
            label: 'Target URL',
            type: 'text',
            required: true,
            placeholder: 'http://example.com/login',
            validation: 'url',
            helpText: 'URL of the login page'
          },
          {
            name: 'parameter',
            label: 'Parameter to Test',
            type: 'text',
            required: true,
            placeholder: 'username',
            helpText: 'Form parameter to test'
          },
          {
            name: 'dbms',
            label: 'Database Type',
            type: 'select',
            options: [
              { value: 'mysql', label: 'MySQL' },
              { value: 'postgresql', label: 'PostgreSQL' },
              { value: 'mssql', label: 'MS SQL Server' },
              { value: 'oracle', label: 'Oracle' }
            ],
            defaultValue: 'mysql',
            helpText: 'Target database type'
          },
          {
            name: 'testForms',
            label: 'Test Form Fields',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Automatically test form fields'
          },
          {
            name: 'risk',
            label: 'Risk Level (1-3)',
            type: 'number',
            defaultValue: 1,
            placeholder: '1',
            helpText: 'Risk level of tests to perform'
          }
        ]
      },
      {
        id: 'data-extraction',
        name: 'Advanced Data Extraction',
        description: 'Comprehensive parameter testing',
        parameters: [
          {
            name: 'target',
            label: 'Target URL',
            type: 'text',
            required: true,
            placeholder: 'http://example.com/api',
            validation: 'url',
            helpText: 'API or page URL'
          },
          {
            name: 'data',
            label: 'POST Data',
            type: 'text',
            placeholder: 'id=1&type=user',
            helpText: 'POST data to include'
          },
          {
            name: 'headers',
            label: 'Custom Headers (JSON)',
            type: 'textarea',
            placeholder: '{"X-API-Key": "test"}',
            validation: 'json',
            helpText: 'Custom HTTP headers'
          },
          {
            name: 'dbms',
            label: 'Database Type',
            type: 'select',
            options: [
              { value: 'mysql', label: 'MySQL' },
              { value: 'postgresql', label: 'PostgreSQL' },
              { value: 'mssql', label: 'MS SQL Server' },
              { value: 'oracle', label: 'Oracle' }
            ],
            defaultValue: 'postgresql',
            helpText: 'Target database type'
          },
          {
            name: 'risk',
            label: 'Risk Level (1-3)',
            type: 'number',
            defaultValue: 3,
            placeholder: '3',
            helpText: 'Risk level of tests'
          },
          {
            name: 'level',
            label: 'Test Level (1-5)',
            type: 'number',
            defaultValue: 5,
            placeholder: '5',
            helpText: 'Thoroughness of testing'
          },
          {
            name: 'proxy',
            label: 'Proxy',
            type: 'text',
            placeholder: 'http://127.0.0.1:8080',
            helpText: 'HTTP proxy for requests'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Only test applications you have permission to test',
      'Be aware that SQL injection can modify or delete data',
      'Use lower risk/level settings initially',
      'Monitor application behavior during testing',
      'Document all findings responsibly',
      'Follow responsible disclosure practices'
    ]
  },

  'credential-harvester': {
    id: 'credential-harvester',
    name: 'Credential Harvester',
    category: 'Application-Layer',
    description: 'Credential Harvester creates phishing pages to collect submitted credentials.',
    theory: {
      description: 'The Credential Harvester creates convincing phishing pages by cloning legitimate login forms and collecting submitted credentials. This tool helps security teams test user awareness and validate security controls against phishing attacks.',
      mechanism: 'Clones target websites or uses templates to create convincing login pages. Runs a web server to host the phishing page. Captures and logs credentials when users submit the form. Can redirect to the real site after capture to avoid suspicion.',
      impact: 'Tests organizational susceptibility to phishing. Educates users about phishing risks. Validates email filtering and user training effectiveness.'
    },
    keyFeatures: [
      'Website cloning',
      'Form customization',
      'SSL/TLS support',
      'Credential logging'
    ],
    mermaidDiagram: `graph TB
    Start[Start Server] --> Clone[Clone Target Site]
    Clone --> Customize[Customize Forms]
    Customize --> Listen[Listen for Connections]
    Listen --> Process{Process Request}
    Process -->|Valid Form| Collect[Collect Credentials]
    Process -->|Other| Redirect[Redirect to Real Site]
    Collect --> Log[Log Data]
    Collect --> Redirect`,
    scenarios: [
      {
        id: 'basic-awareness',
        name: 'Basic Awareness Testing',
        description: 'Simple login page clone',
        parameters: [
          {
            name: 'template',
            label: 'Template',
            type: 'select',
            options: [
              { value: 'login-form', label: 'Generic Login Form' },
              { value: 'corporate-login', label: 'Corporate Login' },
              { value: 'email-login', label: 'Email Login' },
              { value: 'social-media', label: 'Social Media Login' }
            ],
            defaultValue: 'login-form',
            helpText: 'Predefined template to use'
          },
          {
            name: 'port',
            label: 'Server Port',
            type: 'number',
            defaultValue: 8080,
            placeholder: '8080',
            helpText: 'Port to listen on'
          },
          {
            name: 'redirect',
            label: 'Redirect URL',
            type: 'text',
            placeholder: 'https://company.com',
            validation: 'url',
            helpText: 'URL to redirect after submission'
          }
        ]
      },
      {
        id: 'advanced-phishing',
        name: 'Advanced Phishing Simulation',
        description: 'Custom form with SSL and logging',
        parameters: [
          {
            name: 'customForm',
            label: 'Custom HTML Form',
            type: 'textarea',
            placeholder: '<form>...</form>',
            helpText: 'Custom HTML form code'
          },
          {
            name: 'port',
            label: 'Server Port',
            type: 'number',
            defaultValue: 443,
            placeholder: '443',
            helpText: 'Port to listen on'
          },
          {
            name: 'ssl',
            label: 'Enable SSL/TLS',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Use HTTPS'
          },
          {
            name: 'cert',
            label: 'SSL Certificate Path',
            type: 'text',
            placeholder: '/path/to/cert.pem',
            helpText: 'Path to SSL certificate'
          },
          {
            name: 'key',
            label: 'SSL Key Path',
            type: 'text',
            placeholder: '/path/to/key.pem',
            helpText: 'Path to SSL private key'
          },
          {
            name: 'redirect',
            label: 'Redirect URL',
            type: 'text',
            placeholder: 'https://company.com',
            validation: 'url',
            helpText: 'URL to redirect after submission'
          },
          {
            name: 'logFile',
            label: 'Log File Path',
            type: 'text',
            placeholder: '/tmp/harvest.json',
            helpText: 'Path to save captured credentials'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Use only in authorized testing',
      'Handle captured data securely',
      'Delete sensitive data after testing',
      'Monitor for unauthorized access',
      'Document all test activities',
      'Inform relevant security teams'
    ]
  },

  'pcap-replay': {
    id: 'pcap-replay',
    name: 'PCAP Replay',
    category: 'Other',
    description: 'PCAP Replay reproduces previously captured network traffic for testing and analysis.',
    theory: {
      description: 'PCAP Replay functionality allows for the reproduction of previously captured network traffic. This is useful for testing network security controls, analyzing protocol behaviors, and reproducing specific network conditions or attacks. The tool provides control over packet timing, filtering, and interface selection.',
      mechanism: 'Reads packets from PCAP files and replays them onto the network. Can modify timing, filter specific traffic, adjust replay speed, and modify packet contents. Supports looping and statistical analysis.',
      impact: 'Enables reproduction of network attacks for testing defensive measures. Allows protocol analysis and troubleshooting. Can simulate various network conditions and loads.'
    },
    keyFeatures: [
      'PCAP file support',
      'Packet timing control',
      'Traffic filtering',
      'Speed adjustment'
    ],
    mermaidDiagram: `sequenceDiagram
    participant A as Attacker
    participant N as Network
    participant T as Target
    A->>A: Load PCAP File
    A->>A: Parse Packets
    A->>A: Apply Filters
    Note over A: Configure Timing
    loop Replay Sequence
        A->>N: Send Packet
        Note over N: Network Transit
        N->>T: Packet Arrives
        Note over A: Timing Control
        Note over T: Monitor Response
    end
    Note over A: Statistics Collection`,
    scenarios: [
      {
        id: 'http-replay',
        name: 'HTTP Traffic Replay',
        description: 'Replay web traffic',
        parameters: [
          {
            name: 'file',
            label: 'PCAP File Path',
            type: 'text',
            required: true,
            placeholder: '/path/to/capture.pcap',
            helpText: 'Path to PCAP file'
          },
          {
            name: 'interface',
            label: 'Network Interface',
            type: 'text',
            required: true,
            placeholder: 'eth0',
            helpText: 'Interface to replay on'
          },
          {
            name: 'filter',
            label: 'BPF Filter',
            type: 'text',
            placeholder: 'tcp port 80 or port 443',
            helpText: 'Berkeley Packet Filter expression'
          },
          {
            name: 'timing',
            label: 'Timing Mode',
            type: 'select',
            options: [
              { value: 'original', label: 'Original (Real timing)' },
              { value: 'fast', label: 'Fast (No delays)' },
              { value: 'custom', label: 'Custom' }
            ],
            defaultValue: 'original',
            helpText: 'How to handle packet timing'
          },
          {
            name: 'modifyIp',
            label: 'Modify IP Addresses',
            type: 'checkbox',
            defaultValue: false,
            helpText: 'Modify source/dest IPs'
          }
        ]
      },
      {
        id: 'dos-simulation',
        name: 'DoS Attack Simulation',
        description: 'Replay attack traffic at high speed',
        parameters: [
          {
            name: 'file',
            label: 'PCAP File Path',
            type: 'text',
            required: true,
            placeholder: '/path/to/dos_attack.pcap',
            helpText: 'Path to PCAP file'
          },
          {
            name: 'interface',
            label: 'Network Interface',
            type: 'text',
            required: true,
            placeholder: 'eth0',
            helpText: 'Interface to replay on'
          },
          {
            name: 'speed',
            label: 'Replay Speed Multiplier',
            type: 'number',
            defaultValue: 10.0,
            placeholder: '10.0',
            helpText: 'Speed multiplier (10 = 10x faster)'
          },
          {
            name: 'loop',
            label: 'Loop Count',
            type: 'number',
            defaultValue: 5,
            placeholder: '5',
            helpText: 'Number of times to loop'
          },
          {
            name: 'stats',
            label: 'Collect Statistics',
            type: 'checkbox',
            defaultValue: true,
            helpText: 'Collect and display statistics'
          },
          {
            name: 'output',
            label: 'Statistics Output File',
            type: 'text',
            placeholder: '/tmp/replay_stats.json',
            helpText: 'Path to save statistics'
          }
        ]
      }
    ],
    safetyConsiderations: [
      'Verify target environment capacity',
      'Monitor network bandwidth usage',
      'Be cautious with replay speed settings',
      'Consider impact on production systems',
      'Test filters before full replay',
      'Monitor system resources',
      'Keep replay logs for analysis'
    ]
  }
}

/**
 * Get attack by ID
 */
export const getAttackById = (id) => {
  return attacksData[id]
}

/**
 * Get all attacks
 */
export const getAllAttacks = () => {
  return Object.values(attacksData)
}

/**
 * Get attacks by category
 */
export const getAttacksByCategory = (category) => {
  return Object.values(attacksData).filter(attack => attack.category === category)
}

/**
 * Get all categories
 */
export const getCategories = () => {
  const categories = [...new Set(Object.values(attacksData).map(attack => attack.category))]
  return categories
}
