
# all database creation
DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) ,
    phone VARCHAR(50) ,
    linkedin VARCHAR(255),
    career_span INT,
    resume_file VARCHAR(255)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS education (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    degree VARCHAR(255),
    field_of_study VARCHAR(255),
    institution VARCHAR(255),
    location VARCHAR(255),
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    cgpa FLOAT,
    percentage FLOAT,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS experience (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    company VARCHAR(255),
    designation VARCHAR(255),
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    responsibilities TEXT,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    skill VARCHAR(255),
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS awards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT,
    award VARCHAR(255),
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
) ENGINE=InnoDB;
"""
