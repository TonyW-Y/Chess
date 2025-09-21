# Chess Engine + FastAPI + React

A full-stack chess application featuring a Python chess engine, FastAPI backend, and React frontend.

## Features

- Complete chess rules implementation
- Real-time game state management
- Move validation and game status tracking
- Responsive web interface
- Deployable to Render

## Local Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn src.server.app:app --reload --port 8000
   ```

The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the web directory:
   ```bash
   cd web
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:5173

## Deployment

This project is configured for deployment on [Render](https://render.com/).

### Prerequisites

- Render account
- Git repository for your project

### Deployment Steps

1. **Push your code** to a Git repository (GitHub, GitLab, or Bitbucket)

2. **Create a new Web Service** on Render:
   - Connect your repository
   - Select the repository
   - Configure the service:
     - Name: `chess-backend`
     - Region: Choose the one closest to you
     - Branch: `main` (or your deployment branch)
     - Runtime: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn src.server.app:app --host 0.0.0.0 --port $PORT`
   - Add environment variables:
     - `PYTHON_VERSION`: `3.9.16`
     - `ENV`: `production`
   - Click "Create Web Service"

3. **Create a Static Site** on Render:
   - Click "New" → "Static Site"
   - Connect your repository
   - Configure the site:
     - Name: `chess-frontend`
     - Branch: `main` (or your deployment branch)
     - Build Command: `cd web && npm install && npm run build`
     - Publish Directory: `web/dist`
   - Add environment variable:
     - `VITE_API_BASE`: `https://chess-backend.onrender.com` (update with your backend URL)
   - Click "Create Static Site"

4. **Update CORS in Backend**:
   - After deployment, update the `ALLOWED_ORIGINS` in `src/server/app.py` to include your frontend URL
   - Redeploy the backend

## API Endpoints

- `GET /` - API status
- `GET /health` - Health check
- `GET /state` - Current game state
- `POST /legal` - Get legal moves for a piece
  - Body: `{ "row": number, "col": number }`
- `POST /move` - Make a move
  - Body: `{ "from_row": number, "from_col": number, "to_row": number, "to_col": number, "promotion": string }`
- `POST /undo` - Undo last move
- `POST /reset` - Reset the game

## Project Structure

```
.
├── src/                    # Python source code
│   ├── engine/            # Chess engine implementation
│   └── server/            # FastAPI application
├── web/                   # Frontend React application
│   ├── public/            # Static assets
│   ├── src/               # React components and logic
│   ├── package.json       # Frontend dependencies
│   └── vite.config.ts     # Vite configuration
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── render.yaml           # Render deployment configuration
└── README.md            # This file
```

## License

This project is open source and available under the [MIT License](LICENSE).
