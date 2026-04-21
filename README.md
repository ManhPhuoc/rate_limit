Rate Limit Manager
A comprehensive rate limiting system with an interactive web interface for managing and testing API request throttling strategies.

## 1. Problem Description
Modern APIs need protection against excessive requests that could overload servers or drain resources. This project implements a Rate Limiting Manager that:

- Controls API traffic by limiting the number of requests per time window.
- Supports multiple strategies:
  - Sliding Window: Precise request tracking within a time window (no burst allowed).
  - Token Bucket: Flexible approach with token refill rate (allows burst traffic).
- Provides configuration interface to dynamically set rate limit rules.
- Enables request validation to check if incoming requests are allowed.
- Stores state persistently using Redis for distributed systems.

Real-world use cases:
- Protect public APIs from abuse.
- Enforce fair usage policies.
- Prevent DDoS attacks.
- Control resource consumption.

## 2. Features

### Core Functionality
- **Dynamic Rate Limiting Configuration**
  - Set custom limit, time window, and strategy per API key
  - Real-time configuration updates
  - Support for multiple rate limiting strategies

- **Two Proven Rate Limiting Strategies**
  - **Sliding Window**: Strict rate limiting with precise request tracking
  - **Token Bucket**: Flexible approach with token refill for handling bursts

- **Request Validation**
  - Check if an incoming request is allowed
  - Get remaining quota information
  - Real-time request processing

- **Interactive Web Interface**
  - User-friendly forms for configuration
  - Request history and statistics tracking
  - Live testing of rate limiting behavior
  - Response time metrics

- **Persistent Storage**
  - Redis-backed state management
  - Distributed system ready
  - High-performance data access

## 3. How to Run

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+ (for backend)
- Redis server running locally or remotely

### 3.1. Frontend Setup (Next.js)
Navigate to the UI directory:
```bash
cd rate-limit-ui
```

Install dependencies:
```bash
npm install
# or
pnpm install
```

Start the development server:
```bash
npm run dev
# or (using pnpm - recommended for faster performance)
pnpm dev
```

Open in browser:
```
http://localhost:3000
```

### 3.2. Backend Setup (FastAPI)
Navigate to the API directory:
cd rate-limit-api

Install dependencies:
pip install -r requirements.txt

Start the API server:
python main.py

The API will run on http://localhost:8000

### 3.3. Verify Everything Works
1. Go to http://localhost:3000
2. Fill in Send Configuration form:
   - API Key: test-key
   - Limit: 5 requests
   - Window: 10 seconds
   - Strategy: Sliding Window
   - Click "Send Configuration"
3. Use Check Request to test:
   - Enter the same API Key
   - Click "Check" multiple times to see throttling in action.

## 4. Technologies Used

### Frontend
- Next.js 16: React framework with SSR & static generation.
- React 19: UI component library.
- TypeScript: Type-safe JavaScript.
- Tailwind CSS 4: Utility-first CSS framework.
- Fetch API: Client-side HTTP requests.

### Backend
- FastAPI: High-performance Python web framework.
- Redis: In-memory data store for rate limit state.
- Python 3.8+: Programming language.

### Architecture
- State Storage: Redis - Persists rate limit counters & token buckets.
- API Communication: REST + JSON - Frontend-Backend interaction.
- Rate Limit Strategies: Python - Sliding Window & Token Bucket algorithms.

## 5. Project Structure
```text
rate-limit/
├── rate-limit-ui/              # Next.js Frontend
│   ├── app/                   # App Router (Next.js)
│   │   ├── page.tsx           # Main page
│   │   └── layout.tsx         # Root layout
│   │
│   ├── components/            # UI Components
│   │   ├── config-form.tsx    # Configuration form
│   │   └── check-form.tsx     # Request check form
│   │
│   ├── lib/                   # API layer
│   │   └── api.ts             # API client functions
│   │
│   └── package.json
│
└── rate-limit-api/            # FastAPI Backend
    ├── main.py                # Entry point (FastAPI app)
    ├── database.py            # Redis connection setup
    │
    ├── middlewares/
    │   └── rate_limit.py      # Rate limiting middleware
    │
    ├── services/
    │   └── rate_limiter.py    # Core rate limit logic
    │
    ├── strategies/            # Rate limit algorithms
    │   ├── sliding_window.py  # Sliding Window strategy
    │   └── token_bucket.py    # Token Bucket strategy
    │
    └── requirements.txt

## 6. How It Works

### Configuration Flow
1. User fills rate limit settings (limit, window, strategy).
2. Frontend sends POST request to /config endpoint.
3. Backend stores configuration in Redis.
4. Response returned to frontend.

### Check Request Flow
1. User provides API Key.
2. Frontend sends POST request to /check endpoint with API Key.
3. Backend retrieves rate limit config from Redis.
4. Executes appropriate strategy (Sliding Window or Token Bucket).
5. Returns whether request is allowed + remaining quota.

## 7. Algorithm Comparison

### Sliding Window
Advantage: Precise, never allows burst beyond limit.

Disadvantage: Higher memory usage as it stores all request timestamps.

Best for: Strict rate limiting requirements.

### Token Bucket
Advantage: Efficient memory usage (stores only 2 values), allows short bursts.

Disadvantage: Slightly looser control in very short periods.

Best for: Services that need to handle traffic spikes like streaming or downloads.

## 8. API Routes

### Backend API Endpoints

#### 1. POST `/config` - Send Configuration
Configure rate limit settings for an API key

**Request Body:**
```json
{
  "api_key": "test-key",
  "limit": 5,
  "window": 60,
  "strategy": "sliding_window"
}
```

**Parameters:**
- `api_key` (string): Unique identifier for the API key
- `limit` (integer): Maximum requests allowed
- `window` (integer): Time window in seconds
- `strategy` (string): Rate limiting strategy - `sliding_window` or `token_bucket`

**Response (Success 200):**
```json
{
  "message": "Configuration saved successfully",
  "status": "ok"
}
```

**Response (Error 400):**
```json
{
  "error": "Invalid configuration",
  "detail": "Limit must be greater than 0"
}
```

---

#### 2. POST `/check` - Check Request Limit
Check if a request from an API key is allowed

**Request Headers:**
- `x-api-key`: The API key to check

**Response (Success 200 - Request Allowed):**
```json
{
  "data": {
    "allow": true,
    "remaining": 4,
    "reset_at": 1713686400
  },
  "status": "ok"
}
```

**Response (Success 200 - Request Blocked):**
```json
{
  "data": {
    "allow": false,
    "remaining": 0,
    "reset_at": 1713686400
  },
  "status": "ok"
}
```

**Response (Error 404):**
```json
{
  "error": "Configuration not found",
  "detail": "No configuration found for the provided API key"
}
```

---

## 9. Database Schema (Redis)

### Redis Data Structures

#### Configuration Storage
```
Key: rate_limit:config:{api_key}
Type: Hash
Fields:
  - limit: Number of allowed requests
  - window: Time window in seconds
  - strategy: "sliding_window" or "token_bucket"

Example:
Key: rate_limit:config:test-key
Value: {
  "limit": 5,
  "window": 60,
  "strategy": "sliding_window"
}
```

#### Sliding Window Storage
```
Key: rate_limit:sliding:{api_key}
Type: Sorted Set
Members: Request timestamps (score = timestamp, member = timestamp as string)

Example:
Key: rate_limit:sliding:test-key
Members: [1713686100, 1713686105, 1713686110, 1713686115, 1713686120]
```

#### Token Bucket Storage
```
Key: rate_limit:bucket:{api_key}
Type: Hash
Fields:
  - tokens: Current number of tokens available
  - last_refill: Timestamp of last refill

Example:
Key: rate_limit:bucket:test-key
Value: {
  "tokens": 4.5,
  "last_refill": 1713686100
}
```

---

## 10. Scripts and Available Commands

### Frontend (Next.js)

**Development**
```bash
npm run dev
# or
pnpm dev
```
- Starts Next.js development server on `http://localhost:3000`
- Enables hot reload on file changes
- Shows console logs in terminal
- Supports both npm and pnpm package managers

**Build**
```bash
npm run build
# or
pnpm build
```
- Creates optimized production build
- Outputs to `.next` folder
- Performs code splitting and minification

**Production**
```bash
npm start
# or
pnpm start
```
- Starts production server using built files
- Requires `npm run build` or `pnpm build` first
- Optimized for performance

**Lint**
```bash
npm run lint
# or
pnpm lint
```
- Runs ESLint to check code quality
- Identifies code style issues
- Suggests improvements

### Backend (FastAPI + Python)

**Install Dependencies**
```bash
pip install -r requirements.txt
```
- Installs all Python packages (FastAPI, Redis, etc.)
- Creates isolated environment

**Run Development Server**
```bash
python main.py
```
- Starts FastAPI development server on `http://localhost:8000`
- Auto-reloads on file changes
- Shows request logs in terminal

**Install Redis**
```bash
# Windows (using WSL or Docker recommended)
wsl
sudo apt-get install redis-server

# macOS
brew install redis

# Linux
sudo apt-get install redis-server
```

**Start Redis Server**
```bash
redis-server
```
- Starts Redis in-memory database on default port 6379
- Required for rate limit storage

### Full Stack Startup (Recommended)

1. **Terminal 1 - Redis**
```bash
redis-server
```

2. **Terminal 2 - Backend (FastAPI)**
```bash
cd rate-limit-api
python main.py
```

3. **Terminal 3 - Frontend (Next.js)**
```bash
cd rate-limit-ui
pnpm dev
# or npm run dev
```

Then open `http://localhost:3000` in browser.

---

