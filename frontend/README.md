# Frontend - Dharma FIR Assistant

## Structure

```
frontend/
├── public/
├── src/
│   ├── App.jsx              # Main application
│   ├── FIRForm.jsx          # FIR input form
│   ├── FIRResult.jsx        # Results display
│   ├── LegalSectionCard.jsx # Legal section cards
│   ├── api.js               # API client
│   ├── styles.css           # Global styles
│   └── main.jsx             # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Running Frontend

```powershell
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build
```

## Features

- Real-time FIR analysis
- Entity extraction display
- Collapsible legal section cards
- Loading states and error handling
- Responsive design
