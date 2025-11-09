# Research Agent Frontend

Modern React frontend for the Research Agent multi-agent research system.

## Setup & Running Instructions

1. Make sure you have Node.js installed (version 16 or higher)

2. Navigate to the frontend directory:
```bash
cd frontend
```

3. Install dependencies:
```bash
npm install
# or if you prefer yarn
yarn install
```

4. Create a `.env` file in the frontend directory with:
```
VITE_API_URL=http://localhost:8000
```

5. Start the development server:
```bash
npm run dev
# or with yarn
yarn dev
```

The application will start on `http://localhost:3000` by default.

6. For production build:
```bash
npm run build
# or
yarn build
```

### Important Notes

- Ensure the backend server is running at `http://localhost:8000` before using the application
- The frontend runs on port 5173 by default. If this port is in use, Vite will automatically use the next available port
- Use modern browsers (Chrome, Firefox, Safari, Edge) for best experience

### Troubleshooting

If you encounter issues:

1. Make sure all dependencies are installed correctly:
```bash
rm -rf node_modules
npm install
```

2. Clear browser cache and reload
3. Verify the backend is running and accessible
4. Check console for any error messages

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
