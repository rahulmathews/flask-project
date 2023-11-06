LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS i, row.Title AS t, row.Description AS d, row.Year AS y, row.Runtime AS r, row.Rating AS rt, row.Votes AS v, row.Revenue AS rv
WHERE rv IS NOT NULL
MERGE (:Movie {movie_id: i, title:t, description:d, year:y, runtime:r, rating:rt, votes: v, revenue:rv});

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS i, row.Title AS t, row.Description AS d, row.Year AS y, row.Runtime AS r, row.Rating AS rt, row.Votes AS v, row.Revenue AS rv
WHERE rv IS NULL
MERGE (m:Movie {movie_id: i, title:t, description:d, year:y, runtime:r, rating:rt, votes: v})
ON CREATE SET m.revenue = NULL;

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS t, SPLIT(row.Actors,',') AS a, SPLIT(row.Director, ',') as d, SPLIT(row.Genre, ',') as g
UNWIND t AS t1
UNWIND a AS a1
UNWIND d as d1
UNWIND g as g1

WITH *, trim(a1) AS a2, trim(d1) as d2, trim(g1) as g2
MERGE(p:Person {name: a2})
MERGE(p1:Person {name: d2})
MERGE(:Genre {genre: g2});


LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS t, SPLIT(row.Actors,',') AS a, SPLIT(row.Director, ',') as d, SPLIT(row.Genre, ',') as g
UNWIND t AS t1
UNWIND a AS a1
UNWIND d as d1
UNWIND g as g1
WITH *, trim(a1) AS a2, trim(d1) as d2, trim(g1) as g2
MATCH(m:Movie{movie_id:t1}),(p:Person{name:a2})
MERGE(p)-[:ACTED_IN]->(m);
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS t, SPLIT(row.Actors,',') AS a, SPLIT(row.Director, ',') as d, SPLIT(row.Genre, ',') as g
UNWIND t AS t1
UNWIND a AS a1
UNWIND d as d1
UNWIND g as g1
WITH *, trim(a1) AS a2, trim(d1) as d2, trim(g1) as g2
MATCH(m:Movie{movie_id:t1}),(p:Person{name:d2})
MERGE(p)-[:DIRECTED]->(m);

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS t, SPLIT(row.Actors,',') AS a, SPLIT(row.Director, ',') as d, SPLIT(row.Genre, ',') as g
UNWIND t AS t1
UNWIND a AS a1
UNWIND d as d1
UNWIND g as g1
WITH *, trim(a1) AS a2, trim(d1) as d2, trim(g1) as g2
MATCH(m:Movie{movie_id:t1}), (g3:Genre{genre:g2})
MERGE(m)-[:IN]->(g3);