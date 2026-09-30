/**
 * Seed script to populate initial sample student records
 * Run with: npm run seed
 */

require('dotenv').config();
const mongoose = require('mongoose');
const dns = require('dns');
const Student = require('./models/Student');

try {
  dns.setServers(['8.8.8.8', '1.1.1.1', '8.8.4.4']);
} catch (e) {}

const sampleStudents = [
  {
    name: 'Aarav Sharma',
    rollNo: 'CS202601',
    email: 'aarav.sharma@college.edu',
    phone: '+91 9876543210',
    course: 'Computer Science & Engineering',
    semester: 'Semester 6',
    status: 'Active'
  },
  {
    name: 'Priya Patel',
    rollNo: 'CS202602',
    email: 'priya.patel@college.edu',
    phone: '+91 9876543211',
    course: 'Computer Science & Engineering',
    semester: 'Semester 6',
    status: 'Active'
  },
  {
    name: 'Rohan Verma',
    rollNo: 'IT202615',
    email: 'rohan.verma@college.edu',
    phone: '+91 9876543212',
    course: 'Information Technology',
    semester: 'Semester 4',
    status: 'Active'
  },
  {
    name: 'Ananya Iyer',
    rollNo: 'EC202608',
    email: 'ananya.iyer@college.edu',
    phone: '+91 9876543213',
    course: 'Electronics & Communication',
    semester: 'Semester 8',
    status: 'Graduated'
  },
  {
    name: 'Devendra Singh',
    rollNo: 'ME202621',
    email: 'devendra.s@college.edu',
    phone: '+91 9876543214',
    course: 'Mechanical Engineering',
    semester: 'Semester 2',
    status: 'Inactive'
  },
  {
    name: 'Sneha Kulkarni',
    rollNo: 'BA202605',
    email: 'sneha.k@college.edu',
    phone: '+91 9876543215',
    course: 'Business Administration',
    semester: 'Semester 4',
    status: 'Active'
  }
];

async function seedData() {
  const uri = process.env.MONGODB_URI;

  if (!uri) {
    console.error('Error: MONGODB_URI is not defined in .env');
    process.exit(1);
  }

  try {
    console.log('Connecting to MongoDB...');
    await mongoose.connect(uri);
    console.log('Connected.');

    console.log('Clearing existing student records...');
    await Student.deleteMany({});

    console.log('Inserting sample student records...');
    await Student.insertMany(sampleStudents);

    console.log(`Successfully seeded ${sampleStudents.length} student records!`);
    process.exit(0);
  } catch (error) {
    console.error('Seeding failed:', error);
    process.exit(1);
  }
}

seedData();
