# MMT-Attacker Web Interface - Implementation Plan

## Overview
Create a frontend-only web interface to demonstrate the MMT-Attacker playbook with interactive attack simulations, educational content, and simulated results.

## Technical Stack
- **Framework**: Vite + React (JavaScript)
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **Colors**: Gray, Black, White, Dark Green only
- **Design**: Border and shadow effects for block/card layouts
- **Location**: All code in `frontend/` directory

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Layout.jsx
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Select.jsx
│   │   │   ├── Checkbox.jsx
│   │   │   ├── Alert.jsx
│   │   │   ├── Badge.jsx
│   │   │   └── Terminal.jsx
│   │   ├── attack/
│   │   │   ├── AttackTheory.jsx
│   │   │   ├── AttackFlow.jsx (Mermaid diagram renderer)
│   │   │   ├── AttackParameters.jsx
│   │   │   ├── AttackScenario.jsx
│   │   │   ├── AttackResults.jsx
│   │   │   └── AttackExplanation.jsx
│   │   └── home/
│   │       ├── HeroSection.jsx
│   │       ├── AttackTypeCard.jsx
│   │       └── LegalWarning.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── attacks/
│   │   │   ├── ArpSpoofing.jsx
│   │   │   ├── SynFlood.jsx
│   │   │   ├── DnsAmplification.jsx
│   │   │   ├── PingOfDeath.jsx
│   │   │   ├── HttpDos.jsx
│   │   │   ├── Slowloris.jsx
│   │   │   ├── SshBruteForce.jsx
│   │   │   ├── SqlInjection.jsx
│   │   │   ├── CredentialHarvester.jsx
│   │   │   └── PcapReplay.jsx
│   │   └── About.jsx
│   ├── data/
│   │   ├── attacksData.js (Attack definitions, parameters, scenarios)
│   │   ├── mermaidDiagrams.js (Mermaid diagram definitions)
│   │   └── simulationEngine.js (Simulated attack logic)
│   ├── utils/
│   │   ├── parameterValidator.js
│   │   ├── resultGenerator.js
│   │   └── formatters.js
│   ├── hooks/
│   │   ├── useAttackSimulation.js
│   │   └── useFormValidation.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
│   └── favicon.ico
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

---

## Attack Types & Pages

### 1. Network-Layer Attacks

#### 1.1 ARP Spoofing (`/attacks/arp-spoofing`)
**Theory Section:**
- Description of ARP spoofing technique
- How it manipulates ARP protocol
- MAC address spoofing explanation
- Traffic interception mechanism

**Mermaid Diagram:**
- Sequence diagram showing Attacker, Victim, Gateway interaction

**Key Features Display:**
- Bidirectional traffic interception
- MAC address spoofing
- Automatic network restoration
- Real-time traffic monitoring

**Scenarios:**

1. **Network Traffic Monitoring**
   - Parameters:
     - target (IP input, required)
     - gateway (IP input, required)
     - interface (text input, required)
     - bidirectional (checkbox, default: true)
     - packet-log (file path input)
   - Simulated output:
     - Connection status
     - ARP packets sent count
     - Traffic intercepted (bytes/packets)
     - Captured packet summary
   - Explanation:
     - Highlight: ARP poisoning active
     - What's happening: Spoofed ARP responses sent
     - Result interpretation: Traffic successfully redirected

2. **Selective Traffic Interception**
   - Parameters:
     - target (IP input, required)
     - gateway (IP input, required)
     - interface (text input, required)
     - verify (checkbox, default: true)
     - restore-on-exit (checkbox, default: true)
   - Simulated output:
     - Verification status
     - ARP cache poisoning confirmed
     - Interception rate percentage
     - Network stability metrics
   - Explanation:
     - Highlight: Target successfully poisoned
     - What's happening: ARP tables modified
     - Result interpretation: Selective interception working

#### 1.2 SYN Flood (`/attacks/syn-flood`)
**Theory Section:**
- TCP three-way handshake explanation
- SYN flood mechanism
- Resource exhaustion concept
- Half-open connections

**Mermaid Diagram:**
- Graph showing multiple SYN packets, SYN-ACK responses being dropped

**Key Features Display:**
- Randomized source IP addresses
- Customizable packet parameters
- Port range targeting
- Multi-threaded operation

**Scenarios:**

1. **Basic Service Disruption**
   - Parameters:
     - target (IP input, required)
     - port (number input, default: 80)
     - threads (number input, default: 8)
     - randomize-source (checkbox, default: true)
   - Simulated output:
     - Packets sent count
     - Connection attempts
     - Target response time degradation
     - Thread statistics
   - Explanation:
     - Highlight: SYN packets flooding target
     - What's happening: TCP handshake incomplete
     - Result interpretation: Service becoming unresponsive

2. **Multi-Service Attack**
   - Parameters:
     - target (IP input, required)
     - port-range (text input, e.g., "80-443")
     - threads (number input, default: 4)
     - source-ip (text input, default: "random")
     - payload-size (number input, default: 100)
   - Simulated output:
     - Per-port statistics
     - Total packets sent
     - Response time by service
     - Resource exhaustion indicators
   - Explanation:
     - Highlight: Multiple services targeted
     - What's happening: Connection pools filling
     - Result interpretation: Services degraded across ports

#### 1.3 Ping of Death (`/attacks/ping-of-death`)
**Theory Section:**
- Oversized ICMP packets
- IP fragmentation mechanism
- Buffer overflow concept
- System vulnerability

**Mermaid Diagram:**
- Sequence diagram showing fragmented packet sending and reassembly crash

**Key Features Display:**
- Oversized packet generation
- IP fragmentation handling
- Custom packet size control
- System impact analysis

**Scenarios:**

1. **Basic System Testing**
   - Parameters:
     - target (IP input, required)
     - size (number input, default: 65500)
     - count (number input, default: 1)
     - verify (checkbox, default: true)
   - Simulated output:
     - Packets sent
     - Fragmentation details
     - Target response status
     - Vulnerability assessment
   - Explanation:
     - Highlight: Oversized packet sent
     - What's happening: Fragmentation occurring
     - Result interpretation: System vulnerability detected/not detected

2. **Network Stress Test**
   - Parameters:
     - targets-file (textarea for multiple IPs)
     - size (number input, default: 65500)
     - count (number input, default: 50)
     - interval (number input, default: 0.5)
     - fragment-size (number input, default: 1500)
   - Simulated output:
     - Per-target results
     - Total packets sent
     - Fragmentation statistics
     - Network congestion metrics
   - Explanation:
     - Highlight: Multiple systems tested
     - What's happening: Network fragments accumulating
     - Result interpretation: Network stability impact

### 2. Amplification Attacks

#### 2.1 DNS Amplification (`/attacks/dns-amplification`)
**Theory Section:**
- DNS query/response mechanism
- Amplification factor explanation
- Spoofed source IP concept
- Distributed nature of attack

**Mermaid Diagram:**
- Sequence diagram showing small query, large response amplification

**Key Features Display:**
- Multiple DNS server support
- Query type selection
- Amplification factor verification
- Traffic volume monitoring

**Scenarios:**

1. **Basic Amplification Test**
   - Parameters:
     - target (IP input, required)
     - dns-server (IP input, default: "8.8.8.8")
     - query-domain (text input, default: "example.com")
     - verify-amplification (checkbox, default: true)
   - Simulated output:
     - Query size vs response size
     - Amplification factor calculated
     - Traffic volume estimate
     - DNS server response time
   - Explanation:
     - Highlight: Amplification achieved
     - What's happening: DNS responses multiplying traffic
     - Result interpretation: X times amplification detected

2. **Distributed Amplification**
   - Parameters:
     - target (IP input, required)
     - dns-servers-file (textarea for multiple DNS IPs)
     - query-type (select: ANY, TXT, etc.)
     - rotate-dns (checkbox, default: true)
     - threads (number input, default: 4)
     - interval (number input, default: 0.5)
   - Simulated output:
     - Per-server amplification stats
     - Total traffic amplified
     - Query distribution
     - Effective bandwidth multiplication
   - Explanation:
     - Highlight: Multiple amplifiers used
     - What's happening: Distributed DNS responses converging
     - Result interpretation: Massive traffic amplification achieved

### 3. Application-Layer Attacks

#### 3.1 HTTP DoS (`/attacks/http-dos`)
**Theory Section:**
- HTTP request/response mechanism
- Application resource exhaustion
- Worker pool saturation
- Bandwidth consumption

**Mermaid Diagram:**
- Sequence diagram showing multiple threads sending HTTP requests

**Key Features Display:**
- Multiple HTTP methods support
- Custom headers and cookies
- Random path generation
- Multi-threaded operation

**Scenarios:**

1. **Basic Web Server Stress Test**
   - Parameters:
     - target (URL input, required)
     - threads (number input, default: 20)
     - timeout (number input, default: 5)
     - rate-limit (number input, default: 100)
   - Simulated output:
     - Requests sent count
     - Response times
     - Success/failure rate
     - Server load indicators
   - Explanation:
     - Highlight: HTTP flood in progress
     - What's happening: Server workers saturating
     - Result interpretation: Response time increasing

2. **API Endpoint Testing**
   - Parameters:
     - target (URL input, required)
     - method (select: GET, POST, PUT, DELETE)
     - headers (JSON textarea)
     - data (JSON textarea)
     - threads (number input, default: 5)
     - verify-success (checkbox, default: true)
   - Simulated output:
     - Per-endpoint statistics
     - Response status codes distribution
     - API rate limit status
     - Error messages captured
   - Explanation:
     - Highlight: API endpoints stressed
     - What's happening: Backend processing overwhelmed
     - Result interpretation: API throttling/failure observed

#### 3.2 Slowloris (`/attacks/slowloris`)
**Theory Section:**
- Partial HTTP request concept
- Connection pool exhaustion
- Keep-alive mechanism abuse
- Low-bandwidth DoS technique

**Mermaid Diagram:**
- Graph showing multiple partial connections being maintained

**Key Features Display:**
- Connection pool management
- Customizable timing intervals
- SSL/TLS support
- Low bandwidth consumption

**Scenarios:**

1. **Basic Web Server Test**
   - Parameters:
     - target (text input, required)
     - connections (number input, default: 100)
     - verify-vuln (checkbox, default: true)
     - interval (number input, default: 30)
   - Simulated output:
     - Active connections count
     - Connection establishment rate
     - Vulnerability status
     - Server response degradation
   - Explanation:
     - Highlight: Connections held open
     - What's happening: Connection pool filling
     - Result interpretation: Server connection limit reached

2. **Secure Server Testing**
   - Parameters:
     - target (text input, required)
     - ssl (checkbox, default: true)
     - port (number input, default: 443)
     - connections (number input, default: 150)
     - user-agent (text input)
     - proxy (text input, optional)
   - Simulated output:
     - SSL handshake statistics
     - Connection duration
     - Keep-alive effectiveness
     - Server capacity exhaustion
   - Explanation:
     - Highlight: SSL connections maintained
     - What's happening: Encrypted connections held
     - Result interpretation: HTTPS service degraded

#### 3.3 Credential Harvester (`/attacks/credential-harvester`)
**Theory Section:**
- Phishing page concept
- Website cloning technique
- Credential capture mechanism
- Social engineering aspect

**Mermaid Diagram:**
- Graph showing server setup, page clone, credential collection flow

**Key Features Display:**
- Website cloning
- Form customization
- SSL/TLS support
- Credential logging

**Scenarios:**

1. **Basic Awareness Testing**
   - Parameters:
     - template (select: login-form, corporate-login, etc.)
     - port (number input, default: 8080)
     - redirect (URL input)
   - Simulated output:
     - Server status
     - Page views count
     - Form submissions captured
     - Sample captured data (sanitized)
   - Explanation:
     - Highlight: Phishing page active
     - What's happening: Credentials being captured
     - Result interpretation: X users submitted credentials

2. **Advanced Phishing Simulation**
   - Parameters:
     - custom-form (textarea for HTML)
     - port (number input, default: 443)
     - ssl (checkbox, default: true)
     - cert (file path input)
     - key (file path input)
     - redirect (URL input)
     - log-file (text input)
   - Simulated output:
     - HTTPS server running
     - SSL certificate validation
     - Detailed submission logs
     - User interaction timeline
   - Explanation:
     - Highlight: Secure phishing page
     - What's happening: Legitimate-looking HTTPS site
     - Result interpretation: Realistic phishing success rate

### 4. Credential Attacks

#### 4.1 SSH Brute Force (`/attacks/ssh-brute-force`)
**Theory Section:**
- SSH authentication mechanism
- Brute force technique
- Wordlist usage
- Credential testing

**Mermaid Diagram:**
- Graph showing credential attempts loop with success detection

**Key Features Display:**
- Username/password list support
- Connection rate limiting
- Success detection
- Multi-threading support

**Scenarios:**

1. **Single User Testing**
   - Parameters:
     - target (IP input, required)
     - username (text input, required)
     - wordlist (textarea for passwords)
     - delay (number input, default: 2)
     - stop-on-success (checkbox, default: true)
   - Simulated output:
     - Attempts count
     - Current password being tested
     - Success/failure status
     - Time elapsed
   - Explanation:
     - Highlight: Password attempts in progress
     - What's happening: Sequential password testing
     - Result interpretation: Valid credentials found/not found

2. **Multiple Target Scan**
   - Parameters:
     - targets-file (textarea for multiple IPs)
     - usernames-file (textarea for usernames)
     - passwords-file (textarea for passwords)
     - threads (number input, default: 2)
     - timeout (number input, default: 10)
     - output (text input for results file)
   - Simulated output:
     - Per-target progress
     - Total combinations tested
     - Successful authentications list
     - Failed attempt statistics
   - Explanation:
     - Highlight: Network-wide scan
     - What's happening: Distributed credential testing
     - Result interpretation: Weak credentials identified

#### 4.2 SQL Injection (`/attacks/sql-injection`)
**Theory Section:**
- SQL injection vulnerability
- Input sanitization failure
- Database query manipulation
- Data extraction technique

**Mermaid Diagram:**
- Graph showing injection testing, detection, verification, extraction flow

**Key Features Display:**
- Multiple DBMS support
- Form field detection
- Error pattern recognition
- Automated exploitation

**Scenarios:**

1. **Basic Authentication Bypass**
   - Parameters:
     - target (URL input, required)
     - parameter (text input, required)
     - dbms (select: mysql, postgresql, etc.)
     - test-forms (checkbox, default: true)
     - risk (number input 1-3, default: 1)
   - Simulated output:
     - Injection points identified
     - Payload success rate
     - Bypass technique used
     - Access level achieved
   - Explanation:
     - Highlight: SQL injection successful
     - What's happening: Query manipulation
     - Result interpretation: Authentication bypassed

2. **Advanced Data Extraction**
   - Parameters:
     - target (URL input, required)
     - data (text input for POST data)
     - headers (JSON textarea)
     - dbms (select)
     - risk (number input, default: 3)
     - level (number input 1-5, default: 5)
     - proxy (text input, optional)
   - Simulated output:
     - Database structure discovered
     - Tables and columns enumerated
     - Sample data extracted
     - Query reconstruction
   - Explanation:
     - Highlight: Database structure revealed
     - What's happening: Systematic data extraction
     - Result interpretation: Sensitive data exposed

### 5. PCAP Replay

#### 5.1 PCAP Replay (`/attacks/pcap-replay`)
**Theory Section:**
- Packet capture concept
- Traffic replay mechanism
- Timing control
- Protocol reproduction

**Mermaid Diagram:**
- Sequence diagram showing PCAP loading, parsing, filtering, replay

**Key Features Display:**
- PCAP file support
- Packet timing control
- Traffic filtering
- Speed adjustment

**Scenarios:**

1. **HTTP Traffic Replay**
   - Parameters:
     - file (file upload/path input, required)
     - interface (text input, required)
     - filter (text input, e.g., "tcp port 80 or port 443")
     - timing (select: original, fast, custom)
     - modify-ip (checkbox, default: false)
   - Simulated output:
     - Packets read count
     - Packets replayed
     - Timing accuracy
     - Network throughput
   - Explanation:
     - Highlight: Traffic replayed
     - What's happening: Historical packets resent
     - Result interpretation: Original traffic reproduced

2. **DoS Attack Simulation**
   - Parameters:
     - file (file upload/path input, required)
     - interface (text input, required)
     - speed (number input, default: 10.0)
     - loop (number input, default: 5)
     - stats (checkbox, default: true)
     - output (text input for stats file)
   - Simulated output:
     - Total packets sent
     - Bandwidth consumed
     - Loop iterations completed
     - Network impact metrics
   - Explanation:
     - Highlight: Attack traffic amplified
     - What's happening: Accelerated replay
     - Result interpretation: DoS pattern simulated

---

## Page Components Breakdown

### Home Page (`/`)
**Components:**
1. **Hero Section**
   - Title: "MMT-Attacker Demonstration Platform"
   - Subtitle: "Interactive Cybersecurity Attack Simulation"
   - Legal warning banner (prominent, dark green border)

2. **Attack Categories Grid**
   - Network-Layer Attacks (4 cards)
   - Application-Layer Attacks (3 cards)
   - Amplification Attacks (1 card)
   - Credential Attacks (2 cards)
   - PCAP Replay (1 card)

3. **Each Category Card:**
   - Icon (Lucide icon)
   - Attack name
   - Short description
   - "Learn More" button → navigates to attack page
   - Dark border with shadow effect

4. **Footer**
   - Legal disclaimer
   - Educational purpose notice
   - Montimage contact info

### Individual Attack Page Template
**Layout Structure:**

1. **Header Section**
   - Attack name (large heading)
   - Attack category badge
   - Back to home button

2. **Theory Section** (Card with border/shadow)
   - Description text
   - Key concepts highlighted
   - Collapsible for space

3. **Attack Flow Diagram** (Card)
   - Mermaid diagram rendered
   - Visual representation of attack

4. **Key Features** (Card)
   - Bullet list with checkmarks
   - Feature descriptions

5. **Scenarios Tab Navigation**
   - Tab for each scenario
   - Active tab highlighted (dark green)

6. **Active Scenario View** (Large Card)
   - **Parameters Section:**
     - Form with all input fields
     - Field validation
     - Help text for each parameter
     - Required fields marked

   - **Action Button:**
     - "Start Attack Simulation" button (dark green)
     - Loading state during simulation

   - **Results Section:** (appears after simulation)
     - Terminal-style output box
     - Animated text output
     - Color-coded status messages
     - Statistics display

   - **Explanation Section:** (appears after simulation)
     - "What's Happening" box
     - "Result Interpretation" box
     - Highlighted key points (dark green accent)
     - Educational insights

7. **Safety Considerations** (Warning Card)
   - Yellow/warning styling (using gray tones)
   - Bullet points from playbook

---

## Component Design Specifications

### Color Palette
```javascript
// Tailwind config colors
{
  colors: {
    background: '#ffffff',
    surface: '#f9fafb',      // gray-50
    border: '#e5e7eb',        // gray-200
    text: {
      primary: '#000000',
      secondary: '#4b5563',   // gray-600
      muted: '#9ca3af',       // gray-400
    },
    green: {
      dark: '#14532d',        // green-900
      medium: '#15803d',      // green-700
      light: '#16a34a',       // green-600
    }
  }
}
```

### Design System

**Cards:**
```javascript
// Base card style
className="bg-white border-2 border-gray-200 rounded-lg shadow-md p-6"

// Hover effect
className="hover:shadow-lg hover:border-gray-300 transition-all"
```

**Buttons:**
```javascript
// Primary button
className="bg-green-900 text-white px-6 py-3 rounded-lg border-2 border-green-900 shadow-md hover:bg-green-800 hover:shadow-lg transition-all"

// Secondary button
className="bg-white text-gray-900 px-6 py-3 rounded-lg border-2 border-gray-300 shadow-md hover:border-gray-400 hover:shadow-lg transition-all"
```

**Input Fields:**
```javascript
className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-green-700 focus:ring-2 focus:ring-green-200 outline-none"
```

**Terminal Output:**
```javascript
className="bg-black text-white font-mono p-4 rounded-lg border-2 border-gray-800 overflow-auto h-64"
```

**Badges:**
```javascript
className="px-3 py-1 bg-green-900 text-white text-xs font-semibold rounded-full border border-green-800"
```

---

## Data Structure Examples

### Attack Data Structure
```javascript
// src/data/attacksData.js
export const attacksData = {
  'arp-spoofing': {
    id: 'arp-spoofing',
    name: 'ARP Spoofing',
    category: 'Network-Layer',
    description: 'ARP spoofing manipulates...',
    theory: {
      description: '...',
      mechanism: '...',
      impact: '...'
    },
    keyFeatures: [...],
    mermaidDiagram: 'sequenceDiagram...',
    scenarios: [
      {
        id: 'network-monitoring',
        name: 'Network Traffic Monitoring',
        parameters: [
          {
            name: 'target',
            label: 'Target IP',
            type: 'text',
            required: true,
            placeholder: '192.168.1.100',
            validation: 'ipv4',
            helpText: 'IP address to intercept traffic from'
          },
          // ... more parameters
        ],
        simulation: {
          duration: 3000, // ms
          steps: [...] // Animation steps
        }
      },
      // ... more scenarios
    ],
    safetyConsiderations: [...]
  },
  // ... more attacks
}
```

### Simulation Engine
```javascript
// src/data/simulationEngine.js
export const simulateAttack = (attackId, scenarioId, parameters) => {
  // Validate parameters
  // Generate realistic output based on inputs
  // Return simulated results with timeline

  return {
    success: true,
    timeline: [
      { time: 0, message: 'Initializing attack...', type: 'info' },
      { time: 500, message: 'Sending ARP packets...', type: 'progress' },
      { time: 1500, message: 'Target poisoned successfully', type: 'success' },
      // ...
    ],
    metrics: {
      packetsSent: Math.floor(Math.random() * 1000),
      duration: 2500,
      successRate: 95.5,
      // ...
    },
    explanation: {
      happening: 'ARP cache has been poisoned...',
      highlights: ['ARP poisoning active', 'Traffic redirected'],
      interpretation: 'The attack successfully...'
    }
  }
}
```

---

## Implementation Tasks

### Phase 1: Project Setup (Tasks 1-5)
1. **Initialize Vite + React project**
   - Create frontend/ directory
   - Run `npm create vite@latest frontend -- --template react`
   - Install dependencies: `react-router-dom`, `lucide-react`, `mermaid`
   - Configure Vite for proper routing

2. **Configure Tailwind CSS 4**
   - Install Tailwind CSS and dependencies
   - Create `tailwind.config.js` with custom color scheme
   - Set up PostCSS configuration
   - Create base styles in `index.css`
   - Define custom utilities for borders and shadows

3. **Set up project structure**
   - Create all directories as per structure above
   - Set up routing configuration in `App.jsx`
   - Create basic Layout component
   - Configure path aliases in vite.config.js

4. **Create design system components**
   - Button component with variants
   - Card component with shadow/border
   - Input/Select/Checkbox components
   - Alert/Badge components
   - Terminal output component

5. **Set up Mermaid integration**
   - Install and configure Mermaid
   - Create AttackFlow component
   - Test diagram rendering
   - Style diagrams to match color scheme

### Phase 2: Data Layer (Tasks 6-8)
6. **Create attack data structure**
   - Define complete data schema
   - Create attacksData.js with all 10 attacks
   - Include all theory, parameters, scenarios
   - Add Mermaid diagram definitions

7. **Build simulation engine**
   - Create simulationEngine.js
   - Implement realistic result generation
   - Add parameter-based output variation
   - Create timeline animation logic
   - Add metrics calculation

8. **Create parameter validation**
   - IP address validation
   - Port number validation
   - URL validation
   - File path validation
   - JSON validation for complex inputs

### Phase 3: Layout Components (Tasks 9-11)
9. **Build Header component**
   - Logo/branding
   - Navigation menu
   - Mobile responsive menu
   - Dark green accent highlights

10. **Build Sidebar component**
    - Attack categories navigation
    - Collapsible sections
    - Active page highlighting
    - Sticky positioning

11. **Build Footer component**
    - Legal disclaimer
    - Contact information
    - Links to documentation
    - Copyright notice

### Phase 4: Home Page (Tasks 12-14)
12. **Create Hero section**
    - Title and subtitle
    - Legal warning banner
    - Call-to-action buttons
    - Animated entry effects

13. **Build Attack Category cards**
    - Grid layout for categories
    - Individual attack cards
    - Icons from Lucide
    - Hover effects
    - Navigation to attack pages

14. **Add Home page polish**
    - Smooth scrolling
    - Section animations
    - Responsive design
    - Accessibility features

### Phase 5: Attack Page Components (Tasks 15-21)
15. **Create AttackTheory component**
    - Collapsible theory section
    - Formatted description text
    - Key concept highlighting
    - Responsive layout

16. **Create AttackFlow component**
    - Mermaid diagram rendering
    - Responsive sizing
    - Zoom/pan functionality
    - Loading state

17. **Create AttackParameters component**
    - Dynamic form generation from data
    - Field validation
    - Help text tooltips
    - Required field indicators
    - Form state management

18. **Create AttackScenario component**
    - Scenario tab navigation
    - Active scenario highlighting
    - Smooth transitions
    - Parameter form integration

19. **Create AttackResults component**
    - Terminal-style output
    - Animated text rendering
    - Progress indicators
    - Metrics display grid
    - Color-coded messages

20. **Create AttackExplanation component**
    - "What's Happening" section
    - "Result Interpretation" section
    - Highlight boxes
    - Educational content
    - Visual indicators

21. **Build attack page template**
    - Integrate all attack components
    - Page layout structure
    - Responsive design
    - Loading states

### Phase 6: Individual Attack Pages (Tasks 22-31)
22. **Implement ARP Spoofing page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

23. **Implement SYN Flood page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

24. **Implement DNS Amplification page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

25. **Implement Ping of Death page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

26. **Implement HTTP DoS page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

27. **Implement Slowloris page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

28. **Implement SSH Brute Force page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

29. **Implement SQL Injection page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

30. **Implement Credential Harvester page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

31. **Implement PCAP Replay page**
    - Configure attack data
    - Set up both scenarios
    - Test simulation outputs

### Phase 7: Simulation & Interactivity (Tasks 32-35)
32. **Build useAttackSimulation hook**
    - Manage simulation state
    - Handle start/stop/reset
    - Timeline animation control
    - Results state management

33. **Enhance simulation engine**
    - Add realistic delays
    - Create parameter-influenced outputs
    - Add random variations
    - Implement progress callbacks

34. **Add animation effects**
    - Terminal text typing effect
    - Progress bar animations
    - Metric counter animations
    - State transition effects

35. **Implement result highlighting**
    - Syntax highlighting for outputs
    - Color-coded status messages
    - Important data emphasis
    - Success/error visual feedback

### Phase 8: Polish & UX (Tasks 36-40)
36. **Responsive design refinement**
    - Mobile layout optimization
    - Tablet breakpoints
    - Touch-friendly controls
    - Responsive typography

37. **Accessibility improvements**
    - ARIA labels
    - Keyboard navigation
    - Focus indicators
    - Screen reader support

38. **Performance optimization**
    - Code splitting
    - Lazy loading routes
    - Image optimization
    - Bundle size reduction

39. **Error handling**
    - Form validation errors
    - Simulation error states
    - Network error handling
    - User-friendly error messages

40. **Documentation**
    - README.md with setup instructions
    - Component documentation
    - Data structure documentation
    - Deployment guide

---

## Testing Strategy

### Manual Testing Checklist
- [ ] All 10 attack pages render correctly
- [ ] All 20 scenarios (2 per attack) work
- [ ] Parameter validation works for all fields
- [ ] Simulations generate realistic outputs
- [ ] Mermaid diagrams render properly
- [ ] Navigation works smoothly
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Color scheme consistent (gray/black/white/dark green only)
- [ ] Border and shadow effects applied consistently
- [ ] Legal warnings prominently displayed
- [ ] All forms are accessible
- [ ] Keyboard navigation works
- [ ] Loading states display correctly
- [ ] Error handling works gracefully

---

## Future Enhancements (Post-MVP)
1. **Backend Integration**
   - Real attack execution API
   - Result storage
   - User authentication
   - Attack history

2. **Advanced Features**
   - Export results to PDF/JSON
   - Attack comparison tool
   - Learning progress tracking
   - Interactive tutorials

3. **Educational Content**
   - Defense strategies section
   - Mitigation techniques
   - Security best practices
   - Video tutorials

4. **Community Features**
   - Share attack scenarios
   - Custom attack templates
   - Discussion forums
   - Challenge mode

---

## Development Timeline Estimate

- **Phase 1**: 2-3 days
- **Phase 2**: 2-3 days
- **Phase 3**: 1-2 days
- **Phase 4**: 2 days
- **Phase 5**: 3-4 days
- **Phase 6**: 4-5 days
- **Phase 7**: 2-3 days
- **Phase 8**: 2-3 days

**Total Estimated Time**: 18-25 days

---

## Notes
- All colors must be from the approved palette (gray, black, white, dark green)
- Every component should use border and shadow for visual structure
- Simulation results must be realistic and educational
- Legal warnings must be prominently displayed
- Focus on educational value and user understanding
- Mobile-first responsive design approach
- Accessibility is a priority
- Code should be well-commented for future backend integration
