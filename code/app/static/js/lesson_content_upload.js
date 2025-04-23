//document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('lesson-file-upload');
    const progressBar = document.getElementById('lesson-upload-progress');
    const uploadStatus = document.getElementById('lesson-upload-status');
    const contentUrlInput = document.querySelector('[name="content_url"]');
    const currentLessonUrl = document.getElementById('current-lesson-url'); // The image element displaying the profile picture

    async function uploadFile(file) {
        const maxChunkSize =  100 * 1024; // 100 kb
        const totalChunks = Math.ceil(file.size / maxChunkSize);
        const fileId = Date.now().toString(); // Unique ID for the file
        const filename = file.name;

        for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
            const start = chunkIndex * maxChunkSize;
            const end = Math.min(start + maxChunkSize, file.size);
            const chunk = file.slice(start, end);

            const formData = new FormData();
            formData.append('file', chunk);
            formData.append('chunk_index', chunkIndex);
            formData.append('total_chunks', totalChunks);
            formData.append('file_id', fileId);
            formData.append('filename', filename);
            formData.append('course_id', course_id);

            try {
                const response = await fetch(`/courses/${course_id}/upload-lesson-content`, {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.json();
                if (!response.ok) {
                    uploadStatus.textContent = `Error uploading chunk ${chunkIndex + 1}: ${result.error}`;
                    return;
                }

                currentLessonUrl.style.display= 'block';
                
                
                if(result.filename){
                    contentUrlInput.value = result.filename;
                    currentLessonUrl.href = result.content_url;
                }

                // Update progress bar
                const progress = ((chunkIndex + 1) / totalChunks) * 100;
                progressBar.style.width = `${progress}%`;
                progressBar.textContent = `${Math.round(progress)}%`;
            } catch (error) {
                uploadStatus.textContent = `Error uploading chunk ${chunkIndex + 1}: ${error.message}`;
                return;
            }
        }

        uploadStatus.textContent = 'Lesson Content Uploaded Successfully!';
    }

    function handleFileSelection(file) {
        if (!file) return;
    
        const isValid = $('[name="lesson_file"]').valid();// Trigger validation
        const contentType = $('[name="content_type"]').val();
    
        if (!isValid) return;
    
        // Validate file size
        if (contentType === 'video' || contentType === 'pdf') {
            if (file.size > 50 * 1024 * 1024) {
                uploadStatus.textContent = 'File size exceeds 50 MB limit';
                return;
            }
        }
    
        uploadStatus.textContent = 'Uploading...';
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';
        uploadFile(file);
    }
    
    fileInput.addEventListener('change', function () {        
        const file = this.files[0];
        handleFileSelection(file);
    });
    
//});
