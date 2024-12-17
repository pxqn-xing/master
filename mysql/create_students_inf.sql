CREATE DATABASE students_inf;
USE students_inf;

CREATE TABLE Majors (
    major_id INT AUTO_INCREMENT PRIMARY KEY,  -- 专业ID
    major_name VARCHAR(100) NOT NULL         -- 专业名称
);

CREATE TABLE Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,  -- 学生ID
    name VARCHAR(100) NOT NULL,  -- 名字
    gender ENUM('男', '女') NOT NULL,  -- 性别  
    date_of_birth DATE NOT NULL,  -- 出生日期  
    contact_no VARCHAR(15),  -- 联系电话  
    email VARCHAR(100) UNIQUE,  -- 电子邮件  
    enrollment_date DATE NOT NULL,  -- 入学日期  
    academy VARCHAR(100) NOT NULL,    -- 学院
    major VARCHAR(100) NOT NULL  -- 专业
);

CREATE TABLE Teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,  
    name VARCHAR(100) NOT NULL,  -- 名字 
    gender ENUM('男', '女') NOT NULL,  -- 性别  
    email VARCHAR(100) UNIQUE,  -- 电子邮件  
    academy VARCHAR(100) NOT NULL  -- 所属学院 
); 

CREATE TABLE Academies (
    academy_id INT AUTO_INCREMENT PRIMARY KEY,  -- 学院ID
    academy_name VARCHAR(100) NOT NULL,         -- 学院名称
    major_name VARCHAR(100) NOT NULL,           -- 专业名称
    major_id INT NOT NULL,                      -- 专业ID
    student_count INT,                          -- 专业人数
    FOREIGN KEY (major_id) REFERENCES Majors(major_id) -- 参照专业表
);

CREATE TABLE Users (
    id INT NOT NULL AUTO_INCREMENT,  -- 用户ID
    username VARCHAR(50) NOT NULL,  -- 用户名
    password VARCHAR(50) NOT NULL,  -- 密码
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- 更新时间
    PRIMARY KEY (id)  -- 主键
);

CREATE TABLE Courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,  
    course_name VARCHAR(100) NOT NULL,  -- 课程名称  
    description TEXT,  -- 课程描述  
    credits INT NOT NULL,  -- 学分  
    teachername varchar(100)
);

CREATE TABLE Grades (  
    grade_id INT AUTO_INCREMENT PRIMARY KEY,  
    student_id INT,  -- 学生ID  
    course_id INT,  -- 课程ID  
    grade FLOAT NOT NULL,  -- 成绩  
    date_graded DATE NOT NULL,  -- 成绩录入日期  
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,  -- 外键约束，关联到Students表
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE ON UPDATE CASCADE  -- 外键约束，关联到Courses表
);

CREATE TABLE TempGrades (  
    student_id INT,  
    course_id INT,  
    PRIMARY KEY (student_id, course_id),  -- 确保每个学生每门课程只有一条成绩记录  
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,  -- 外键约束，关联到Students表
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE ON UPDATE CASCADE  -- 外键约束，关联到Courses表
);

CREATE TABLE Root (
    id INT NOT NULL AUTO_INCREMENT,  -- 用户ID
    username VARCHAR(50) NOT NULL,  -- 用户名
    password VARCHAR(50) NOT NULL,  -- 密码
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- 更新时间
    PRIMARY KEY (id)  -- 主键
);