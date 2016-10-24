-- Addresses


-- This puts all the addresses from both tables together:
.once addresses.csv
SELECT * FROM
(SELECT type, addr_housename, addr_housenumber, addr_street, addr_city, addr_postcode, addr_state 
FROM node_tags WHERE address = 'addressed'
UNION ALL
SELECT type, addr_housename, addr_housenumber, addr_street, addr_city, addr_postcode, addr_state 
FROM way_tags WHERE address = 'addressed');


 -- ############################
 
-- States
SELECT addr_state, COUNT(*) AS count
FROM
(SELECT addr_state FROM node_tags WHERE address = 'addressed'
UNION ALL
SELECT addr_state FROM way_tags WHERE address = 'addressed')
GROUP BY addr_state
ORDER BY count DESC;
addr_state    count
------------  ------
NV            519
              240  -- missing values
AZ            39
Nevada        2    -- NEED TO CLEAN
CA            1

 -- ############################
 
-- Cities
SELECT addr_city, COUNT(*) AS count
FROM
(SELECT addr_city FROM node_tags WHERE address = 'addressed'
UNION ALL
SELECT addr_city FROM way_tags WHERE address = 'addressed')
GROUP BY addr_city
ORDER BY count DESC;
addr_city     count
------------  ------
              676
Henderson     63
Las Vegas     60
Boulder City  2

-- "place" and "name" as city; offers room to fill in addr_city
-- types of places
SELECT place, COUNT(*) AS count
FROM
(SELECT place FROM node_tags --WHERE place IN ('city', 'town', 'village')
UNION ALL
SELECT place FROM way_tags) --WHERE place IN ('city', 'town', 'village')
GROUP BY place HAVING place != ''
ORDER BY count DESC;
place            count
---------------  --------
hamlet           34
island           31
suburb           27
neighbourhood    17
town             7
village          7
city             3
locality         1

-- Some names of places:
SELECT * FROM
(SELECT place, name FROM node_tags WHERE place IN ('city', 'town', 'village')
UNION
SELECT place, name FROM way_tags) WHERE place IN ('city', 'town', 'village')
ORDER BY place;
place            name
---------------  -------------------
city             Henderson
city             Las Vegas
city             North Las Vegas
town             Boulder City
town             Enterprise
town             Jean
town             Moapa Valley
town             Summerlin
town             Whitney
town             Winchester
village          Blue Diamond
village          Corn Creek
village          Goodsprings
village          Logandale
village          Mountain Springs
village          Overton
village          Temple Bar

-- ###########################

-- Postal codes that aren't solely numeric:
SELECT addr_postcode, addr_city FROM node_tags 
WHERE address = 'addressed' AND addr_postcode GLOB '*[^0-9]*'
UNION ALL
SELECT addr_postcode, addr_city FROM way_tags 
WHERE address = 'addressed' AND addr_postcode GLOB '*[^0-9]*';
addr_postcode    addr_city
---------------  -------------
89109-1907                    -- node
NV 89117         Las Vegas    -- node; (missed during Python auditing)
NV 89123         Las Vegas    -- node; (missed during Python auditing)
Nevada 89113                  -- way

-- could also have retrieved id's of elements:
SELECT * FROM
(SELECT node_id, NULL 'way_id', addr_postcode, addr_city FROM node_tags 
WHERE address = 'addressed' AND addr_postcode GLOB '*[^0-9]*'
UNION ALL
SELECT NULL 'node_id', way_id, addr_postcode, addr_city FROM way_tags 
WHERE address = 'addressed' AND addr_postcode GLOB '*[^0-9]*')
node_id|way_id|addr_postcode|addr_city
1700469005||89109-1907|
2540047619||NV 89117|Las Vegas
2572969955||NV 89123|Las Vegas
  |27750647|Nevada 89113|

-- NOTE: GO BACK AND WRITE POSTAL CLEANING CODE FOR IN PYTHON
--   UPDATE: code added and works.



-- ########################################################
--          O L D ,  b e l o w
-- ########################################################

-- Cities

sqlite> select place, name, count(*) as count from node_tags where place != ''
roup by place order by count desc;
place            name             count
---------------  ---------------  ----------
hamlet           Downtown         34
island           Beehive Island   31
suburb           Green Valley Ra  27
neighbourhood    Water Street Di  8
town             Summerlin        7
village          Temple Bar       7
city             North Las Vegas  3
locality         St. Thomas       1

sqlite> select place, name, count(*) as count from way_tags where place != '' g
oup by place order by count desc;
place            name             count
---------------  ---------------  ----------
neighbourhood    Terragona Est    9


sqlite> select distinct addr_city from way_tags;
addr_city
---------------

Las Vegas
Boulder City
Henderson


sqlite> select distinct addr_city from node_tags;
addr_city
---------------

Las Vegas
Henderson

-- ############################################
 

-- Postal codes that aren't 5-digit:
SELECT DISTINCT addr_postcode FROM node_tags
WHERE addr_postcode GLOB '*[^0-9]*';
89109-1907
NV 89117
NV 89123
-- whole records:
sqlite> SELECT * FROM node_tags
   ...> WHERE addr_postcode GLOB '*[^0-9]*';
1700469005|node|addressed|||3341|89109-1907||Industrial Road||||||||||||||||||||
|||||||Charleston Auto Parts|||||||||doityourself|local knowledge|||
2540047619|node|addressed|Las Vegas||7942|NV 89117||West Sahara Avenue||||||||||
|||||||||||||||||Haeran Dempsey Real Estate|||||||||||||
2572969955|node|addressed|Las Vegas|Ste 404|7437|NV 89123||South Eastern Avenue|
||||||||||||||||||||||||||inlineVision|||||||||||||

-- and,
SELECT DISTINCT addr_postcode FROM way_tags
WHERE addr_postcode GLOB '*[^0-9]*';
Nevada 89113
-- whole records
SELECT * FROM way_tags
WHERE addr_postcode GLOB '*[^0-9]*';
27750647|way|addressed||||6355|Nevada 89113||South Buffalo Drive||||||||||||||||
||commercial|||IGT||||||||||||||||||||||||||||||||||||||||||||||||


-- ############################################

-- shortage of addr_ data filled-in

SELECT DISTINCT addr_housename FROM way_tags;
addr_housename
-------------------------

Dag Spring 2
County of Clark (Administ
Former City Hall
The Coffee Cup
302 East Carson -- should be in addr_housenumber, addr_street
Bank of America Plaza
City Centre Place
RTC of Southern Nevada
Mob Museum
Whole Foods Market

-- in node_tags we also see inconsistencies, lack of standardization:
SELECT DISTINCT addr_housename FROM node_tags;
addr_housename
-------------------------

Hughes Center
Horizon Web Marketing
US Bank Building
Bonneville Transit Center
Suite 120 -- where should "Suite" data go?
Ste 404

-- ############################################

-- HIGHWAYS

-- AND "service":
SELECT highway, service, COUNT(*) AS count FROM way_tags
WHERE service = "" GROUP BY service, highway ORDER BY count DESC;
highway          service          count
---------------  ---------------  ----------
service          parking_aisle    2286
service          driveway         1317
service          alley            52
                 spur             45
service          drive-through    6
                 yard             5 -- shouldn't these nulls be filled-
                 siding           4 -- in with "service" for highway?
                 alley            2
track            alley            2
motorway_link    driveway         2
secondary_link   parking_aisle    2

SELECT highway, service, COUNT(*) AS count FROM way_tags 
WHERE highway = 'service' GROUP BY service, highway ORDER BY count DESC;
highway          service          count
---------------  ---------------  ----------
service          parking_aisle    2286
service                           2219
service          driveway         1317
service          alley            52
service          drive-through    6

