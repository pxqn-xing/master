-- 创建数据库并选择
CREATE DATABASE students_inf;
USE students_inf;

-- 创建学生表
CREATE TABLE Students (  
    student_id INT AUTO_INCREMENT PRIMARY KEY,  
    name VARCHAR(100) NOT NULL,  -- 名字
    gender CHAR(1) CHECK (gender IN ('男', '女')),  -- 性别  
    date_of_birth DATE NOT NULL,  -- 出生日期  
    contact_no VARCHAR(15),  -- 联系电话  
    email VARCHAR(100) UNIQUE,  -- 电子邮件  
    enrollment_date DATE NOT NULL,  -- 入学日期  
    academy VARCHAR(100) NOT NULL,    -- 学院
    major VARCHAR(100) NOT NULL  -- 专业
);  

-- 插入学生数据
INSERT INTO Students VALUES(2018100101,"王亮","男","1999-07-21",18227407896,"10001@qq.com","2018-09-01","人工智能学院","人工智能");
INSERT INTO Students VALUES(2018100102,"张毅","男","1999-05-27",14265307886,"10002@qq.com","2018-09-01","人工智能学院","人工智能");
INSERT INTO Students VALUES(2018100201,"杨文文","女","2000-01-17",18575839857,"10003@qq.com","2018-09-01","人工智能学院","区块链工程");
INSERT INTO Students VALUES(2018110101,"吴达劲","男","1999-06-01",142674071187,"10004@qq.com","2018-09-01","软件工程学院","软件工程");
INSERT INTO Students VALUES(2017110102,"罗蕊","女","1998-04-11",18789240786,"10005@qq.com","2017-09-01","软件工程学院","软件工程");
INSERT INTO Students VALUES(2018120101,"孙筱筱","女","1998-07-10",18211437006,"10006@qq.com","2018-09-01","计算机科学学院","计算机科学与技术");
INSERT INTO Students VALUES(2018120102,"秦一","男","1999-09-01",18477897800,"10007@qq.com","2018-09-01","计算机科学学院","计算机科学与技术");
INSERT INTO Students VALUES(2017130101,"肖邡琳","女","1998-12-21",18227407896,"10008@qq.com","2017-09-01","电子信息工程学院","集成电路设计与集成系统");
INSERT INTO Students VALUES(2017140101,"方静","女","1999-7-11",18227407896,"10009@qq.com","2017-09-01","会计学院","会计学");
INSERT INTO Students VALUES(2018140101,"杨思思","女","1999-08-01",18227407896,"10010@qq.com","2018-09-01","会计学院","会计学");
INSERT INTO Students VALUES(2018150101,"黄金","男","1999-09-16",18227407896,"10011@qq.com","2018-09-01","土木工程学院","土木工程");
INSERT INTO Students VALUES(2018150201,"董浩","男","1999-03-11",18227407896,"10012@qq.com","2018-09-01","土木工程学院","测绘工程");
INSERT INTO Students VALUES(2018160101,"李杰","男","1999-01-10",18227407896,"10013@qq.com","2018-09-01","大气科学学院","应用气象学");

-- 创建教师表
CREATE TABLE Teachers (  
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,  
    name VARCHAR(100) NOT NULL,  -- 名字 
    gender CHAR(1) CHECK (gender IN ('男', '女')),  -- 性别  
    date_of_birth DATE NOT NULL,  -- 出生日期  
    contact_no VARCHAR(15),  -- 联系电话  
    email VARCHAR(100) UNIQUE,  -- 电子邮件  
    academy VARCHAR(100) NOT NULL  -- 所属学院 
);  

-- 插入教师数据
INSERT INTO Teachers VALUES(199701,"孙素强","男","1983-01-25",'14165471102',"sunsuqiang@school.com","土木工程学院");
INSERT INTO Teachers VALUES(199402,'张伟', '男', '1970-05-12', '13800138000', 'zhangwei@school.com', '计算机科学学院'); 
INSERT INTO Teachers VALUES(198903,'李娜', '女', '1975-08-23', '13900239000', 'lina@school.com', '数学学院');
INSERT INTO Teachers VALUES(199304,'王芳', '女', '1980-11-05', '13600336000', 'wangfang@school.com', '物理学院');  
INSERT INTO Teachers VALUES(198705,'赵雷', '男', '1985-03-17', '13700437000', 'zhaolei@school.com', '人工智能学院'); 
INSERT INTO Teachers VALUES(197606,'刘洋', '男', '1990-06-30', '13500535000', 'liuyang@school.com', '大气科学学院');  
INSERT INTO Teachers VALUES(198807,'陈静', '女', '1995-09-12', '13400634000', 'chenjing@school.com', '会计学院');  
INSERT INTO Teachers VALUES(199108,'杨明', '男', '2000-12-20', '13300733000', 'yangming@school.com', '电子信息工程学院');  
INSERT INTO Teachers VALUES(199909,'周丽', '女', '2005-02-08', '13200832000', 'zhouli@school.com', '软件工程学院'); 
INSERT INTO Teachers VALUES(199410,'吴强', '男', '2010-04-25', '13100931000', 'wuqiang@school.com', '软件工程学院'); 
INSERT INTO Teachers VALUES(199211,'郑敏', '女', '2015-07-10', '13001030000', 'zhengmin@school.com', '计算机科学学院');

-- 创建课程表
CREATE TABLE Courses (  
    course_id INT AUTO_INCREMENT PRIMARY KEY,  
    course_name VARCHAR(100) NOT NULL,  -- 课程名称  
    description TEXT,  -- 课程描述  
    credits INT NOT NULL,  -- 学分  
    teacher_id INT,  -- 授课教师ID  
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)  -- 外键约束  
);

-- 插入课程数据
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('数据库系统原理', '介绍数据库的基本概念、设计和实现技术。', 4,198705); 
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('操作系统', '探讨操作系统的原理、结构和功能。', 3,199211);
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('数据结构', '学习基本的数据结构和算法。', 4,199410);
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('微积分', '讲解微积分的基本原理和应用。', 3,198903);  
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('计算机网络', '介绍计算机网络的基本原理和协议。', 4,199909);  
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('软件工程', '学习软件开发的过程和方法。', 3,199909);
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('人工智能导论', '介绍人工智能的基本原理和应用领域。', 4,198705);  
INSERT INTO Courses (course_name, description, credits, teacher_id) VALUES ('会计原理', '讲解会计的基本概念和原则。', 3,198807);

-- 创建成绩表
CREATE TABLE Grades (  
    grade_id INT AUTO_INCREMENT PRIMARY KEY,  
    student_id INT,  -- 学生ID  
    course_id INT,  -- 课程ID  
    grade FLOAT NOT NULL,  -- 成绩  
    date_graded DATE NOT NULL,  -- 成绩录入日期  
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,  -- 外键约束
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE ON UPDATE CASCADE  -- 外键约束  
);

-- 创建临时成绩表，确保唯一性
CREATE TABLE TempGrades (  
    student_id INT,  
    course_id INT,  
    PRIMARY KEY (student_id, course_id)  -- 确保每个学生每门课程只有一条成绩记录  
);  

-- 创建用户表
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

-- 插入用户数据
INSERT INTO users (username, password) VALUES ('users', '123456');
