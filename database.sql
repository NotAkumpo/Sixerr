-- To run this script: source C:\Users\<user>\Documents\GitHub\Sixerr\database.sql

-- For skill database
-- Query: SELECT * FROM sixerrapp_skill;
-- Delete: DELETE FROM sixerrapp_skill WHERE;
-- Insert: INSERT INTO sixerrapp_skill (skill_name, image, popularity) VALUES ('pickleball', 'images/skills/pickleball.jpeg', 1);

-- For user database
-- Query: SELECT username, first_name, last_name, role, skill_id, popularity, rating, hourly_rate, image, email, dummy FROM sixerrapp_user;
-- Delete: DELETE FROM sixerrapp_user WHERE;
-- Insert: INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Chris', 'Paul', 'cp3', 'cp3@gmail.com', 'ThisIsMyPassword', 'mentor', 'pickleball', 0, 0, 1, '2025-03-10', 'images/users/chris.jpg', 1, 1, 4.5, 20.50);

-- Just some random data for skill
INSERT INTO sixerrapp_skill (skill_name, image, popularity) VALUES ('pickleball', 'images/skills/pickleball.jpeg', 1);
INSERT INTO sixerrapp_skill (skill_name, image, popularity) VALUES ('basketball', 'images/skills/basketball.jpeg', 2);
INSERT INTO sixerrapp_skill (skill_name, image, popularity) VALUES ('capoeira', 'images/skills/capoeira.jpg', 3);
INSERT INTO sixerrapp_skill (skill_name, image, popularity) VALUES ('dancing', 'images/skills/dancing.jpg', 4);
INSERT INTO sixerrapp_skill (skill_name, image, popularity) VALUES ('animefighting', 'images/skills/default.jpg', 5);

-- Just some random data for user
INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Chris', 'Paul', 'cp3', 'cp3@gmail.com', 'ThisIsMyPassword', 'mentor', 'pickleball', 0, 0, 1, '2025-03-10', 'images/users/chris.jpg', 1, 1, 4.5, 20.50);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Donovan', 'Mitchell', 'dm', 'dm@gmail.com', 'ThisIsMyPassword', 'mentor', 'pickleball', 0, 0, 1, '2025-03-10', 'images/users/donovan.jpg', 1, 2, 3.7, 18.00);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Ja', 'Morant', 'jm', 'jm@gmail.com', 'ThisIsMyPassword', 'mentor', 'pickleball', 0, 0, 1, '2025-03-10', 'images/users/ja.jpg', 1, 3, 4.2, 19.75);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Jrue', 'Holiday', 'jh', 'jh@gmail.com', 'ThisIsMyPassword', 'mentor', 'pickleball', 0, 0, 1, '2025-03-10', 'images/users/jh.jpg', 1, 4, 4.8, 30.50);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Kevin', 'Durant', 'kd', 'kd@gmail.com', 'ThisIsMyPassword', 'mentor', 'pickleball', 0, 0, 1, '2025-03-10', 'images/users/kevin.jpg', 1, 5, 4.1, 15.99);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Luka', 'Doncic', 'ld', 'ld@gmail.com', 'ThisIsMyPassword', 'mentor', 'pickleball', 0, 0, 1, '2025-03-10', 'images/users/luka.jpg', 1, 6, 3.2, 9.99);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Victor', 'Wembanyama', 'vw', 'vw@gmail.com', 'ThisIsMyPassword', 'mentor', 'capoeira', 0, 0, 1, '2025-03-10', 'images/users/victor.jpg', 1, 7, 2.1, 5.00);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Paolo', 'Banchero', 'pb', 'pb@gmail.com', 'ThisIsMyPassword', 'mentor', 'dancing', 0, 0, 1, '2025-03-10', 'images/users/paolo.jpg', 1, 8, 5.0, 1.50);

INSERT INTO sixerrapp_user (first_name, last_name, username, email, password, role, skill_id, is_superuser, is_staff, is_active, date_joined, image, dummy, popularity, rating, hourly_rate) VALUES ('Jogo', 'Sukuna', 'js', 'js@gmail.com', 'ThisIsMyPassword', 'mentor', 'animefighting', 0, 0, 1, '2025-03-10', 'images/users/default.jpg', 1, 9, 0.2, 100.00);
