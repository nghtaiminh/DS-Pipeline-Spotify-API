DROP TABLE IF EXISTS played_song;
DROP TABLE IF EXISTS song_artists;
DROP TABLE IF EXISTS time;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS audio_feature;
DROP TABLE IF EXISTS song;
DROP TABLE IF EXISTS album;



-- CREATE TABLES
CREATE TABLE album (
	album_id TEXT PRIMARY KEY,
	album_name TEXT NOT NULL,
	album_type TEXT NOT NULL,
	popularity SMALLINT,
	release_year SMALLINT,
	external_url TEXT
);

-- Create Songs Table 
CREATE TABLE song (
	song_id TEXT PRIMARY KEY,
	song_name TEXT NOT NULL,
	album_id TEXT NOT NULL,
	duration_ms INTEGER NOT NULL,
	popularity SMALLINT,
	external_url TEXT,
	FOREIGN KEY (album_id) REFERENCES album(album_id)
);

-- Create Artists Table 
CREATE TABLE artist (
	artist_id TEXT PRIMARY KEY,
	artist_name TEXT NOT NULL,
	followers INTEGER,
	popularity SMALLINT,
	external_url TEXT
);

-- Create Time Table 
CREATE TABLE time (
	start_time TIMESTAMP PRIMARY KEY,
	time TEXT NOT NULL,
	day SMALLINT NOT NULL,
	month SMALLINT NOT NULL,
	year SMALLINT NOT NULL,
	weekday SMALLINT NOT NULL
);

-- Create AudioFeatures Table 
CREATE TABLE audio_feature (
	song_id TEXT PRIMARY KEY,
	dancibility NUMERIC(4, 3) NOT NULL,
	energy NUMERIC(7, 3) NOT NULL,
	loudness NUMERIC(7, 3) NOT NULL,
	speechiness NUMERIC(7, 3) NOT NULL,
	acousticness NUMERIC(7, 3) NOT NULL,
	instrulmentalness NUMERIC(7, 3) NOT NULL,
	liveness NUMERIC(7, 3) NOT NULL,
	valance NUMERIC(7, 3) NOT NULL,
	tempo NUMERIC(7, 3) NOT NULL,
	FOREIGN KEY (song_id) REFERENCES Song(song_id)
);


CREATE TABLE song_artists (
	song_id TEXT,
	artist_id TEXT,
	PRIMARY KEY (song_id, artist_id),
	FOREIGN KEY (song_id) REFERENCES song(song_id),
	FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
);

-- Create PlayedSong Table 
CREATE TABLE played_song (
	played_song_id TEXT PRIMARY KEY,
	song_id TEXT NOT NULL,
	album_id TEXT NOT NULL,
	played_at TIMESTAMP NOT NULL,
	FOREIGN KEY (song_id) REFERENCES song(song_id),
	FOREIGN KEY (album_id) REFERENCES album(album_id),
	FOREIGN KEY (played_at) REFERENCES time(start_time)
);
