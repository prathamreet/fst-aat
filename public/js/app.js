/**
 * Student Management System - Frontend Controller
 * Pure Vanilla JavaScript (Fetch API)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Base API endpoint - works locally & on Netlify serverless
  const API_BASE = '/api/students';

  // State
  let students = [];
  let deleteTarget = null;
  let searchTimeout = null;

  // DOM Elements
  const studentsTableBody = document.getElementById('studentsTableBody');
  const recordsCount = document.getElementById('recordsCount');
  const loadingIndicator = document.getElementById('loadingIndicator');
  const emptyState = document.getElementById('emptyState');
  const emptySubtitle = document.getElementById('emptySubtitle');

  const statTotal = document.getElementById('statTotal');
  const statActive = document.getElementById('statActive');
  const statCourses = document.getElementById('statCourses');

  const searchInput = document.getElementById('searchInput');
  const clearSearchBtn = document.getElementById('clearSearchBtn');
  const courseFilter = document.getElementById('courseFilter');
  const statusFilter = document.getElementById('statusFilter');

  // Modals
  const studentModal = document.getElementById('studentModal');
  const studentForm = document.getElementById('studentForm');
  const modalTitle = document.getElementById('modalTitle');
  const openAddModalBtn = document.getElementById('openAddModalBtn');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const cancelModalBtn = document.getElementById('cancelModalBtn');
  const submitStudentBtn = document.getElementById('submitStudentBtn');

  // Delete Modal
  const deleteModal = document.getElementById('deleteModal');
  const deleteStudentName = document.getElementById('deleteStudentName');
  const deleteStudentRoll = document.getElementById('deleteStudentRoll');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
  const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
  const closeDeleteModalBtn = document.getElementById('closeDeleteModalBtn');

  const toastContainer = document.getElementById('toastContainer');

  // ==========================================
  // Fetch Functions
  // ==========================================

  // Load all students according to current filters
  async function loadStudents() {
    showLoading(true);

    try {
      const params = new URLSearchParams();
      const search = searchInput.value.trim();
      const course = courseFilter.value;
      const status = statusFilter.value;

      if (search) params.append('search', search);
      if (course && course !== 'All') params.append('course', course);
      if (status && status !== 'All') params.append('status', status);

      const res = await fetch(`${API_BASE}?${params.toString()}`);
      const result = await res.json();

      if (result.success) {
        students = result.data;
        renderTable(students);
      } else {
        showToast(result.message || 'Error loading students', 'error');
      }
    } catch (err) {
      console.error('Fetch error:', err);
      showToast('Could not connect to backend server. Make sure MongoDB and server are running.', 'error');
      renderTable([]);
    } finally {
      showLoading(false);
    }
  }

  // Load KPI Statistics
  async function loadStats() {
    try {
      const res = await fetch(`${API_BASE}/stats`);
      const result = await res.json();

      if (result.success) {
        statTotal.textContent = result.data.total;
        statActive.textContent = result.data.active;
        statCourses.textContent = result.data.totalCourses;
      }
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  }

  // ==========================================
  // Render Functions
  // ==========================================

  function renderTable(data) {
    studentsTableBody.innerHTML = '';
    recordsCount.textContent = `Showing ${data.length} record${data.length === 1 ? '' : 's'}`;

    if (data.length === 0) {
      emptyState.style.display = 'flex';
      const isFiltered = searchInput.value.trim() !== '' || courseFilter.value !== 'All' || statusFilter.value !== 'All';
      emptySubtitle.textContent = isFiltered
        ? 'No matching records found for the applied filter. Try resetting search.'
        : 'Click "Add Student" to enroll a new student into the system.';
      return;
    }

    emptyState.style.display = 'none';

    data.forEach((student) => {
      const tr = document.createElement('tr');

      const statusBadgeClass =
        student.status === 'Active'
          ? 'badge-active'
          : student.status === 'Inactive'
          ? 'badge-inactive'
          : 'badge-graduated';

      tr.innerHTML = `
        <td><span class="roll-badge">${escapeHTML(student.rollNo)}</span></td>
        <td class="student-name-cell">${escapeHTML(student.name)}</td>
        <td>
          <div class="student-email">${escapeHTML(student.email)}</div>
          ${student.phone ? `<div class="student-phone">${escapeHTML(student.phone)}</div>` : ''}
        </td>
        <td>
          <div class="course-name">${escapeHTML(student.course)}</div>
          <div class="semester-badge">${escapeHTML(student.semester || 'Semester 1')}</div>
        </td>
        <td>
          <span class="badge ${statusBadgeClass}">${escapeHTML(student.status)}</span>
        </td>
        <td class="text-right">
          <div class="actions-cell">
            <button class="btn btn-icon btn-icon-edit edit-btn" data-id="${student._id}" title="Edit student">
              Edit
            </button>
            <button class="btn btn-icon btn-icon-delete delete-btn" data-id="${student._id}" title="Delete student">
              Delete
            </button>
          </div>
        </td>
      `;

      studentsTableBody.appendChild(tr);
    });

    // Attach row button events
    document.querySelectorAll('.edit-btn').forEach((btn) => {
      btn.addEventListener('click', () => openEditModal(btn.dataset.id));
    });

    document.querySelectorAll('.delete-btn').forEach((btn) => {
      btn.addEventListener('click', () => openDeleteModal(btn.dataset.id));
    });
  }

  function showLoading(isLoading) {
    if (isLoading) {
      loadingIndicator.style.display = 'flex';
      emptyState.style.display = 'none';
    } else {
      loadingIndicator.style.display = 'none';
    }
  }

  // ==========================================
  // Modal Handlers
  // ==========================================

  function openAddModal() {
    studentForm.reset();
    document.getElementById('studentId').value = '';
    modalTitle.textContent = 'Add New Student';
    submitStudentBtn.textContent = 'Save Student';
    studentModal.style.display = 'flex';
    document.getElementById('nameInput').focus();
  }

  function openEditModal(id) {
    const student = students.find((s) => s._id === id);
    if (!student) return;

    document.getElementById('studentId').value = student._id;
    document.getElementById('nameInput').value = student.name;
    document.getElementById('rollNoInput').value = student.rollNo;
    document.getElementById('emailInput').value = student.email;
    document.getElementById('phoneInput').value = student.phone || '';
    document.getElementById('courseSelect').value = student.course;
    document.getElementById('semesterSelect').value = student.semester || 'Semester 1';
    document.getElementById('statusSelect').value = student.status || 'Active';

    modalTitle.textContent = 'Edit Student Record';
    submitStudentBtn.textContent = 'Update Student';
    studentModal.style.display = 'flex';
  }

  function closeStudentModal() {
    studentModal.style.display = 'none';
    studentForm.reset();
  }

  // ==========================================
  // Form Submission (Create & Update)
  // ==========================================

  studentForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('studentId').value;
    const isEdit = Boolean(id);

    const payload = {
      name: document.getElementById('nameInput').value.trim(),
      rollNo: document.getElementById('rollNoInput').value.trim(),
      email: document.getElementById('emailInput').value.trim(),
      phone: document.getElementById('phoneInput').value.trim(),
      course: document.getElementById('courseSelect').value,
      semester: document.getElementById('semesterSelect').value,
      status: document.getElementById('statusSelect').value
    };

    submitStudentBtn.disabled = true;
    submitStudentBtn.textContent = isEdit ? 'Updating...' : 'Saving...';

    try {
      const url = isEdit ? `${API_BASE}/${id}` : API_BASE;
      const method = isEdit ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (data.success) {
        showToast(isEdit ? 'Student record updated successfully' : 'Student added successfully');
        closeStudentModal();
        loadStudents();
        loadStats();
      } else {
        showToast(data.message || 'Operation failed', 'error');
      }
    } catch (err) {
      console.error('Save error:', err);
      showToast('An unexpected server error occurred', 'error');
    } finally {
      submitStudentBtn.disabled = false;
      submitStudentBtn.textContent = isEdit ? 'Update Student' : 'Save Student';
    }
  });

  // ==========================================
  // Delete Handlers
  // ==========================================

  function openDeleteModal(id) {
    const student = students.find((s) => s._id === id);
    if (!student) return;

    deleteTarget = student;
    deleteStudentName.textContent = student.name;
    deleteStudentRoll.textContent = `Roll: ${student.rollNo}`;
    deleteModal.style.display = 'flex';
  }

  function closeDeleteModal() {
    deleteModal.style.display = 'none';
    deleteTarget = null;
  }

  confirmDeleteBtn.addEventListener('click', async () => {
    if (!deleteTarget) return;

    confirmDeleteBtn.disabled = true;
    confirmDeleteBtn.textContent = 'Deleting...';

    try {
      const res = await fetch(`${API_BASE}/${deleteTarget._id}`, {
        method: 'DELETE'
      });
      const data = await res.json();

      if (data.success) {
        showToast(`Student record for ${deleteTarget.name} deleted`);
        closeDeleteModal();
        loadStudents();
        loadStats();
      } else {
        showToast(data.message || 'Failed to delete record', 'error');
      }
    } catch (err) {
      console.error('Delete error:', err);
      showToast('Error deleting student record', 'error');
    } finally {
      confirmDeleteBtn.disabled = false;
      confirmDeleteBtn.textContent = 'Delete Record';
    }
  });

  // ==========================================
  // Event Listeners (Search, Filter, Modal Toggles)
  // ==========================================

  openAddModalBtn.addEventListener('click', openAddModal);
  closeModalBtn.addEventListener('click', closeStudentModal);
  cancelModalBtn.addEventListener('click', closeStudentModal);

  closeDeleteModalBtn.addEventListener('click', closeDeleteModal);
  cancelDeleteBtn.addEventListener('click', closeDeleteModal);

  // Close modals on backdrop click
  window.addEventListener('click', (e) => {
    if (e.target === studentModal) closeStudentModal();
    if (e.target === deleteModal) closeDeleteModal();
  });

  // Search input debouncing
  searchInput.addEventListener('input', () => {
    clearSearchBtn.style.display = searchInput.value ? 'block' : 'none';
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      loadStudents();
    }, 300);
  });

  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    clearSearchBtn.style.display = 'none';
    loadStudents();
  });

  courseFilter.addEventListener('change', loadStudents);
  statusFilter.addEventListener('change', loadStudents);

  // ==========================================
  // Utilities
  // ==========================================

  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(20px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // Initial Load
  loadStudents();
  loadStats();
});
