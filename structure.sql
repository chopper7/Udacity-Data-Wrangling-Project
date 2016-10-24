-- physical structures

-- building: DONE
-- landuse: DONE
-- place: DONE
-- highway: DONE
-- source: DONE
--

-- ########################################################

-- Building, an example of INCONSISTENY, "yes|no" w/non-bool VALUES
SELECT building, COUNT(*) AS count
FROM (SELECT building FROM node_tags
UNION ALL
SELECT building FROM way_tags)
GROUP BY building HAVING building != ''
ORDER BY count DESC
LIMIT 15;
building         count
---------------  ----------
yes              2364
hangar           175
warehouse        134
roof             70
retail           69
house            53
industrial       43
office           41
entrance         33
residential      16
apartments       12
garage           12
public           3
hut              2
no               2  -- no
-- and cant be explained away by nodes being all Y|N or ways being Y|N:
SELECT DISTINCT building FROM node_tags;
building
-----------
entrance
yes
apartments
office

SELECT COUNT(building) FROM way_tags WHERE building = 'yes';
2305  -- not 2364

-- ########################################################

-- Landuse; Top 20 (there's only 20)
SELECT landuse, COUNT(*) AS count
FROM
(SELECT landuse FROM node_tags
UNION ALL
SELECT landuse FROM way_tags)
GROUP BY landuse HAVING landuse != ''
ORDER BY count DESC
LIMIT 20;
residential           874
grass                 870
retail                292
commercial            160
quarry                154
industrial            85
basin                 79
farmland              36
construction          24
reservoir             23
forest                14
greenfield            12
meadow                5
cemetery              4
farm                  4
brownfield            3
recreation_ground     3
military              2
orchard               2
landfill              1

-- ########################################################

-- Places
SELECT place, COUNT(*) AS count
FROM
(SELECT place FROM node_tags
UNION ALL
SELECT place FROM way_tags)
GROUP BY place HAVING place != ''
ORDER BY count DESC;
place                 count
--------------------  ------
hamlet                34
island                31
suburb                27
neighbourhood         17
town                  7
village               7
city                  3
locality              1

-- ########################################################

-- Top 10 Sources
SELECT source, COUNT(*) AS count
FROM
(SELECT source FROM node_tags
UNION ALL
SELECT source FROM way_tags)
GROUP BY source HAVING source != ''
ORDER BY count DESC
LIMIT 10;
source                                              count
--------------------------------------------------  ----------
Bing                                                18450
Bing;Tiger 2012                                     1005
bing                                                894
Yahoo image; TIGER                                  690
survey                                              472
Tiger;Bing                                          445
Bing; TIGER 2012                                    396
Map of the Shopping Centre                          376
tiger_import_dch_v0.6_20070813                      219
NHD                                                 209


-- sources involving first-hand knowledge could use cleaning up:
SELECT source, COUNT(*) AS count
FROM
(SELECT source FROM node_tags
UNION ALL
SELECT source FROM way_tags)
GROUP BY source HAVING source LIKE '%know%';
source                            count
--------------------------------  ----------
local knowledge;Yahoo image        14
Yahoo image; local knowledge       11
local knowledge                    10
Local Knowledge                    7
knowledge                          1
personal knowledge                 10


-- ########################################################

-- Highways
SELECT highway, COUNT(*) AS count
FROM
(SELECT highway FROM node_tags
UNION ALL
SELECT highway FROM way_tags)
GROUP BY highway HAVING highway != ''
ORDER BY count DESC
LIMIT 15;
highway             count
------------------  ----------
residential         37269
footway             8259
crossing            6821
service             5880
turning_circle      4908
tertiary            1793
path                1366
track               1315
secondary           1113
motorway_link       772
motorway            547
primary             485
traffic_signals     262
proposed            256
unclassified        217  -- proposal to change to 'minor' (2011) but no action yet taken http://wiki.openstreetmap.org/wiki/Proposed_features/highway:minor;
-- also is ambiguous ("he distinction between unclassified and tertiary often causes confusion" -- http://wiki.openstreetmap.org/wiki/Tag:highway%3Dunclassified
-- compared to the sheer volume of other more specific tags, its not a problem in vegas map, imho.


-- highway = *<foot type>
SELECT * --highway, foot, footway --COUNT(*) AS count
FROM
(SELECT highway, NULL 'foot', NULL 'footway' FROM node_tags
UNION ALL
SELECT highway, foot, footway FROM way_tags
WHERE foot != '' OR footway != '')
GROUP BY highway HAVING highway IN ('footway', 'crossing', 'path', 'steps', 'pedestrian');

/* OVERLAPPING, REDUNDANT, NEEDS CLARIFICATION?: */
-- Focus on ways bec ways have k='footway' and k='foot' attribs but nodes don't;
-- output would be large table, so exported to CSV for easier viewing in Excel:
sqlite> .once hwy_foot.csv
sqlite> select way_id, access, bicycle, bridge, foot, footway, highway, name, s
rvice, surface from way_tags where highway IN ('footway', 'path', 'pedestrian',
'crossing', 'steps');
-- "footway" value + "footway" tag and "foot" tag seems REDUNDANT
-- highway 'feet' type values: 'footway', 'crossing', 'path', 'steps', 'pedestrian'
-- highway='footway' and 'foot'='yes' or 'designeated': if it's a footway of course foot woudl be 'yess' (but most "foot" values are NULL when highway= 'footway'; 
-- highway= footway and the footway field go togeehtrer, with footway specifying TYPE
-- of footway (mostly sidewalk and crosssing with a couple outliers, 'C' and 'S').

-- foot field is either 'yes' or 'designated', but almost exclusively when highway = 'path', not 'footway'; but a lot of the same ways are also 'yes' and 'designeated' for the bicycle fiedl too; proposal would be to change the ';path' tag into 2: 'footpath' and 'bikepath' however I can see the value where some users might want to search a simple yes|no for bicylce access or foot access (in which case SUGGESTION clean up the yes|designated terms. OSM wiki asserts using "designated" (not "yes"), meaning a way was specially designated for a certain usage.http://wiki.openstreetmap.org/wiki/Tag:access%3Ddesignated
-- so change the yes's to designated, possibley?
-- alos messy, a few footway fields are = sidewalk where highway = path (instead of footway)
-- Overall imporession is that users by and large have good effort to stick with OSM conventions, but lots of room for clarity.