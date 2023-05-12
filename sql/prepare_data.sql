--- Create table
CREATE TABLE IF NOT EXISTS items (
    id serial PRIMARY KEY, 
    title VARCHAR (50), 
    description VARCHAR (255), 
    completed BOOL
);

--- Fill up table with test data
INSERT INTO items(title, description, completed) 
VALUES 
('Prepare database', 'Prepare database with docker image', True),
('Prepare docker image', 'Docker image creation', True),
('API implementation', 'Implement REST API', True),
('Unit tests', 'Implement unit tests', True),
('Code refactoring', 'Find bugs and fix them', False);