# LLM Query App - Frontend Service

React-based frontend application for querying LLM with authentication.

## Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)
- Backend API running (see backend repository)

## Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd llm-query-app
```

2. Install dependencies
```bash
npm install
```

3. Configure the API URL
Edit `src/App.js` and update the API_BASE_URL:
```javascript
const API_BASE_URL = 'http://your-backend-url:8000/api/v1';
```

## Running the Application

Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Building for Production

Create an optimized production build:
```bash
npm run build
```

The build files will be in the `build/` folder.

## Features

- User registration and authentication
- Submit queries to LLM
- View query history
- Check daily usage statistics
- JWT token-based authentication

