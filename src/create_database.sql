-- Drop the database if it exists
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'StudentLoanDB')
BEGIN
    DROP DATABASE StudentLoanDB;
END
GO

-- Create the database
CREATE DATABASE StudentLoanDB;
GO

-- Use the database
USE StudentLoanDB;
GO

-- Create the Province table
CREATE TABLE Province (
    ProvinceID INT PRIMARY KEY IDENTITY(1,1),
    Province NVARCHAR(50) NOT NULL
);
GO

-- Create the EducationInstitution table
CREATE TABLE EducationInstitution (
    EducationInstitutionID INT PRIMARY KEY IDENTITY(1,1),
    College NVARCHAR(100) NOT NULL,
    CollegeCode NVARCHAR(10) NOT NULL,
    ProvinceID INT,
    FOREIGN KEY (ProvinceID) REFERENCES Province(ProvinceID)
);
GO

-- Create the Communication table
CREATE TABLE Communication (
    CommunicationID INT PRIMARY KEY IDENTITY(1,1),
    PhoneNumber NVARCHAR(20) NOT NULL,
    Email NVARCHAR(100) NOT NULL
);
GO

-- Create the LoanInfo table
CREATE TABLE LoanInfo (
    LoanInfoID INT PRIMARY KEY IDENTITY(1,1),
    EnrollmentType NVARCHAR(10) NOT NULL,
    LoanAmount DECIMAL(18, 2) NOT NULL,
    YearStarted INT NOT NULL,
    LoanBalance DECIMAL(18, 2) NOT NULL,
    PercentagePaid NVARCHAR(10) NOT NULL
);
GO

-- Create the StudyInfo table
CREATE TABLE StudyInfo (
    StudyInfoID INT PRIMARY KEY IDENTITY(1,1),
    ProgramOfStudy NVARCHAR(100) NOT NULL,
    ProgramCode NVARCHAR(10) NOT NULL,
    CollegeCode NVARCHAR(10) NOT NULL
);
GO

-- Create the Student table
CREATE TABLE Student (
    StudentID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Address NVARCHAR(200) NOT NULL,
    LoanInfoID INT,
    CommunicationID INT,
    StudyInfoID INT,
    EducationInstitutionID INT,
    FOREIGN KEY (LoanInfoID) REFERENCES LoanInfo(LoanInfoID),
    FOREIGN KEY (CommunicationID) REFERENCES Communication(CommunicationID),
    FOREIGN KEY (StudyInfoID) REFERENCES StudyInfo(StudyInfoID),
    FOREIGN KEY (EducationInstitutionID) REFERENCES EducationInstitution(EducationInstitutionID)
);
GO