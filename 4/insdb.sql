PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Member (
    memberId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    address TEXT,
    age INTEGER CHECK (age >= 15),
    membershipStartDate TEXT NOT NULL,
    membershipEndDate TEXT NOT NULL CHECK (membershipEndDate >= membershipStartDate)
);
INSERT INTO Member VALUES(1,'John Doe','john@example.com','555-1234','123 Main St',25,'2024-01-01','2024-12-31');
INSERT INTO Member VALUES(2,'Jane Smith','jane@example.com','555-5678','456 Elm St',30,'2024-02-01','2024-12-31');
INSERT INTO Member VALUES(3,'Mark Brown','mark@example.com','555-1111','789 Pine St',18,'2024-03-01','2024-12-31');
INSERT INTO Member VALUES(4,'Lisa White','lisa@example.com','555-2222','321 Oak St',27,'2024-04-01','2024-12-31');
INSERT INTO Member VALUES(5,'James Green','james@example.com','555-3333','654 Birch St',32,'2024-05-01','2024-12-31');
CREATE TABLE Instructor (
    instructorId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT,
    phone TEXT,
    email TEXT NOT NULL UNIQUE
);
INSERT INTO Instructor VALUES(1,'Mike Tyson','Boxing','555-7777','mike@example.com');
INSERT INTO Instructor VALUES(2,'Serena Williams','Tennis','555-8888','serena@example.com');
INSERT INTO Instructor VALUES(3,'Usain Bolt','Sprint','555-9999','usain@example.com');
INSERT INTO Instructor VALUES(4,'LeBron James','Basketball','555-6666','lebron@example.com');
INSERT INTO Instructor VALUES(5,'Tom Brady','Football','555-5555','tom@example.com');
CREATE TABLE GymFacility (
    gymId INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    phone TEXT,
    manager TEXT
);
INSERT INTO GymFacility VALUES(1,'Downtown Gym','555-4444','John Manager');
INSERT INTO GymFacility VALUES(2,'Westside Gym','555-3333','Sarah Coach');
INSERT INTO GymFacility VALUES(3,'Eastside Gym','555-2222','Paul Trainer');
INSERT INTO GymFacility VALUES(4,'North Gym','555-1111','Emily Supervisor');
INSERT INTO GymFacility VALUES(5,'South Gym','555-0000','Jake Owner');
CREATE TABLE Class (
    classId INTEGER PRIMARY KEY AUTOINCREMENT,
    className TEXT NOT NULL,
    classType TEXT NOT NULL CHECK (classType IN ('Yoga', 'Zumba', 'HIIT', 'Weights')),
    duration INTEGER NOT NULL,
    classCapacity INTEGER NOT NULL,
    instructorId INTEGER NOT NULL,
    gymId INTEGER NOT NULL,
    FOREIGN KEY (instructorId) REFERENCES Instructor(instructorId) ON DELETE CASCADE,
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId) ON DELETE CASCADE
);
INSERT INTO Class VALUES(1,'Yoga Basics','Yoga',60,10,1,1);
INSERT INTO Class VALUES(2,'Zumba Dance','Zumba',45,15,2,2);
INSERT INTO Class VALUES(3,'HIIT Strength','HIIT',30,20,3,3);
INSERT INTO Class VALUES(4,'Weight Training','Weights',50,12,4,4);
INSERT INTO Class VALUES(5,'Advanced Yoga','Yoga',90,8,5,5);
CREATE TABLE Equipment (
    equipmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('Cardio', 'Strength', 'Flexibility', 'Recovery')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    gymId INTEGER NOT NULL,
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId) ON DELETE CASCADE
);
INSERT INTO Equipment VALUES(1,'Treadmill','Cardio',5,1);
INSERT INTO Equipment VALUES(2,'Bench Press','Strength',3,2);
INSERT INTO Equipment VALUES(3,'Dumbbells','Strength',10,3);
INSERT INTO Equipment VALUES(4,'Rowing Machine','Cardio',2,4);
INSERT INTO Equipment VALUES(5,'Resistance Bands','Flexibility',15,5);
CREATE TABLE MembershipPlan (
    planId INTEGER PRIMARY KEY AUTOINCREMENT,
    planType TEXT NOT NULL CHECK (planType IN ('Monthly', 'Annual')),
    cost NUMERIC NOT NULL CHECK (cost > 0)
);
INSERT INTO MembershipPlan VALUES(1,'Monthly',50);
INSERT INTO MembershipPlan VALUES(2,'Annual',500);
INSERT INTO MembershipPlan VALUES(3,'Monthly',55);
INSERT INTO MembershipPlan VALUES(4,'Annual',480);
INSERT INTO MembershipPlan VALUES(5,'Monthly',60);
CREATE TABLE Payment (
    paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberId INTEGER NOT NULL,
    planId INTEGER NOT NULL,
    amountPaid REAL NOT NULL CHECK (amountPaid > 0),
    paymentDate TEXT NOT NULL,
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (planId) REFERENCES MembershipPlan(planId) ON DELETE CASCADE
);
INSERT INTO Payment VALUES(1,1,1,50.0,'2024-01-01');
INSERT INTO Payment VALUES(2,2,2,500.0,'2024-02-01');
INSERT INTO Payment VALUES(3,3,3,55.0,'2024-03-01');
INSERT INTO Payment VALUES(4,4,4,480.0,'2024-04-01');
INSERT INTO Payment VALUES(5,5,5,60.0,'2024-05-01');
CREATE TABLE Attends (
    memberId INTEGER NOT NULL,
    classId INTEGER NOT NULL,
    attendanceDate TEXT NOT NULL,
    PRIMARY KEY (memberId, classId, attendanceDate),
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (classId) REFERENCES Class(classId) ON DELETE CASCADE
);
INSERT INTO Attends VALUES(1,1,'2024-03-01');
INSERT INTO Attends VALUES(2,2,'2024-03-02');
INSERT INTO Attends VALUES(3,3,'2024-03-03');
INSERT INTO Attends VALUES(4,4,'2024-03-04');
INSERT INTO Attends VALUES(5,5,'2024-03-05');
INSERT INTO sqlite_sequence VALUES('MembershipPlan',5);
INSERT INTO sqlite_sequence VALUES('Member',5);
INSERT INTO sqlite_sequence VALUES('Instructor',5);
INSERT INTO sqlite_sequence VALUES('GymFacility',5);
INSERT INTO sqlite_sequence VALUES('Class',5);
INSERT INTO sqlite_sequence VALUES('Equipment',5);
INSERT INTO sqlite_sequence VALUES('Payment',5);
COMMIT;
