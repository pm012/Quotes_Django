const avatarInput = document.getElementById("id_avatar");
const avatarPreview = document.getElementById("avatar-preview");

if (avatarInput && avatarPreview) {
    let previewUrl;

    avatarInput.addEventListener("change", () => {
        const [file] = avatarInput.files;
        if (!file) {
            return;
        }

        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
        }
        previewUrl = URL.createObjectURL(file);
        avatarPreview.src = previewUrl;
    });

    window.addEventListener("pagehide", () => {
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
        }
    });
}
