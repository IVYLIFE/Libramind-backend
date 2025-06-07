-- ========================================= [Table Creation] =========================================



-- Drop table if it exists (optional safety)
DROP TABLE IF EXISTS issued_books;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS students;

-- Create the books table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL CHECK (char_length(title) >= 3),
    author VARCHAR(255) NOT NULL CHECK (char_length(author) >= 3),
    isbn VARCHAR(13) NOT NULL CHECK (char_length(isbn) >= 10),
    category VARCHAR(100) NOT NULL CHECK (char_length(category) >= 3),
    copies INT NOT NULL CHECK (copies >= 1)
);

-- Create the students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL CHECK (char_length(title) >= 3),
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    phone VARCHAR(15) NOT NULL CHECK (phone ~ '^[0-9+]{10,15}$'),
    email VARCHAR(100) UNIQUE NOT NULL CHECK (email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$')
);

CREATE TABLE issued_books (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    returned_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);



-- ========================================= [Adding Records ] =========================================




-- Insert 50 books
INSERT INTO books (title, author, isbn, category, copies) VALUES
('The Catcher in the Rye', 'J.D. Salinger', '9780316769488', 'Fiction', 6),
('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'Classic', 10),
('1984', 'George Orwell', '9780451524935', 'Dystopian', 7),
('Pride and Prejudice', 'Jane Austen', '9780141439518', 'Romance', 5),
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Classic', 8),
('Moby-Dick', 'Herman Melville', '9781503280786', 'Adventure', 4),
('Brave New World', 'Aldous Huxley', '9780060850524', 'Science Fiction', 9),
('War and Peace', 'Leo Tolstoy', '9780199232765', 'Historical', 3),
('Ulysses', 'James Joyce', '9780199535675', 'Modernist', 6),
('Crime and Punishment', 'Fyodor Dostoevsky', '9780143058144', 'Philosophical', 5),
('The Hobbit', 'J.R.R. Tolkien', '9780547928227', 'Fantasy', 10),
('The Lord of the Rings', 'J.R.R. Tolkien', '9780618640157', 'Fantasy', 15),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', '9780590353427', 'Fantasy', 12),
('The Da Vinci Code', 'Dan Brown', '9780307474278', 'Thriller', 6),
('Angels & Demons', 'Dan Brown', '9780743493468', 'Thriller', 7),
('The Alchemist', 'Paulo Coelho', '9780061122415', 'Fiction', 11),
('The Book Thief', 'Markus Zusak', '9780375842207', 'Historical Fiction', 8),
('The Fault in Our Stars', 'John Green', '9780142424179', 'Young Adult', 9),
('Gone Girl', 'Gillian Flynn', '9780307588371', 'Mystery', 6),
('The Girl on the Train', 'Paula Hawkins', '9781594634024', 'Mystery', 7),
('A Game of Thrones', 'George R.R. Martin', '9780553573404', 'Fantasy', 10),
('The Name of the Wind', 'Patrick Rothfuss', '9780756404741', 'Fantasy', 8),
('Dune', 'Frank Herbert', '9780441013593', 'Science Fiction', 9),
('Ender''s Game', 'Orson Scott Card', '9780812550702', 'Science Fiction', 6),
('Fahrenheit 451', 'Ray Bradbury', '9781451673319', 'Dystopian', 5),
('The Road', 'Cormac McCarthy', '9780307387899', 'Post-apocalyptic', 4),
('Life of Pi', 'Yann Martel', '9780156027328', 'Adventure', 7),
('Memoirs of a Geisha', 'Arthur Golden', '9780679781585', 'Historical Fiction', 6),
('The Shining', 'Stephen King', '9780307743657', 'Horror', 8),
('It-A', 'Stephen King', '9781501142970', 'Horror', 9),
('Misery', 'Stephen King', '9781501143106', 'Horror', 7),
('Dracula', 'Bram Stoker', '9780141439846', 'Horror', 5),
('Frankenstein', 'Mary Shelley', '9780141439471', 'Horror', 6),
('The Picture of Dorian Gray', 'Oscar Wilde', '9780141439570', 'Classic', 5),
('Wuthering Heights', 'Emily Brontë', '9780141439556', 'Classic', 4),
('Jane Eyre', 'Charlotte Brontë', '9780141441146', 'Classic', 6),
('Little Women', 'Louisa May Alcott', '9780142408766', 'Classic', 6),
('A Tale of Two Cities', 'Charles Dickens', '9780141439600', 'Historical', 6),
('Great Expectations', 'Charles Dickens', '9780141439563', 'Classic', 5),
('The Odyssey', 'Homer', '9780140268867', 'Epic', 7),
('The Iliad', 'Homer', '9780140275360', 'Epic', 6),
('The Divine Comedy', 'Dante Alighieri', '9780140448955', 'Epic', 4),
('Inferno', 'Dan Brown', '9781400079155', 'Thriller', 6),
('Deception Point', 'Dan Brown', '9781416524809', 'Thriller', 5),
('Digital Fortress', 'Dan Brown', '9780312944926', 'Thriller', 4),
('Norwegian Wood', 'Haruki Murakami', '9780375704024', 'Literary Fiction', 6),
('Kafka on the Shore', 'Haruki Murakami', '9781400079278', 'Fantasy', 5),
('1Q84', 'Haruki Murakami', '9780307593313', 'Magical Realism', 7),
('The Wind-Up Bird Chronicle', 'Haruki Murakami', '9780679775430', 'Magical Realism', 6);










-- Insert 50 Students
INSERT INTO students (name, roll_number, department, semester, phone, email) VALUES
('Alice', 'CS101', 'CS', 3, '9876000001', 'alice@example.com'),
('Bob', 'CS102', 'CS', 2, '9876000002', 'bob@example.com'),
('Charlie', 'CS103', 'CS', 1, '9876000003', 'charlie@example.com'),
('David', 'CS104', 'CS', 4, '9876000004', 'david@example.com'),
('Eve', 'CS105', 'CS', 5, '9876000005', 'eve@example.com'),
('Frank', 'CS106', 'CS', 6, '9876000006', 'frank@example.com'),
('Grace', 'CS107', 'CS', 7, '9876000007', 'grace@example.com'),
('Hank', 'CS108', 'CS', 8, '9876000008', 'hank@example.com'),
('Ivy', 'CS109', 'CS', 2, '9876000009', 'ivy@example.com'),
('Jack', 'CS110', 'CS', 3, '9876000010', 'jack@example.com'),
('Kate', 'EE201', 'EE', 1, '9876000011', 'kate@example.com'),
('Leo', 'EE202', 'EE', 2, '9876000012', 'leo@example.com'),
('Mona', 'EE203', 'EE', 3, '9876000013', 'mona@example.com'),
('Nick', 'EE204', 'EE', 4, '9876000014', 'nick@example.com'),
('Olivia', 'EE205', 'EE', 5, '9876000015', 'olivia@example.com'),
('Paul', 'EE206', 'EE', 6, '9876000016', 'paul@example.com'),
('Quinn', 'EE207', 'EE', 7, '9876000017', 'quinn@example.com'),
('Rose', 'EE208', 'EE', 8, '9876000018', 'rose@example.com'),
('Sam', 'EE209', 'EE', 2, '9876000019', 'sam@example.com'),
('Tina', 'EE210', 'EE', 3, '9876000020', 'tina@example.com'),
('Uma', 'ME301', 'ME', 1, '9876000021', 'uma@example.com'),
('Victor', 'ME302', 'ME', 2, '9876000022', 'victor@example.com'),
('Wendy', 'ME303', 'ME', 3, '9876000023', 'wendy@example.com'),
('Xavier', 'ME304', 'ME', 4, '9876000024', 'xavier@example.com'),
('Yara', 'ME305', 'ME', 5, '9876000025', 'yara@example.com'),
('Zane', 'ME306', 'ME', 6, '9876000026', 'zane@example.com'),
('Amy', 'ME307', 'ME', 7, '9876000027', 'amy@example.com'),
('Ben', 'ME308', 'ME', 8, '9876000028', 'ben@example.com'),
('Cathy', 'ME309', 'ME', 2, '9876000029', 'cathy@example.com'),
('Dan', 'ME310', 'ME', 3, '9876000030', 'dan@example.com'),
('Ella', 'CE401', 'CE', 1, '9876000031', 'ella@example.com'),
('Fred', 'CE402', 'CE', 2, '9876000032', 'fred@example.com'),
('Gina', 'CE403', 'CE', 3, '9876000033', 'gina@example.com'),
('Harry', 'CE404', 'CE', 4, '9876000034', 'harry@example.com'),
('Isla', 'CE405', 'CE', 5, '9876000035', 'isla@example.com'),
('Jake', 'CE406', 'CE', 6, '9876000036', 'jake@example.com'),
('Kim', 'CE407', 'CE', 7, '9876000037', 'kim@example.com'),
('Liam', 'CE408', 'CE', 8, '9876000038', 'liam@example.com'),
('Maya', 'CE409', 'CE', 2, '9876000039', 'maya@example.com'),
('Noah', 'CE410', 'CE', 3, '9876000040', 'noah@example.com'),
('Omar', 'IT501', 'IT', 1, '9876000041', 'omar@example.com'),
('Pam', 'IT502', 'IT', 2, '9876000042', 'pam@example.com'),
('Qian', 'IT503', 'IT', 3, '9876000043', 'qian@example.com'),
('Rita', 'IT504', 'IT', 4, '9876000044', 'rita@example.com'),
('Steve', 'IT505', 'IT', 5, '9876000045', 'steve@example.com'),
('Tara', 'IT506', 'IT', 6, '9876000046', 'tara@example.com'),
('Usha', 'IT507', 'IT', 7, '9876000047', 'usha@example.com'),
('Vik', 'IT508', 'IT', 8, '9876000048', 'vik@example.com'),
('Walt', 'IT509', 'IT', 2, '9876000049', 'walt@example.com'),
('Zoya', 'IT510', 'IT', 3, '9876000050', 'zoya@example.com');







-- Insert 50 Issued-Book Records
INSERT INTO issued_books (book_id, student_id, issue_date, due_date, returned_date) VALUES
(1, 1, '2025-01-10', '2025-01-20', '2025-01-19'),
(2, 2, '2025-01-12', '2025-01-22', '2025-01-21'),
(3, 3, '2025-01-15', '2025-01-25', NULL),
(4, 4, '2025-01-18', '2025-01-28', '2025-01-26'),
(5, 5, '2025-01-20', '2025-01-30', NULL),
(6, 6, '2025-02-01', '2025-02-11', '2025-02-10'),
(7, 7, '2025-02-03', '2025-02-13', NULL),
(8, 8, '2025-02-05', '2025-02-15', '2025-02-14'),
(9, 9, '2025-02-07', '2025-02-17', NULL),
(10, 10, '2025-02-10', '2025-02-20', '2025-02-19'),
(11, 11, '2025-02-12', '2025-02-22', NULL),
(12, 12, '2025-02-14', '2025-02-24', '2025-02-23'),
(13, 13, '2025-02-16', '2025-02-26', NULL),
(14, 14, '2025-02-18', '2025-02-28', '2025-02-27'),
(15, 15, '2025-02-20', '2025-03-01', NULL),
(1, 1, '2025-03-01', '2025-03-11', '2025-03-10'),
(2, 2, '2025-03-03', '2025-03-13', NULL),
(3, 3, '2025-03-05', '2025-03-15', '2025-03-14'),
(4, 4, '2025-03-07', '2025-03-17', NULL),
(5, 5, '2025-03-10', '2025-03-20', '2025-03-19'),
(6, 6, '2025-03-12', '2025-03-22', NULL),
(7, 7, '2025-03-14', '2025-03-24', '2025-03-23'),
(8, 8, '2025-03-16', '2025-03-26', NULL),
(9, 9, '2025-03-18', '2025-03-28', '2025-03-27'),
(10, 10, '2025-03-20', '2025-03-30', NULL),
(11, 11, '2025-04-01', '2025-04-11', '2025-04-10'),
(12, 12, '2025-04-03', '2025-04-13', NULL),
(13, 13, '2025-04-05', '2025-04-15', '2025-04-14'),
(14, 14, '2025-04-07', '2025-04-17', NULL),
(15, 15, '2025-04-10', '2025-04-20', '2025-04-19'),
(1, 2, '2025-04-12', '2025-04-22', NULL),
(2, 3, '2025-04-14', '2025-04-24', '2025-04-23'),
(3, 4, '2025-04-16', '2025-04-26', NULL),
(4, 5, '2025-04-18', '2025-04-28', '2025-04-27'),
(5, 6, '2025-04-20', '2025-04-30', NULL),
(6, 7, '2025-05-01', '2025-05-11', '2025-05-10'),
(7, 8, '2025-05-03', '2025-05-13', NULL),
(8, 9, '2025-05-05', '2025-05-15', '2025-05-14'),
(9, 10, '2025-05-07', '2025-05-17', NULL),
(10, 11, '2025-05-10', '2025-05-20', '2025-05-19'),
(11, 12, '2025-05-12', '2025-05-22', NULL),
(12, 13, '2025-05-14', '2025-05-24', '2025-05-23'),
(13, 14, '2025-05-16', '2025-05-26', NULL),
(14, 15, '2025-05-18', '2025-05-28', '2025-05-27'),
(15, 1, '2025-05-20', '2025-05-30', NULL),
(1, 3, '2025-05-22', '2025-06-01', '2025-05-31'),
(2, 4, '2025-05-24', '2025-06-03', NULL),
(3, 5, '2025-05-26', '2025-06-05', '2025-06-04'),
(4, 6, '2025-05-28', '2025-06-07', NULL),
(5, 7, '2025-05-30', '2025-06-09', NULL);



