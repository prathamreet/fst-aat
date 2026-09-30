const mongoose = require('mongoose');

const studentSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Student name is required'],
      trim: true,
      minlength: [2, 'Name must be at least 2 characters long'],
      maxlength: [100, 'Name cannot exceed 100 characters']
    },
    rollNo: {
      type: String,
      required: [true, 'Roll number is required'],
      unique: true,
      trim: true,
      uppercase: true
    },
    email: {
      type: String,
      required: [true, 'Email address is required'],
      trim: true,
      lowercase: true,
      match: [/^\S+@\S+\.\S+$/, 'Please provide a valid email address']
    },
    course: {
      type: String,
      required: [true, 'Course is required'],
      trim: true
    },
    semester: {
      type: String,
      required: [true, 'Semester is required'],
      default: 'Semester 1'
    },
    phone: {
      type: String,
      trim: true,
      default: ''
    },
    status: {
      type: String,
      enum: ['Active', 'Inactive', 'Graduated'],
      default: 'Active'
    }
  },
  {
    timestamps: true
  }
);

// Helpful index for fast searching by name or roll number
studentSchema.index({ name: 'text', rollNo: 'text' });

module.exports = mongoose.model('Student', studentSchema);
