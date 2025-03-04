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
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE Instructor (
    instructorId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT,
    phone TEXT,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE GymFacility (
    gymId INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    phone TEXT,
    manager TEXT
);
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
CREATE TABLE Equipment (
    equipmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('Cardio', 'Strength', 'Flexibility', 'Recovery')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    gymId INTEGER NOT NULL,
    FOREIGN KEY (gymId) REFERENCES GymFacility(gymId) ON DELETE CASCADE
);
CREATE TABLE MembershipPlan (
    planId INTEGER PRIMARY KEY AUTOINCREMENT,
    planType TEXT NOT NULL CHECK (planType IN ('Monthly', 'Annual')),
    cost NUMERIC NOT NULL CHECK (cost > 0)
);
CREATE TABLE Payment (
    paymentId INTEGER PRIMARY KEY AUTOINCREMENT,
    memberId INTEGER NOT NULL,
    planId INTEGER NOT NULL,
    amountPaid REAL NOT NULL CHECK (amountPaid > 0),
    paymentDate TEXT NOT NULL,
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (planId) REFERENCES MembershipPlan(planId) ON DELETE CASCADE
);
CREATE TABLE Attends (
    memberId INTEGER NOT NULL,
    classId INTEGER NOT NULL,
    attendanceDate TEXT NOT NULL,
    PRIMARY KEY (memberId, classId, attendanceDate),
    FOREIGN KEY (memberId) REFERENCES Member(memberId) ON DELETE CASCADE,
    FOREIGN KEY (classId) REFERENCES Class(classId) ON DELETE CASCADE
);
