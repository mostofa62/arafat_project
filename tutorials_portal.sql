
-- Create Users Table
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('teacher', 'student', 'admin')) NOT NULL,
    profile_picture TEXT,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Categories Table
CREATE TABLE Categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    thumbnail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Courses Table
CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    teacher_id INT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    language VARCHAR(50) NOT NULL,
    level VARCHAR(50) CHECK (level IN ('Beginner', 'Intermediate', 'Advanced')) NOT NULL,
    category_id INT REFERENCES Categories(id) ON DELETE SET NULL,
    thumbnail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Lessons Table
CREATE TABLE Lessons (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content_type VARCHAR(50) CHECK (content_type IN ('video', 'pdf', 'text')) NOT NULL,
    content_url TEXT,
    text_content TEXT,
    duration INTERVAL,
    "order" INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Quizzes Table
CREATE TABLE Quizzes (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Questions Table
CREATE TABLE Questions (
    id SERIAL PRIMARY KEY,
    quiz_id INT NOT NULL REFERENCES Quizzes(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Answers Table
CREATE TABLE Answers (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL REFERENCES Questions(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Quiz Attempts Table
CREATE TABLE Quiz_Attempts (
    id SERIAL PRIMARY KEY,
    quiz_id INT NOT NULL REFERENCES Quizzes(id) ON DELETE CASCADE,
    student_id INT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    score NUMERIC(5, 2) CHECK (score >= 0),
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Attempt Answers Table
CREATE TABLE Attempt_Answers (
    id SERIAL PRIMARY KEY,
    attempt_id INT NOT NULL REFERENCES Quiz_Attempts(id) ON DELETE CASCADE,
    question_id INT NOT NULL REFERENCES Questions(id) ON DELETE CASCADE,
    selected_answer_id INT NOT NULL REFERENCES Answers(id) ON DELETE CASCADE
);

-- Create Assignments Table
CREATE TABLE Assignments (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Submissions Table
CREATE TABLE Submissions (
    id SERIAL PRIMARY KEY,
    assignment_id INT NOT NULL REFERENCES Assignments(id) ON DELETE CASCADE,
    student_id INT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    submission_file TEXT NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade NUMERIC(5, 2) CHECK (grade >= 0 AND grade <= 100),
    feedback TEXT,
    graded_at TIMESTAMP
);

-- Create Enrollments Table
CREATE TABLE Enrollments (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    course_id INT NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (student_id, course_id)
);

-- Create Reviews Table
CREATE TABLE Reviews (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    student_id INT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Orders Table
CREATE TABLE Orders (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    course_id INT NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    payment_status VARCHAR(50) CHECK (payment_status IN ('pending', 'completed', 'failed')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Course Progress Table
CREATE TABLE Course_Progress (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    course_id INT NOT NULL REFERENCES Courses(id) ON DELETE CASCADE,
    lesson_id INT NOT NULL REFERENCES Lessons(id) ON DELETE CASCADE,
    completed_at TIMESTAMP
);
