function copyUrl(btn) {
    const urlInput = document.getElementById('shortUrl');
    urlInput.select();
    urlInput.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(urlInput.value).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Скопировано!';
        btn.style.background = 'linear-gradient(135deg, #6366f1, #4f46e5)';

        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = 'linear-gradient(135deg, #818cf8, #6366f1)';
        }, 2000);
    });
}
