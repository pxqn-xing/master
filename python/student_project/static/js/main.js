window.onload = function() {
    // 从后端获取学生信息
    fetch('/api/get_student_info/')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // 获取学生信息并插入到表格中
            const students = data.students;
            const tableBody = document.querySelector('#studentTable tbody');
            students.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${student.student_id}</td>
                    <td>${student.name}</td>
                    <td>${student.email}</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            alert('无法获取学生信息');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('获取学生信息失败');
    });
};
