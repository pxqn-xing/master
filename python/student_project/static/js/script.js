document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // 防止表单提交刷新页面

    const student_id = document.getElementById('student_id').value;
    const password = document.getElementById('password').value;

    // 发送 POST 请求到后端的 /login/ 接口
    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `student_id=${student_id}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // 登录成功，跳转到主界面
            window.location.href = '/main.html';
        } else {
            // 显示错误消息
            document.getElementById('error-message').textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = '登录失败，请重试！';
    });
});
