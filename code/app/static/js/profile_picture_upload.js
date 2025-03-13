document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('profile-picture-upload');
    const progressBar = document.getElementById('upload-progress-bar');
    const uploadStatus = document.getElementById('upload-status');
    const currentProfilePicture = document.getElementById('current-profile-picture'); // The image element displaying the profile picture

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

            try {
                const response = await fetch('/admin/upload-profile-picture', {
                    method: 'POST',
                    body: formData,
                });

                const result = await response.json();
                if (!response.ok) {
                    uploadStatus.textContent = `Error uploading chunk ${chunkIndex + 1}: ${result.error}`;
                    return;
                }

                
                if(result.image_url){
                    currentProfilePicture.src = result.image_url;
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

        uploadStatus.textContent = 'Profile Picture Changed Successfully!';
    }

    fileInput.addEventListener('change', function () {
        const file = this.files[0];
        if (!file) return;

        // Validate file size
        if (file.size > 2 * 1024 * 1024) {
            uploadStatus.textContent = 'File size exceeds 2 MB limit';
            return;
        }

        uploadStatus.textContent = 'Uploading...';
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';
        uploadFile(file);
    });
});
