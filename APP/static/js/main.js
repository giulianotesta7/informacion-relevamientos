tinymce.init({
    selector: '#description',
    plugins: 'image paste',
    paste_data_images: true,
    toolbar: 'undo redo | formatselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | image',
    
    images_upload_handler: function (blobInfo, success, failure) {
        let formData = new FormData();
        formData.append('file', blobInfo.blob(), blobInfo.filename());

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            if (result.url) {
                success(result.url);  
            } else {
                failure('Error uploading image');
            }
        })
        .catch(() => failure('Error uploading image'));
    }
});

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.relevamiento-form').addEventListener('submit', function (event) {
        const editorContent = tinymce.get('description').getContent();
        document.querySelector('#description').value = editorContent;
    });
});
