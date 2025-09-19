jalaliDatepicker.startWatch();

const inputFile = document.querySelector('input[data-jdp="true"]');
const previewImage = document.getElementById('profile_image_preview');

if (inputFile && previewImage) {
    inputFile.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }
    });
}
