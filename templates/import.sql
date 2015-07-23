DROP TABLE IF EXISTS tmp;
create table tmp (checksum HEX, type char, num_files int, num_dirs int, filesize int, total_num_files int, total_filesize int, name text);
.separator "\t"
.import MANIFEST_FILE tmp

-- Clean up: 
-- remove headers
-- insert deletions
-- remove duplicates
DELETE FROM tmp WHERE type IS NULL;
DELETE FROM tmp WHERE name ='name';
INSERT INTO tmp SELECT * FROM deletions;
DELETE FROM tmp WHERE tmp.name IN (SELECT name FROM duplicate);

-- Add snapshot metadata
ALTER TABLE tmp ADD COLUMN snapshot text;
ALTER TABLE tmp ADD COLUMN created TIMESTAMP;
UPDATE tmp SET created = "MANIFEST_TIMESTAMP";
UPDATE tmp SET snapshot = "MANIFEST_SNAPSHOT";

-- Insert into master
INSERT INTO dataset SELECT * FROM tmp;

-- Clean Up
DROP TABLE tmp;
