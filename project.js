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
        // 显示生成的霓虹灯效果图
        const img = document.createElement('img');
        img.src = data.output_image;  // 这里需要确保后端的图像可通过 URL 访问
        document.body.appendChild(img);
    } else {
        alert('Failed to generate neon image.');
    }
});
