document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const fileNameDisplay = document.getElementById('fileName');
    const analyzeButton = document.getElementById('analyzeButton');

    if (uploadForm && fileInput && analyzeButton) {
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
                fileNameDisplay.classList.add('loaded');
                analyzeButton.disabled = false;
            } else {
                fileNameDisplay.textContent = 'No file selected';
                fileNameDisplay.classList.remove('loaded');
                analyzeButton.disabled = true;
            }
        });

        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const form = e.target;
            const formData = new FormData(form);
            const loader = document.getElementById('loader');
            const submitBtn = form.querySelector('#analyzeButton');
            const errorDiv = document.getElementById('errorMessage');
            
            errorDiv.style.display = 'none';
            errorDiv.textContent = '';
            loader.style.display = 'block';
            submitBtn.disabled = true;

            try {
                const response = await fetch('/extract-prescription', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }

                const data = await response.json();
                
                if (data.error) {
                    if (data.error.includes("429") || data.error.includes("Too Many Requests")) {
                        throw new Error("Too many requests. Please try again later.");
                    }
                    throw new Error(data.error);
                }

                sessionStorage.setItem('prescriptionResult', JSON.stringify(data));
                window.location.href = '/result';
                
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            } finally {
                loader.style.display = 'none';
                submitBtn.disabled = false;
            }
        });
    }
});

(function handleResultPage() {
    if (window.location.pathname !== '/result') {
        return;
    }

    const result = JSON.parse(sessionStorage.getItem('prescriptionResult'));
    const resultContainer = document.getElementById('resultContainer');
    
    if (!resultContainer) {
        return;
    }

    if (!result) {
        resultContainer.innerHTML = '<div class="error">No result found. Please upload a prescription first.</div>';
        return;
    }

    if (result.error) {
        resultContainer.innerHTML = `<div class="error">${result.error}</div>`;
        return;
    }

    let html = `
        <div class="result-card">
            <h2>Patient Information</h2>
            <ul>
                <li><strong>Name:</strong> ${result["Patient's full name"] || 'Not available'}</li>
                <li><strong>Age:</strong> ${result["Patient's age"] || 'Not available'}</li>
                <li><strong>Gender:</strong> ${result["Patient's gender"] || 'Not available'}</li>
            </ul>
        </div>
        
        <div class="result-card">
            <h2>Doctor Information</h2>
            <ul>
                <li><strong>Name:</strong> ${result["Doctor's full name"] || 'Not available'}</li>
                <li><strong>License:</strong> ${result["Doctor's license number"] || 'Not available'}</li>
                <li><strong>Date:</strong> ${result["Prescription date"] || 'Not available'}</li>
            </ul>
        </div>
        
        <div class="result-card">
            <h2>Medications</h2>
    `;
    
    if (result.Medications && result.Medications.length > 0) {
        result.Medications.forEach(med => {
            html += `
                <ul>
                    <li><strong>Name:</strong> ${med["Medication name"] || 'Not available'}</li>
                    <li><strong>Dosage:</strong> ${med.Dosage || 'Not available'}</li>
                    <li><strong>Frequency:</strong> ${med.Frequency || 'Not available'}</li>
                    <li><strong>Duration:</strong> ${med.Duration || 'Not available'}</li>
                    <li><strong>Description:</strong> ${med["Medicine Description"] || 'Not available'}</li>
                    <li><strong>Usage:</strong> ${med["Medicine Usage"] || 'Not available'}</li>
                    <li><strong>Side Effects:</strong> ${med["Medicine Side effects"] || 'Not available'}</li>
                </ul>
                <hr>
            `;
        });
    } else {
        html += '<p>No medications found</p>';
    }
    html += '</div>';

    html += '<div class="result-card"><h2>Additional Notes</h2>';
    if (result["Additional notes"]) {
        const noteOrder = [
            "Complaints of (c/o)",
            "General Advice",
            "Duration",
            "Contact Information",
            "Disclaimer"
        ];

        const notes = result["Additional notes"];
        if (notes["(c/o) complaints of"]) {
            notes["Complaints of (c/o)"] = notes["(c/o) complaints of"];
            delete notes["(c/o) complaints of"];
        }

        noteOrder.forEach(key => {
            if (notes[key]) {
                if (Array.isArray(notes[key])) {
                    html += `<h3>${key}</h3><ul>`;
                    notes[key].forEach(item => html += `<li>${item}</li>`);
                    html += '</ul>';
                } else {
                    html += `<h3>${key}</h3><ul><li>${notes[key]}</li></ul>`;
                }
            }
        });

        for (const [key, value] of Object.entries(notes)) {
            if (!noteOrder.includes(key)) {
                if (Array.isArray(value)) {
                    html += `<h3>${key}</h3><ul>`;
                    value.forEach(item => html += `<li>${item}</li>`);
                    html += '</ul>';
                } else {
                    html += `<h3>${key}</h3><ul><li>${value}</li></ul>`;
                }
            }
        }
    } else {
        html += '<p>Not available</p>';
    }
    html += '</div>';

    resultContainer.innerHTML = html;
})();