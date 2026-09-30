const express = require('express');
const router = express.Router();
const Student = require('../models/Student');
const mongoose = require('mongoose');

// Middleware to ensure DB connection is active before queries
const ensureDBConnection = (req, res, next) => {
  if (mongoose.connection.readyState !== 1) {
    return res.status(503).json({
      success: false,
      message: 'MongoDB is not connected yet. Please check MONGODB_URI in your .env file or MongoDB Atlas network access (0.0.0.0/0).'
    });
  }
  next();
};

router.use(ensureDBConnection);

// @route   GET /api/students/stats
// @desc    Get summary statistics
router.get('/stats', async (req, res) => {
  try {
    const totalStudents = await Student.countDocuments();
    const activeStudents = await Student.countDocuments({ status: 'Active' });
    const courses = await Student.distinct('course');

    res.json({
      success: true,
      data: {
        total: totalStudents,
        active: activeStudents,
        totalCourses: courses.length
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

// @route   GET /api/students
// @desc    Get all students with optional search and course filter
router.get('/', async (req, res) => {
  try {
    const { search, course, status } = req.query;
    const query = {};

    if (search && search.trim() !== '') {
      const regex = new RegExp(search.trim(), 'i');
      query.$or = [{ name: regex }, { rollNo: regex }, { email: regex }];
    }

    if (course && course !== 'All') {
      query.course = course;
    }

    if (status && status !== 'All') {
      query.status = status;
    }

    const students = await Student.find(query).sort({ createdAt: -1 });

    res.json({
      success: true,
      count: students.length,
      data: students
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

// @route   GET /api/students/:id
// @desc    Get single student by ID
router.get('/:id', async (req, res) => {
  try {
    const student = await Student.findById(req.params.id);

    if (!student) {
      return res.status(404).json({ success: false, message: 'Student not found' });
    }

    res.json({ success: true, data: student });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Invalid Student ID or server error' });
  }
});

// @route   POST /api/students
// @desc    Add a new student
router.post('/', async (req, res) => {
  try {
    const { name, rollNo, email, course, semester, phone, status } = req.body;

    // Check for existing roll number
    const existingStudent = await Student.findOne({ rollNo: rollNo?.trim().toUpperCase() });
    if (existingStudent) {
      return res.status(400).json({
        success: false,
        message: `Student with Roll Number '${rollNo}' already exists.`
      });
    }

    const student = await Student.create({
      name,
      rollNo,
      email,
      course,
      semester,
      phone,
      status
    });

    res.status(201).json({
      success: true,
      message: 'Student registered successfully',
      data: student
    });
  } catch (error) {
    if (error.name === 'ValidationError') {
      const messages = Object.values(error.errors).map(val => val.message);
      return res.status(400).json({ success: false, message: messages.join(', ') });
    }
    res.status(500).json({ success: false, message: error.message });
  }
});

// @route   PUT /api/students/:id
// @desc    Update a student
router.put('/:id', async (req, res) => {
  try {
    const { name, rollNo, email, course, semester, phone, status } = req.body;

    // Check if roll number is changed and already taken by another student
    if (rollNo) {
      const existingStudent = await Student.findOne({
        rollNo: rollNo.trim().toUpperCase(),
        _id: { $ne: req.params.id }
      });

      if (existingStudent) {
        return res.status(400).json({
          success: false,
          message: `Another student is already registered with Roll Number '${rollNo}'.`
        });
      }
    }

    const student = await Student.findByIdAndUpdate(
      req.params.id,
      {
        name,
        rollNo: rollNo?.trim().toUpperCase(),
        email,
        course,
        semester,
        phone,
        status
      },
      { new: true, runValidators: true }
    );

    if (!student) {
      return res.status(404).json({ success: false, message: 'Student not found' });
    }

    res.json({
      success: true,
      message: 'Student record updated successfully',
      data: student
    });
  } catch (error) {
    if (error.name === 'ValidationError') {
      const messages = Object.values(error.errors).map(val => val.message);
      return res.status(400).json({ success: false, message: messages.join(', ') });
    }
    res.status(500).json({ success: false, message: error.message });
  }
});

// @route   DELETE /api/students/:id
// @desc    Delete a student
router.delete('/:id', async (req, res) => {
  try {
    const student = await Student.findByIdAndDelete(req.params.id);

    if (!student) {
      return res.status(404).json({ success: false, message: 'Student not found' });
    }

    res.json({
      success: true,
      message: 'Student record deleted successfully',
      data: {}
    });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Error deleting student record' });
  }
});

module.exports = router;
