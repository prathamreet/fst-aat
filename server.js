const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const mongoose = require('mongoose');
const connectDB = require('./config/db');
const studentRoutes = require('./routes/studentRoutes');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Connect to MongoDB
connectDB();

// API Routes
app.use('/api/students', studentRoutes);
app.use('/.netlify/functions/api/students', studentRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
    timestamp: new Date().toISOString()
  });
});

// Serve static frontend files
app.use(express.static(path.join(__dirname, 'public')));

// Catch-all to serve frontend index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server if run directly (local development or Node host)
const PORT = process.env.PORT || 5000;
if (process.env.NODE_ENV !== 'test' && !process.env.NETLIFY) {
  app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
  });
}

module.exports = app;
