create database library;
use library;
#类别
CREATE TABLE Categories (  
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,  #主键，自增
    CategoryName VARCHAR(255) NOT NULL  
);  
  
#图书
CREATE TABLE Books (  
    BookID INT PRIMARY KEY AUTO_INCREMENT,  
    Title VARCHAR(255) NOT NULL,  #书名
    Author VARCHAR(255),  
    Publisher VARCHAR(255),  #出版社
    YearPublished INT,  #出版年份
    CopiesAvailable INT,  #可借数量
    TotalCopies INT,  #总数量
    CategoryID INT,  #外键
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)  
);  
  
#读者
CREATE TABLE Readers (  
    ReaderID INT PRIMARY KEY AUTO_INCREMENT,  
    Name VARCHAR(255) NOT NULL,  
    Email VARCHAR(255) UNIQUE,  
    Phone VARCHAR(20),  
    RegistrationDate DATE  #注册日期
);  
  
#借阅记录
CREATE TABLE Loans (  
    LoanID INT PRIMARY KEY AUTO_INCREMENT,  #主键，自增
    BookID INT,  
    ReaderID INT,  
    LoanDate DATE NOT NULL,  #借阅日期
    DueDate DATE NOT NULL,  #到期日期
    ReturnDate DATE,  #归还日期
    FOREIGN KEY (BookID) REFERENCES Books(BookID),  
    FOREIGN KEY (ReaderID) REFERENCES Readers(ReaderID)  
);