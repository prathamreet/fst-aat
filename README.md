# Student Management System

A Full Stack Web Application built for the **Full Stack Technologies (FST) Mini Project Assessment**. The application provides an interface to manage student enrollment records with complete Create, Read, Update, and Delete (CRUD) capabilities, backed by a Node.js REST API and MongoDB database.

---

## Key Features

- **Full CRUD Operations**:
  - **Create**: Register new students with validation (Roll No, Name, Email, Department, Semester).
  - **Read**: View all registered students in a clean, responsive directory table.
  - **Update**: Edit existing student details via a dedicated modal dialog.
  - **Delete**: Remove student records with confirmation to prevent accidental loss.
- **Search & Filtering**:
  - Live debounced search across student names, roll numbers, and emails.
  - Filter directory by Department / Course.
  - Filter directory by Enrollment Status (*Active*, *Inactive*, *Graduated*).
- **Dashboard Counters**:
  - Real-time statistics showing Total Students, Active Enrolled, and Departments.
- **Human-Centric, Lightweight UI**:
  - Built with semantic HTML5, modern Vanilla CSS, and pure JavaScript (`fetch` API).
  - Zero heavy frontend build chains or framework overhead.
- **Dual Deployment Architecture**:
  - Standard Express server for local development and traditional platforms (Render, Railway, VPS).
  - Pre-configured for **Netlify** using Netlify Serverless Functions (`serverless-http`) and redirects.

---

## Tech Stack

| Component | Technology | Description |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | Clean responsive layout, Fetch API, Modal UX |
| **Backend** | Node.js, Express.js | Modular RESTful API |
| **Database** | MongoDB & Mongoose | Document database with schema validation |
| **Deployment** | Netlify / Render / Local Node | Serverless functions & static assets |

---

## Project Structure

```text
fst-aat/
├── config/
│   └── db.js                 # MongoDB connection handler
├── doc/
│   └── teacher-task.md       # Assessment requirements
├── models/
│   └── Student.js            # Mongoose schema and model
├── netlify/
│   └── functions/
│       └── api.js            # Netlify Serverless function handler
├── public/                   # Static Frontend files
│   ├── css/
│   │   └── style.css         # Styling and design system
│   ├── js/
│   │   └── app.js           # Client-side CRUD and UI logic
│   └── index.html            # Main dashboard interface
├── routes/
│   └── studentRoutes.js      # REST API route handlers
├── .env.example              # Sample environment variables
├── .gitignore                # Git ignore rules
├── netlify.toml              # Netlify build and redirect configuration
├── package.json              # Project dependencies and npm scripts
├── README.md                 # Project documentation
├── seed.js                   # Script to populate sample data
└── server.js                 # Express application entry point
```

---

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/students` | Get all students (supports `?search=`, `?course=`, `?status=`) |
| `GET` | `/api/students/stats` | Get aggregate counts (total, active, courses) |
| `GET` | `/api/students/:id` | Get details of a single student by ID |
| `POST` | `/api/students` | Register a new student |
| `PUT` | `/api/students/:id` | Update an existing student record |
| `DELETE` | `/api/students/:id` | Delete a student record |
| `GET` | `/api/health` | Health check and database status |

---

## Getting Started Locally

### 1. Prerequisites
- [Node.js](https://nodejs.org/) (v16 or higher)
- [MongoDB](https://www.mongodb.com/) (either running locally or a free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster)

### 2. Clone and Install Dependencies
```bash
git clone <your-repository-url>
cd fst-aat
npm install
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your MongoDB connection string:
```env
PORT=5000
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxxx.mongodb.net/student_db?retryWrites=true&w=majority
```
*(If using local MongoDB, use `mongodb://127.0.0.1:27017/student_db`)*

### 4. (Optional) Populate Sample Data
To test the application immediately with realistic sample records:
```bash
npm run seed
```

### 5. Start the Server
For standard run:
```bash
npm start
```
For development with auto-reload:
```bash
npm run dev
```

Open your browser and visit: **`http://localhost:5000`**

---

## Deployment to Netlify

This project is configured out-of-the-box for Netlify using `netlify.toml` and Netlify Serverless Functions.

### Step 1: Push to GitHub
1. Initialize git and commit:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Student Management System"
   ```
2. Create a new repository on [GitHub](https://github.com/new).
3. Push your repository:
   ```bash
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Netlify
1. Log in to [Netlify](https://app.netlify.com).
2. Click **"Add new site"** &rarr; **"Import an existing project"**.
3. Select **GitHub** and choose your repository.
4. Netlify will automatically detect `netlify.toml` with:
   - **Publish directory**: `public`
   - **Functions directory**: `netlify/functions`
5. Under **Environment variables**, click **Add a variable**:
   - **Key**: `MONGODB_URI`
   - **Value**: Your MongoDB Atlas connection URI (e.g. `mongodb+srv://user:pass@cluster0.xxxx.mongodb.net/student_db?retryWrites=true&w=majority`)
   > **Note on MongoDB Atlas**: Ensure your Atlas cluster has Network Access configured to **Allow access from anywhere (`0.0.0.0/0`)** so Netlify serverless functions can connect.
6. Click **Deploy site**.
7. Once deployed, Netlify will provide your live URL (e.g., `https://your-site-name.netlify.app`).

---

## License
This project is submitted for academic assessment under the Full Stack Technologies curriculum.
