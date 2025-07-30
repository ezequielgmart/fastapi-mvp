CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY, -- Cambiado de VARCHAR(200) a VARCHAR(255) para consistencia con IDs hash
    username VARCHAR(200) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE authors (
    author_id VARCHAR(255) PRIMARY KEY, -- Cambiado de SERIAL a VARCHAR(255)
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50)
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY, -- Cambiado de SERIAL a VARCHAR(255)
    genre_name VARCHAR(200) NOT NULL
);

CREATE TABLE books (
    book_id VARCHAR(255) PRIMARY KEY, -- Cambiado de SERIAL a VARCHAR(255)
    title VARCHAR(255) NOT NULL,
    release_date DATE
);

CREATE TABLE book_authors (
    author_id VARCHAR(255) NOT NULL, -- Cambiado de INT a VARCHAR(255)
    book_id VARCHAR(255) NOT NULL,   -- Cambiado de INT a VARCHAR(255)
    PRIMARY KEY (author_id, book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

CREATE TABLE book_genres (
    genre_id INT NOT NULL, -- Cambiado de INT a VARCHAR(255)
    book_id VARCHAR(255) NOT NULL,   -- Cambiado de INT a VARCHAR(255)
    PRIMARY KEY (genre_id, book_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);
