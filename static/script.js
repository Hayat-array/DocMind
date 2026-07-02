// ---- Theme toggle (persisted in localStorage) ----
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const root = document.documentElement;

function applyTheme(theme) {
    if (theme === 'light') {
        root.setAttribute('data-theme', 'light');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    } else {
        root.removeAttribute('data-theme');
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    }
}

const savedTheme = localStorage.getItem('docmind-theme');
const systemPrefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
applyTheme(savedTheme || (systemPrefersLight ? 'light' : 'dark'));

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const isLight = root.getAttribute('data-theme') === 'light';
        const next = isLight ? 'dark' : 'light';
        applyTheme(next);
        localStorage.setItem('docmind-theme', next);
    });
}

// ---- Dropzone: drag & drop + filename preview ----
const dropzone = document.getElementById('dropzone');
const pdfInput = document.getElementById('pdf-input');
const dzTitle = document.getElementById('dz-title');
const dzSub = document.getElementById('dz-sub');

if (dropzone && pdfInput) {
    ['dragenter', 'dragover'].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(evt => {
        dropzone.addEventListener(evt, (e) => {
            e.preventDefault();
            dropzone.classList.remove('drag-over');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        if (file && file.name.toLowerCase().endsWith('.pdf')) {
            pdfInput.files = e.dataTransfer.files;
            updateDropzoneLabel(file.name);
        }
    });

    pdfInput.addEventListener('change', () => {
        if (pdfInput.files.length > 0) {
            updateDropzoneLabel(pdfInput.files[0].name);
        }
    });
}

function updateDropzoneLabel(filename) {
    dzTitle.textContent = filename;
    dzSub.textContent = 'Ready to upload — click to change';
}

// ---- Button loading states on submit ----
const uploadForm = document.getElementById('upload-form');
const uploadBtn = document.getElementById('upload-btn');
if (uploadForm && uploadBtn) {
    uploadForm.addEventListener('submit', () => {
        if (!pdfInput.files.length) return;
        setLoading(uploadBtn, 'Uploading...');
    });
}

const askForm = document.getElementById('ask-form');
const askBtn = document.getElementById('ask-btn');
const questionInput = document.getElementById('question-input');
if (askForm && askBtn) {
    askForm.addEventListener('submit', (e) => {
        if (!questionInput || !questionInput.value.trim()) return;
        setLoading(askBtn, 'Thinking...');
    });
}

if (questionInput) {
    const resizeQuestionInput = () => {
        questionInput.style.height = 'auto';
        questionInput.style.height = `${Math.min(questionInput.scrollHeight, 220)}px`;
    };

    questionInput.addEventListener('input', resizeQuestionInput);
    resizeQuestionInput();
}

function setLoading(btn, label) {
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i><span>${label}</span>`;
}