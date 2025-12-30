function copyLink(btn, url) {
    navigator.clipboard.writeText(url).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Скопировано!';
        btn.style.background = 'rgba(99, 102, 241, 0.35)';
        btn.style.color = '#a5b4fc';

        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = 'rgba(99, 102, 241, 0.15)';
            btn.style.color = '#a5b4fc';
        }, 2000);
    });
}
