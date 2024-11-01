// 用户提交自定义颜色
document.getElementById('submit-colors').addEventListener('click', function() {
    const paths = document.querySelectorAll('.neon-path');
    const colorData = [];
    paths.forEach((path, index) => {
        const color = path.getAttribute('stroke');
        colorData.push({ pathIndex: index, color });
    });

    fetch('/submit-colors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(colorData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Colors submitted successfully!');
        } else {
            alert('Failed to submit colors.');
        }
    });
});
