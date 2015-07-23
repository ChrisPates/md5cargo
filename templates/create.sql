CREATE TABLE dataset (
	checksum HEX, 
	type char, 
	num_files int, 
	num_dirs int, 
	filesize int, 
	total_num_files int, 
	total_filesize int, 
	name text, 
	snapshot text, 
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tmp (
	checksum HEX, 
	type char, 
	num_files int, 
	num_dirs int, 
	filesize int, 
	total_num_files int, 
	total_filesize int, 
	name text 
);

CREATE VIEW latest AS
SELECT	checksum,
	type,
	num_files,
	num_dirs,
	filesize,
	total_num_files,
	total_filesize,
	name,
	snapshot,
	MAX(created) AS created
FROM	dataset
GROUP BY name
HAVING checksum != 0x0;

CREATE VIEW duplicate AS
SELECT	*
FROM	tmp 
INNER JOIN latest ON 
	tmp.checksum = latest.checksum AND
	tmp.name = latest.name;

CREATE VIEW snapshots AS
SELECT	snapshot,
	MAX(created) AS created
FROM	dataset
GROUP BY snapshot;

CREATE VIEW current AS
SELECT	*
FROM	latest
WHERE	checksum NOT like '#%';

CREATE VIEW deletions AS
SELECT	0x0 AS checksum,
	type,
	num_files,
	num_dirs,
	filesize,
	total_num_files,
	total_filesize,
	name
FROM	latest
WHERE	latest.name NOT IN (
	SELECT name 
	FROM tmp);

CREATE VIEW mkdir AS
SELECT	snapshot,
	name
FROM	latest
WHERE	type='d';

CREATE VIEW ln AS
SELECT 	snapshot,
	name
FROM	latest
WHERE	type='-';
