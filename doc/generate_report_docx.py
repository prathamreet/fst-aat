import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Document Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("Academic Project Report: Student Management System - Full-Stack Academic Record & Enrollment Portal")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    p_title.paragraph_format.space_after = Pt(14)

    # Metadata Table (Table 0)
    meta_data = [
        ("Student Name", "Prathamreet Singh"),
        ("USN", "1NH23CS191"),
        ("Semester / Section", "5th / 7th Semester - CSE"),
        ("Subject", "Full Stack Technologies"),
        ("AAT-1 Title", "Portfolio-Driven Assessment (Student Management System)"),
        ("Project Title", "Student Management System - Mini Full-Stack Academic Record & Enrollment Portal"),
        ("GitHub Repository Link", "https://github.com/prathamreet/fst-aat"),
        ("Live Production Link", "https://fst-aat-prathamreet-1nh23cs191.netlify.app/")
    ]
    
    table0 = doc.add_table(rows=len(meta_data), cols=2)
    table0.alignment = WD_TABLE_ALIGNMENT.CENTER
    table0.style = 'Table Grid'
    
    for i, (k, v) in enumerate(meta_data):
        row = table0.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        
        set_cell_background(c0, "F1F5F9")
        set_cell_margins(c0, 100, 100, 140, 140)
        set_cell_margins(c1, 100, 100, 140, 140)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = RGBColor(30, 41, 59)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_code(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(text)
        r.font.name = 'Consolas'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_image_with_caption(image_path, width, caption_text):
        if os.path.exists(image_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            run = p_img.add_run()
            run.add_picture(image_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(14)
            r_cap = p_cap.add_run(caption_text)
            r_cap.italic = True
            r_cap.bold = True
            r_cap.font.size = Pt(9)
            r_cap.font.color.rgb = RGBColor(71, 85, 105)
        else:
            add_body(f"[Image file not found: {image_path}]")

    # 1. Project Title
    add_h1("1. Project Title")
    add_body("Student Management System: Mini Full-Stack Academic Record & Enrollment Portal")
    add_body("Tagline: A centralized, high-performance academic record management portal enabling educational institutions to enroll students, track departmental records, and execute full-lifecycle CRUD operations through an asynchronous RESTful web architecture.")

    # 2. Problem Statement and Objectives
    add_h1("2. Problem Statement and Objectives")
    add_h2("Problem Statement")
    add_body("Academic institutions and departments frequently grapple with fragmented student record management systems. Traditional spreadsheet trackers and legacy desktop software lack real-time synchronization, fail to prevent duplicate enrollments, suffer from high administrative overhead, and do not provide clean, web-accessible RESTful interfaces for cross-platform integration.")
    add_body("The Student Management System solves these administrative bottlenecks by providing a responsive, lightweight, and cloud-integrated web portal. It unifies student registrations, departmental classifications, real-time search, enrollment tracking, and record modifications into a single cohesive full-stack application backed by MongoDB Atlas cloud persistence and Netlify Serverless execution.")

    add_h2("Objectives Matrix")
    obj_data = [
        ("Academic Requirement / Objective", "Scope & Implementation in Student Management System", "Status"),
        ("Topic Focus", "Student Management System (Academic Records & Departmental Directory)", "Complete"),
        ("Frontend Architecture", "Semantic HTML5, Vanilla CSS3 with custom design system, and Vanilla JavaScript Fetch API (zero framework bloat)", "Complete"),
        ("Backend Infrastructure", "Node.js and Express.js RESTful API with modular route controllers, validation, and CORS handling", "Complete"),
        ("Database System", "MongoDB persistence via Mongoose schemas (Student model with unique constraints and indexing)", "Complete"),
        ("System Resiliency", "Cached connection pooling for serverless execution and public DNS resolver fallback (8.8.8.8) for reliable SRV resolution", "Complete"),
        ("CRUD Operations", "Comprehensive Create, Read, Update, Delete workflows implemented across UI modals and RESTful endpoints", "Complete"),
        ("Version Control", "Structured Git commit history, semantic tags, and cloud deployment on GitHub and Netlify", "Complete")
    ]
    t1 = doc.add_table(rows=len(obj_data), cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.style = 'Table Grid'
    for r_idx, row in enumerate(obj_data):
        for c_idx, val in enumerate(row):
            cell = t1.rows[r_idx].cells[c_idx]
            if r_idx == 0:
                set_cell_background(cell, "1E293B")
                p = cell.paragraphs[0]
                r = p.add_run(val)
                r.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                p = cell.paragraphs[0]
                r = p.add_run(val)
                r.font.size = Pt(9)
                if c_idx == 2:
                    r.bold = True
                    r.font.color.rgb = RGBColor(16, 185, 129)
                else:
                    r.font.color.rgb = RGBColor(30, 41, 59)
            set_cell_margins(cell, 80, 80, 100, 100)

    # 3. Technologies / Tools Used
    add_h1("3. Technologies / Tools Used")
    add_h2("Core Technology Stack")
    add_body("• Frontend Runtime & Structure: Semantic HTML5, Vanilla JavaScript (ES6+ Asynchronous Fetch API, DOM Controller)")
    add_body("• Styling & Design System: Vanilla CSS3 utilizing custom variables (--primary, --border-light, --radius-md), Inter typography, and responsive media queries")
    add_body("• Backend Runtime & Server: Node.js (v26.3.0), Express.js Framework (v4.21.2)")
    add_body("• Middleware & Security: CORS (Cross-Origin Resource Sharing), Express JSON body parser, Dotenv (environment configuration)")
    add_body("• Database & ODM: MongoDB Atlas (Cloud NoSQL Database), Mongoose ODM (v8.9.5)")
    add_body("• Resiliency & Serverless: Serverless-HTTP (v3.2.0), Node.js DNS resolver configuration (Google DNS 8.8.8.8 fallback)")
    add_body("• Cloud Hosting & Deployment: Netlify (Global CDN static hosting + AWS Lambda Serverless Functions)")
    add_body("• Version Control: Git, GitHub Architecture (https://github.com/prathamreet/fst-aat)")

    add_h2("Repository Language Distribution Statistics")
    add_body("• JavaScript (Backend Routes, Controllers, Config, & Frontend DOM): 52.8%")
    add_body("• CSS (Custom Design Tokens, Modal Systems, Grid Layouts): 30.1%")
    add_body("• HTML (Dashboard Structure & Semantic Modals): 17.1%")

    # 4. Project Description
    add_h1("4. Project Description")
    add_body("The Student Management System operates as an asynchronous, single-page web portal designed for educational administrators. Upon loading, the client establishes an asynchronous handshake with the Express REST API (or Netlify serverless function) to retrieve live aggregate metrics and the student directory.")
    add_body("Administrators can register new students via a modal dialog that validates fields and prevents duplicate roll numbers. The interface allows instant searching across student names, roll numbers, and emails with client-side debouncing, and enables filtering by academic department and enrollment status. Records can be updated or deleted with two-step safety confirmations.")

    # High-Quality Styled Visual Architecture Table Diagram
    add_h2("System Architecture & Data Flow Diagram")
    
    arch_table = doc.add_table(rows=3, cols=3)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_table.style = 'Table Grid'
    
    # Column widths: 2.7 in, 1.1 in, 2.7 in
    col_widths = [Inches(2.7), Inches(1.1), Inches(2.7)]

    # Row 0: Client Layer <---> API Serverless Layer
    r0 = arch_table.rows[0]
    for c_i, w in enumerate(col_widths):
        r0.cells[c_i].width = w
        set_cell_margins(r0.cells[c_i], 100, 100, 120, 120)

    # Box 1: Client
    set_cell_background(r0.cells[0], "EFF6FF")
    p00 = r0.cells[0].paragraphs[0]
    rn00 = p00.add_run("CLIENT LAYER (BROWSER)\n")
    rn00.bold = True
    rn00.font.size = Pt(9.5)
    rn00.font.color.rgb = RGBColor(30, 58, 138)
    p00_sub = r0.cells[0].add_paragraph()
    p00_sub.paragraph_format.line_spacing = 1.1
    p00_sub.add_run("• Semantic HTML5 & Modern CSS3\n• Vanilla JavaScript (app.js)\n• Asynchronous Fetch API & DOM").font.size = Pt(8.5)

    # Box 2: Middle Protocol Arrow
    set_cell_background(r0.cells[1], "F8FAFC")
    p01 = r0.cells[1].paragraphs[0]
    p01.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p01.paragraph_format.space_before = Pt(8)
    rn01 = p01.add_run("◄══════►\n")
    rn01.bold = True
    rn01.font.size = Pt(10)
    rn01.font.color.rgb = RGBColor(37, 99, 235)
    p01_sub = r0.cells[1].add_paragraph()
    p01_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p01_sub.add_run("HTTP / HTTPS\nREST API\n(JSON Payloads)").font.size = Pt(7.5)

    # Box 3: Serverless Backend
    set_cell_background(r0.cells[2], "F1F5F9")
    p02 = r0.cells[2].paragraphs[0]
    rn02 = p02.add_run("BACKEND / SERVERLESS LAYER\n")
    rn02.bold = True
    rn02.font.size = Pt(9.5)
    rn02.font.color.rgb = RGBColor(15, 23, 42)
    p02_sub = r0.cells[2].add_paragraph()
    p02_sub.paragraph_format.line_spacing = 1.1
    p02_sub.add_run("• Node.js & Express.js Router\n• Netlify Serverless (AWS Lambda)\n• Input Validation & CORS Handler").font.size = Pt(8.5)

    # Row 1: Flow Arrows
    r1 = arch_table.rows[1]
    for c_i, w in enumerate(col_widths):
        r1.cells[c_i].width = w
        set_cell_margins(r1.cells[c_i], 40, 40, 100, 100)

    p10 = r1.cells[0].paragraphs[0]
    p10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r10 = p10.add_run("▼  Dynamic DOM / Modal Events")
    r10.font.size = Pt(8)
    r10.font.color.rgb = RGBColor(100, 116, 139)

    p11 = r1.cells[1].paragraphs[0] # empty

    p12 = r1.cells[2].paragraphs[0]
    p12.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r12 = p12.add_run("▼  Mongoose ODM Connection Pool")
    r12.font.size = Pt(8)
    r12.font.color.rgb = RGBColor(100, 116, 139)

    # Row 2: Client Components <---> Database Persistence
    r2 = arch_table.rows[2]
    for c_i, w in enumerate(col_widths):
        r2.cells[c_i].width = w
        set_cell_margins(r2.cells[c_i], 100, 100, 120, 120)

    # Box 4: Interactive Client Features
    set_cell_background(r2.cells[0], "F8FAFC")
    p20 = r2.cells[0].paragraphs[0]
    rn20 = p20.add_run("INTERACTIVE UI CONTROLS\n")
    rn20.bold = True
    rn20.font.size = Pt(9.5)
    rn20.font.color.rgb = RGBColor(30, 41, 59)
    p20_sub = r2.cells[0].add_paragraph()
    p20_sub.paragraph_format.line_spacing = 1.1
    p20_sub.add_run("• Real-time Debounced Search\n• Department & Status Filters\n• KPI Metric Counters & Toasts").font.size = Pt(8.5)

    # Box 5: Middle blank
    set_cell_background(r2.cells[1], "FFFFFF")

    # Box 6: Database Persistence Layer
    set_cell_background(r2.cells[2], "ECFDF5")
    p22 = r2.cells[2].paragraphs[0]
    rn22 = p22.add_run("MONGODB ATLAS CLOUD DB\n")
    rn22.bold = True
    rn22.font.size = Pt(9.5)
    rn22.font.color.rgb = RGBColor(6, 95, 70)
    p22_sub = r2.cells[2].add_paragraph()
    p22_sub.paragraph_format.line_spacing = 1.1
    p22_sub.add_run("• Database: student_db (students)\n• Unique Roll Index & Validation\n• Cached Pool & Public DNS Fallback").font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("End-to-End CRUD Operations Matrix")
    crud_data = [
        ("Entity", "Create (POST)", "Read (GET)", "Update (PUT / PATCH)", "Delete (DELETE)"),
        ("Student Records", 
         "Register new student (POST /api/students) with roll number uniqueness check via interactive modal",
         "Query directory with filters (GET /api/students?search=...&course=...); Fetch student profile by ID (GET /api/students/:id)",
         "Modify student details (PUT /api/students/:id) with server-side validation and duplicate prevention",
         "Permanently remove student record (DELETE /api/students/:id) with confirmation modal dialog"),
        ("Academic KPI Metrics",
         "Dynamic recalculation upon record creation",
         "Retrieve aggregate metrics (GET /api/students/stats) for dashboard counters (Total, Active, Departments)",
         "Automatic stat counter synchronization upon record updates or status alterations",
         "Immediate metric decrement upon record deletion"),
        ("Departmental Enrollment",
         "Enroll student into specific department and semester on creation",
         "Filter directory listing by department (GET /api/students?course=Computer+Science)",
         "Reassign department or advance semester via PUT /api/students/:id",
         "De-enroll student from department roster upon record removal")
    ]
    t2 = doc.add_table(rows=len(crud_data), cols=5)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.style = 'Table Grid'
    for r_idx, row in enumerate(crud_data):
        for c_idx, val in enumerate(row):
            cell = t2.rows[r_idx].cells[c_idx]
            if r_idx == 0:
                set_cell_background(cell, "1E293B")
                p = cell.paragraphs[0]
                r = p.add_run(val)
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                p = cell.paragraphs[0]
                r = p.add_run(val)
                r.font.size = Pt(8.5)
                r.font.color.rgb = RGBColor(30, 41, 59)
            set_cell_margins(cell, 80, 80, 100, 100)

    # 5. Implementation / Methodology
    add_h1("5. Implementation / Methodology")
    add_h2("Codebase Directory Structure")
    add_code("""fst-aat/
├── config/
│   └── db.js                 # MongoDB Atlas connection handler & DNS failover logic
├── doc/
│   ├── teacher-task.md       # Teacher assessment guidelines
│   ├── screenshot/           # Production application interface screenshots
│   │   ├── dash.png          # Live dashboard & student directory view
│   │   └── form.png          # Student registration modal dialog view
│   ├── Student_Management_System_Project_Report.docx # Formatted academic report
│   └── Student_Management_System_Project_Report.md   # Markdown project report
├── models/
│   └── Student.js            # Mongoose Data Schema & Model constraints
├── netlify/
│   └── functions/
│       └── api.js            # Serverless-HTTP Lambda wrapper for Netlify deployment
├── public/                   # Static Frontend client
│   ├── css/
│   │   └── style.css         # Clean custom CSS design system & responsive styling
│   ├── js/
│   │   └── app.js           # Client-side controller (Fetch API, DOM events, modals)
│   └── index.html            # Main administrative dashboard
├── routes/
│   └── studentRoutes.js      # Express REST API endpoints & CRUD controllers
├── .env                      # Local environment variables (MONGODB_URI, PORT)
├── .env.example              # Configuration template for deployment
├── .gitignore                # Protects secrets and node_modules from version control
├── netlify.toml              # Netlify build configuration & serverless rewrite rules
├── package.json              # Project dependencies & execution scripts
├── README.md                 # Complete academic documentation & submission report
├── seed.js                   # Automated database seeder with sample student records
└── server.js                 # Express server entry point for local and traditional hosting""")

    add_h2("Serverless Dual-Mode Resiliency & DNS Fallback Mechanism")
    add_body("To guarantee uninterrupted execution across local development and Netlify serverless functions, the application implements two architectural safeguards:")
    add_body("1. Serverless Connection Caching: In config/db.js, the MongoDB connection state is cached across AWS Lambda invocations. When Netlify executes the function, it reuses the established Mongoose connection pool rather than opening redundant connections, eliminating connection latency and avoiding connection spikes.")
    add_body("2. Fallback DNS Resolver Configuration: On Windows developer environments and restrictive ISP networks, MongoDB Atlas SRV connection strings (mongodb+srv://) frequently trigger 'querySrv ECONNREFUSED' due to misconfigured local DNS servers. The application programmatically configures Google Public DNS (8.8.8.8, 8.8.4.4) and Cloudflare DNS (1.1.1.1) in config/db.js and seed.js, ensuring robust SRV lookup across all host operating systems.")

    add_h2("Standardized REST API Response Contract")
    add_body("All backend HTTP endpoints adhere to a standardized JSON envelope:")
    add_code("""{
  "success": true,
  "count": 6,
  "data": [...],
  "message": "Operation completed successfully."
}""")

    add_h2("Local Development & Testing Setup")
    add_body("• Install Dependencies: npm install")
    add_body("• Configure Environment: Set MONGODB_URI in .env")
    add_body("• Seed Sample Data: npm run seed")
    add_body("• Launch Server: npm start (or npm run dev)")
    add_body("• Access Dashboard: http://localhost:5000")
    add_body("• Health Check Endpoint: http://localhost:5000/api/health")

    # 6. Important Code Snippets
    add_h1("6. Important Code Snippets")
    add_h2("1. Mongoose Data Schema (models/Student.js)")
    add_code("""const mongoose = require('mongoose');

const studentSchema = new mongoose.Schema({
  name: { type: String, required: [true, 'Student name is required'], trim: true },
  rollNo: { type: String, required: [true, 'Roll number is required'], unique: true, trim: true, uppercase: true },
  email: { type: String, required: [true, 'Email is required'], trim: true, lowercase: true },
  course: { type: String, required: [true, 'Course is required'], trim: true },
  semester: { type: String, required: [true, 'Semester is required'], default: 'Semester 1' },
  phone: { type: String, trim: true, default: '' },
  status: { type: String, enum: ['Active', 'Inactive', 'Graduated'], default: 'Active' }
}, { timestamps: true });

studentSchema.index({ name: 'text', rollNo: 'text' });
module.exports = mongoose.model('Student', studentSchema);""")

    add_h2("2. Database Connection Handler with DNS Fallback (config/db.js)")
    add_code("""const mongoose = require('mongoose');
const dns = require('dns');

// Configure fallback DNS servers for reliable SRV resolution on Windows
try {
  dns.setServers(['8.8.8.8', '1.1.1.1', '8.8.4.4']);
} catch (e) {}

let isConnected = false;
const connectDB = async () => {
  if (isConnected || mongoose.connection.readyState >= 1) return;
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI, { serverSelectionTimeoutMS: 5000 });
    isConnected = true;
    console.log(`MongoDB Connected: ${conn.connection.host}`);
  } catch (error) {
    console.warn(`MongoDB Connection Warning: ${error.message}`);
  }
};
module.exports = connectDB;""")

    add_h2("3. Express REST API CRUD Routes (routes/studentRoutes.js)")
    add_code("""// GET /api/students - List all students with search and filtering
router.get('/', async (req, res) => {
  try {
    const { search, course, status } = req.query;
    const query = {};
    if (search) {
      const regex = new RegExp(search.trim(), 'i');
      query.$or = [{ name: regex }, { rollNo: regex }, { email: regex }];
    }
    if (course && course !== 'All') query.course = course;
    if (status && status !== 'All') query.status = status;

    const students = await Student.find(query).sort({ createdAt: -1 });
    res.json({ success: true, count: students.length, data: students });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

// POST /api/students - Create new student with duplicate prevention
router.post('/', async (req, res) => {
  try {
    const { name, rollNo, email, course, semester, phone, status } = req.body;
    const exists = await Student.findOne({ rollNo: rollNo?.trim().toUpperCase() });
    if (exists) {
      return res.status(400).json({ success: false, message: `Roll Number '${rollNo}' already registered.` });
    }
    const student = await Student.create({ name, rollNo, email, course, semester, phone, status });
    res.status(201).json({ success: true, message: 'Student registered successfully', data: student });
  } catch (error) {
    res.status(400).json({ success: false, message: error.message });
  }
});""")

    add_h2("4. Netlify Serverless Function Handler (netlify/functions/api.js)")
    add_code("""const serverless = require('serverless-http');
const connectDB = require('../../config/db');
const app = require('../../server');

const serverlessHandler = serverless(app);

module.exports.handler = async (event, context) => {
  context.callbackWaitsForEmptyEventLoop = false;
  await connectDB();
  return await serverlessHandler(event, context);
};""")

    # 7. Output Screenshots
    add_h1("7. Output Screenshots")
    add_body("The deployed Student Management System interface encompasses five primary operational views. The figures below document the production deployment on Netlify backed by MongoDB Atlas:")

    add_h2("View 1: Administrative Dashboard & Student Directory (Read Operation & KPI Analytics)")
    add_body("Description: Primary dashboard view showing real-time aggregate KPI metrics (Total Students: 6, Active Enrolled: 4, Departments: 5), the student directory table with roll number badges, contact information, department badges, and action buttons.")
    add_image_with_caption('doc/screenshot/dash.png', Inches(6.2), "Figure 1: Production Student Management Dashboard displaying real-time KPI metrics, search filter, and populated student records on Netlify.")

    add_h2("View 2: Student Enrollment Modal Dialog (Create Operation)")
    add_body("Description: Interactive modal dialog allowing administrators to register new students with fields for Name, Roll Number, Email Address, Contact Phone, Department, Semester, and Enrollment Status. Built-in client validation enforces required fields and proper data formatting.")
    add_image_with_caption('doc/screenshot/form.png', Inches(4.8), "Figure 2: Student Registration Form Modal displaying field-level validation rules and enrollment input controls.")

    add_h2("View 3: Dynamic Real-Time Search & Departmental Filter (Read Operation)")
    add_body("Description: Instant debounced query execution searching across student name, roll number, or email, with live record count updating dynamically as filters are applied across departments (Computer Science, IT, ECE, Mechanical, Civil, Business Administration).")

    add_h2("View 4: Student Record Modification Dialog (Update Operation)")
    add_body("Description: Pre-populated modal dialog allowing administrative staff to modify student department, contact details, or enrollment status with instantaneous database synchronization upon submission.")

    add_h2("View 5: Safety Confirmation & Toast Feedback (Delete Operation)")
    add_body("Description: Two-step confirmation modal protecting against accidental record loss, accompanied by an animated success toast notification upon successful deletion from MongoDB Atlas.")

    # 8. GitHub Repository Screenshot and Link
    add_h1("8. GitHub Repository Screenshot and Link")
    add_h2("Metadata and Deployment Links")
    add_body("• GitHub Repository URL: https://github.com/prathamreet/fst-aat")
    add_body("• Production Deployment URL: https://fst-aat-prathamreet-1nh23cs191.netlify.app/")
    add_h2("Repository Commit History")
    add_code("""1eebe2e  docs: add official academic project report in Word (.docx) and Markdown (.md) formats
301ec47  docs: add live Netlify deployment link to README
2de1649  docs: update README with comprehensive academic documentation aligned with assessment criteria
7cde5cf  Configure reliable DNS resolution for MongoDB Atlas SRV lookup
0e4eb8a  Complete Student Management System for FST Mini Project""")

    # 9. Challenges Faced
    add_h1("9. Challenges Faced")
    add_h2("1. MongoDB Atlas SSL Alert 80 (IP Whitelist / Network Access Restriction)")
    add_body("Challenge: During initial connection testing to MongoDB Atlas, Mongoose threw 'MongooseServerSelectionError: SSL alert number 80 (tlsv1 alert internal error)'. Atlas terminated TLS handshakes because incoming client IP addresses were not permitted in the Atlas Network Access firewall.")
    add_body("Solution: Navigated to MongoDB Atlas Security Settings and updated Network Access rules to allow connection requests from anywhere (0.0.0.0/0). This resolved the TLS handshake alert and permitted both local Node.js processes and Netlify serverless functions to authenticate reliably.")

    add_h2("2. Windows ISP DNS SRV Lookup Failure (querySrv ECONNREFUSED)")
    add_body("Challenge: On Windows workstations, Node.js's native DNS subsystem occasionally failed to resolve MongoDB Atlas SRV records (_mongodb._tcp.cluster0...), throwing an immediate querySrv ECONNREFUSED error.")
    add_body("Solution: Integrated Node.js's native dns module in config/db.js and seed.js to set authoritative fallback nameservers (dns.setServers(['8.8.8.8', '1.1.1.1', '8.8.4.4'])). This eliminated the Windows ISP DNS bottleneck and guaranteed seamless database discovery.")

    add_h2("3. Serverless Decoupled Routing on Netlify")
    add_body("Challenge: Netlify natively serves static assets but requires special URL rewrite routing to channel API calls (/api/*) to AWS Lambda serverless functions without causing path duplication.")
    add_body("Solution: Structured netlify.toml with 200 rewrite rules redirecting /api/* to /.netlify/functions/api/:splat, wrapped the Express application using serverless-http, and mounted dual route aliases in server.js to ensure 100% path compatibility.")

    # 10. Learning Outcomes and Conclusion
    add_h1("10. Learning Outcomes and Conclusion")
    add_h2("Key Learning Outcomes")
    add_body("• Full-Stack Decoupled Architecture: Gained practical expertise in connecting a lightweight, responsive vanilla client to an Express.js REST API using modern asynchronous Fetch API patterns.")
    add_body("• Document-Oriented Data Modeling: Designed clean Mongoose schemas with strict data validation, unique indexes, and schema enforcement.")
    add_body("• Production Serverless Deployment: Mastered the configuration of Netlify Serverless Functions, route rewrites via netlify.toml, and MongoDB Atlas cloud security.")
    add_body("• System Resiliency & Diagnostics: Developed fault-tolerant database connection handling, including DNS failovers and serverless connection pool caching.")

    add_h2("Conclusion")
    add_body("The Student Management System successfully fulfills all requirements stipulated in the Portfolio-Driven Assessment for Full Stack Technologies. By implementing complete end-to-end CRUD operations, robust database connectivity, responsive UI design, and cloud serverless deployment, the project delivers a reliable, production-ready educational management solution.")

    try:
        doc.save("doc/Student_Management_System_Project_Report.docx")
        print("Report generated successfully: doc/Student_Management_System_Project_Report.docx")
    except PermissionError:
        fallback_path = "doc/Student_Management_System_Project_Report_Updated.docx"
        doc.save(fallback_path)
        print(f"File is open in Microsoft Word. Saved updated report to: {fallback_path}")

if __name__ == '__main__':
    create_report()
