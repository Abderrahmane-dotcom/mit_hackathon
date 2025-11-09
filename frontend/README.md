# Research Agent Frontend

Modern React frontend for the Research Agent multi-agent research system.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Ensure backend is running at `http://localhost:8000`

## Features

- **Home**: Introduction and system status
- **Upload**: Configure research topic and data sources
- **Dashboard**: Real-time agent collaboration visualization
- **Report**: Comprehensive research insights with citations

## Tech Stack

- React 18 + TypeScript
- Vite for fast builds
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls
- Radix UI for accessible components

## API Integration

The frontend connects to the backend API at `http://localhost:8000` with endpoints:
- `GET /health` - Health check
- `POST /research` - Start research
- `POST /reinitialize` - Reload system
- `GET /config` - Get configuration

## Color Palette

Based on Research Agent logo:
- Primary: Navy Blue (#0B1E3D)
- Accent: Cyan (#00D9D9)
- Background: White/Light Gray
