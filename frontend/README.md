# Frontend - Housing Intelligence Platform

React frontend for the Housing Intelligence Platform with Tailwind CSS.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env if needed (default should work with local backend)
```

3. Run development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Chat/          # Chat interface components
│   │   ├── Properties/    # Property display components
│   │   └── common/        # Shared components
│   ├── pages/             # Page components
│   ├── services/          # API services
│   ├── hooks/             # Custom React hooks
│   ├── utils/             # Utility functions
│   ├── App.jsx           # Main app component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles + Tailwind
├── public/               # Static assets
└── package.json         # Dependencies
```

## Design System

- **Colors**: Port Gore (dark), Marlin (blue), Primary (blue-gray), Rajah (peach accent)
- **Font**: Raleway (Regular 400, Semibold 600)
- **Animations**: Fade-in, slide-in (left/right), slide-up
- **Framework**: Tailwind CSS with custom configuration

## Features

- Interactive chat interface with typing indicator
- Animated message bubbles
- Property cards with image galleries
- Responsive design (mobile-first)
- Landing page with sliding images
