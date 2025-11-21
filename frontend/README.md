# MMT-Attacker Web Interface

Interactive web interface for demonstrating cybersecurity attacks from the MMT-Attacker playbook. Built with React, Vite, and Tailwind CSS.

## 🚀 Features

- **10 Attack Types** with detailed simulations:
  - Network Layer: ARP Spoofing, SYN Flood, Ping of Death
  - Application Layer: HTTP DoS, Slowloris, Credential Harvester
  - Amplification: DNS Amplification
  - Credential: SSH Brute Force, SQL Injection
  - Other: PCAP Replay

- **20 Attack Scenarios** (2 per attack type)
- **Interactive Simulations** with realistic output
- **Educational Content** with theory, diagrams, and explanations
- **Responsive Design** for desktop, tablet, and mobile
- **Real-time Validation** of attack parameters
- **Animated Results** with terminal-style output

## 📋 Prerequisites

- Node.js 18+
- npm 9+

## 🛠️ Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## 💻 Development

```bash
# Start development server
npm run dev

# Server will start on http://localhost:3000
```

The app will automatically reload when you make changes to the source code.

## 🏗️ Build

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

The optimized build will be output to the `dist/` directory.

## ☁️ Deployment

### Netlify Deployment

This project is configured for easy deployment on Netlify with zero-config setup.

#### Option 1: Deploy via Netlify CLI

```bash
# Install Netlify CLI globally
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy to production
netlify deploy --prod
```

#### Option 2: Deploy via Git Integration

1. Push your code to GitHub, GitLab, or Bitbucket
2. Go to [Netlify](https://app.netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Connect your repository
5. Netlify will auto-detect the configuration from `netlify.toml`
6. Click "Deploy site"

#### Option 3: Manual Deploy

```bash
# Build the project
npm run build

# Drag and drop the `dist/` folder to Netlify's deploy interface
# Or use the Netlify CLI:
netlify deploy --prod --dir=dist
```

### Configuration

The project includes:
- `netlify.toml` - Netlify configuration with build settings, redirects, and headers
- `public/_redirects` - SPA routing redirects (backup for netlify.toml)

#### Build Settings (from netlify.toml)
- **Base directory**: `frontend/`
- **Build command**: `npm run build`
- **Publish directory**: `dist/`
- **Node version**: 20

#### Environment Variables

No environment variables are required for the demo version. For production with backend integration, add:
- `VITE_API_URL` - Backend API endpoint

### Custom Domain

After deployment:
1. Go to Site settings → Domain management
2. Add your custom domain
3. Configure DNS records as instructed by Netlify

### Performance Optimizations

The deployment includes:
- Static asset caching (1 year)
- HTML caching disabled for updates
- Security headers (XSS, frame options, etc.)
- Gzip/Brotli compression (automatic)
- CDN distribution (automatic)

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/          # Header, Footer, Sidebar
│   │   ├── common/          # Reusable components (Button, Card, Input, etc.)
│   │   ├── attack/          # Attack-specific components
│   │   └── home/            # Home page components
│   ├── pages/
│   │   ├── Home.jsx         # Landing page
│   │   └── attacks/         # Attack page templates
│   ├── data/
│   │   ├── attacksData.js         # All attack definitions
│   │   └── simulationEngine.js   # Simulation logic
│   ├── utils/
│   │   └── parameterValidator.js  # Input validation
│   ├── hooks/
│   │   └── useAttackSimulation.js # Simulation state management
│   ├── App.jsx              # Main app component
│   ├── main.jsx            # App entry point
│   └── index.css           # Global styles
├── public/                  # Static assets
├── index.html              # HTML template
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── package.json           # Dependencies and scripts
```

## 🎨 Technology Stack

- **Framework**: React 19
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **Diagrams**: Mermaid
- **Routing**: React Router DOM

## 🎯 Key Components

### Layout Components
- **Header**: Navigation and branding
- **Sidebar**: Attack category navigation
- **Footer**: Legal disclaimer and contact info

### Common Components
- **Button**: Primary, secondary, outline variants
- **Card**: Container with shadow and border
- **Input/Select/Checkbox**: Form controls with validation
- **Terminal**: Black terminal-style output display
- **Alert**: Info, warning, success, error messages
- **Badge**: Category and status indicators

### Attack Components
- **AttackTheory**: Collapsible theory section
- **AttackFlow**: Mermaid diagram renderer
- **AttackParameters**: Dynamic form generator
- **AttackScenario**: Tab navigation and scenario execution
- **AttackResults**: Terminal output and metrics
- **AttackExplanation**: Educational interpretation

## 🎨 Design System

### Colors
- **Primary Green**: `#14532d` (green-900)
- **Medium Green**: `#15803d` (green-700)
- **Light Green**: `#16a34a` (green-600)
- **Grayscale**: Full gray palette from 50-900
- **Black**: `#000000`
- **White**: `#ffffff`

### Typography
- **Headings**: Bold, black color
- **Body**: Regular weight, gray-700
- **Links**: Green-900 with hover effects

### Shadows
- **custom**: `0 2px 8px rgba(0, 0, 0, 0.1)`
- **custom-md**: `0 4px 12px rgba(0, 0, 0, 0.15)`
- **custom-lg**: `0 8px 24px rgba(0, 0, 0, 0.2)`

## 🔄 Adding New Attacks

To add a new attack type:

1. **Define Attack Data** in `src/data/attacksData.js`:
```javascript
'new-attack': {
  id: 'new-attack',
  name: 'New Attack',
  category: 'Network-Layer',
  description: 'Attack description',
  theory: { description, mechanism, impact },
  keyFeatures: [...],
  mermaidDiagram: '...',
  scenarios: [{ id, name, parameters, ... }],
  safetyConsiderations: [...]
}
```

2. **Add Simulation Logic** in `src/data/simulationEngine.js`:
```javascript
const simulateNewAttack = (scenarioId, params) => {
  // Generate timeline, metrics, explanation
  return { success, timeline, metrics, explanation }
}
```

3. **Route Automatically Created** - The template handles all attacks dynamically!

## 🧪 Simulation Engine

The simulation engine (`simulationEngine.js`) generates realistic attack outputs based on user inputs:

- **Timeline Events**: Sequential messages with timing
- **Metrics**: Attack statistics and measurements
- **Explanations**: Educational interpretation of results
- **Parameter Influence**: Outputs vary based on inputs
- **Random Variations**: Realistic unpredictability

Example simulation result:
```javascript
{
  success: true,
  timeline: [
    { time: 0, message: 'Initializing...', type: 'info' },
    { time: 1000, message: 'Sending packets...', type: 'progress' },
    { time: 2000, message: 'Attack successful', type: 'success' }
  ],
  metrics: {
    packetsSent: 1250,
    successRate: '95%',
    duration: '2.5s'
  },
  explanation: {
    happening: 'Detailed explanation...',
    highlights: ['Key point 1', 'Key point 2'],
    interpretation: 'Overall analysis...'
  }
}
```

## 📝 Parameter Validation

The validator (`parameterValidator.js`) supports:

- **IPv4/IPv6 addresses**
- **Port numbers** (1-65535)
- **URLs** (HTTP/HTTPS)
- **File paths**
- **JSON strings**
- **Email addresses**
- **Hostnames**
- **MAC addresses**
- **Number ranges**

## 🔒 Legal & Safety

**⚠️ IMPORTANT**: This is an educational tool.

- Obtain proper authorization before testing
- Use only in controlled environments
- Follow responsible disclosure practices
- Comply with all applicable laws
- Accept full responsibility for use

Improper use may be illegal and result in criminal charges.

## 🐛 Known Issues

- None currently

## 🚧 Planned Features

- Real backend integration for actual attacks
- User authentication and session management
- Attack history and logging
- Export results to PDF/JSON
- Advanced attack configurations
- Video tutorials and walkthroughs

## 📄 License

Copyright (c) 2025 Montimage. All rights reserved.

This software is proprietary. Unauthorized use is strictly prohibited.

## 📞 Contact

**Montimage**
- Website: https://www.montimage.eu
- Email: contact@montimage.eu
- GitHub: https://github.com/montimage/mmt-attacker
- Issues: https://github.com/montimage/mmt-attacker/issues

## 🙏 Acknowledgments

Built with:
- React - UI framework
- Vite - Build tool
- Tailwind CSS - Styling
- Lucide - Icons
- Mermaid - Diagrams

---

For the complete playbook and CLI tool, see: [MMT-Attacker Main Repository](https://github.com/montimage/mmt-attacker)
