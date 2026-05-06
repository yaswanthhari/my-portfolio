document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileNameDisplay = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file');
    const parseBtn = document.getElementById('parse-btn');
    
    const loadingState = document.getElementById('loading');
    const resultsSection = document.getElementById('results');
    
    const resName = document.getElementById('res-name');
    const resEmail = document.getElementById('res-email');
    const resPhone = document.getElementById('res-phone');
    const resSummary = document.getElementById('res-summary');
    const resSkills = document.getElementById('res-skills');

    let selectedFile = null;

    // Drag and Drop Events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', handleDrop, false);
    dropZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    removeFileBtn.addEventListener('click', clearFile);
    parseBtn.addEventListener('click', parseResume);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFiles(files[0]);
        }
    }

    function handleFileSelect(e) {
        if (e.target.files.length > 0) {
            handleFiles(e.target.files[0]);
        }
    }

    function handleFiles(file) {
        if (file.type !== 'application/pdf') {
            alert('Please upload a valid PDF file.');
            return;
        }
        selectedFile = file;
        
        // Update UI
        fileNameDisplay.textContent = file.name;
        dropZone.classList.add('hidden');
        fileInfo.classList.remove('hidden');
        parseBtn.disabled = false;
        resultsSection.classList.add('hidden');
    }

    function clearFile(e) {
        e.stopPropagation();
        selectedFile = null;
        fileInput.value = '';
        
        // Update UI
        fileInfo.classList.add('hidden');
        dropZone.classList.remove('hidden');
        parseBtn.disabled = true;
        resultsSection.classList.add('hidden');
    }

    async function parseResume() {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        // Show loading state
        parseBtn.disabled = true;
        loadingState.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error parsing resume:', error);
            alert('Failed to parse resume. Please try again.');
        } finally {
            loadingState.classList.add('hidden');
            parseBtn.disabled = false;
        }
    }

    function displayResults(data) {
        // Populate fields
        resName.textContent = data.name && data.name !== "Unknown" ? data.name : "Candidate Name Not Found";
        
        // Handle Email
        if (data.email) {
            resEmail.innerHTML = `<i class="fa-solid fa-envelope"></i> ${data.email}`;
            resEmail.style.display = 'flex';
        } else {
            resEmail.style.display = 'none';
        }

        // Handle Phone
        if (data.phone) {
            resPhone.innerHTML = `<i class="fa-solid fa-phone"></i> ${data.phone}`;
            resPhone.style.display = 'flex';
        } else {
            resPhone.style.display = 'none';
        }

        // Handle Summary
        resSummary.textContent = data.ai_summary || "Could not generate summary.";

        // Handle Skills
        resSkills.innerHTML = '';
        if (data.skills && data.skills.length > 0) {
            data.skills.forEach(skill => {
                const chip = document.createElement('div');
                chip.className = 'skill-chip';
                chip.textContent = skill;
                resSkills.appendChild(chip);
            });
        } else {
            resSkills.innerHTML = '<span class="text-muted">No specific skills detected.</span>';
        }

        // Show results with animation
        resultsSection.classList.remove('hidden');
    }
});
