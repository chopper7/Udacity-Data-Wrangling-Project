-- Exploratory SQL queries on natural features in map data
-- A "scratch pad" of queries, most of which did not end up in final project report

SELECT DISTINCT natural, waterway, water, name
FROM way_tags
WHERE natural like '%w%';
/*natural     waterway       water                      name
----------  -------------  -------------------------  --------------------
water                  --THIS IS HARDLY "natural"-->  Fountains of Bellagio
water                                                 Tule Springs
water
water                                                 Lake Sahara
wood
water                                                 Lake Lindsey
water                                                 Lake Jacqueline
wetland
water                                                 Sirens' Cove
water                                                 Mulberry Lake
water                                                 Cottonwood Lake
water                                                 Desert Willow Lake
water                      reservoir
water                      lake;pond
water                                                 Mouse's Tank
water                      lake;pond                  South Senator Tank
water                                                 Roaring Rapids
water                      stream;river
water                                                 Big Sand Bar
water                                                 Ringbolt Rapids
water                                                 Cross Current Rapids
water                                                 Shallow Rapids
water                                                 Indian Rapids
water                                                 Horseshoe Rapids
water                                                 Cranes Nest Rapids
wetlands
wetland                                               Petroglyph Wash
water                                                 Lake of Dreams
water                                                 Harris Springs
water_park  river
water                      pond                       Bird Viewing Pond #1
water                      pond                       Bird Viewing Pond #3
water                      pond                       Bird Viewing Pond #4
water                      pond                       Bird Viewing Pond #5
water                      pond                       Bird Viewing Pond #6
water                      pond                       Bird Viewing Pond #7
water                      pond                       Bird Viewing Pond #8
water                      pond*/

-- nodes, the "k":"natural" is blank while waterway is filled in
SELECT DISTINCT natural, waterway, name
FROM node_tags
WHERE waterway != '';
/* natural     waterway       name
----------  -------------  -------------------------
            weir
            rapids         Big Sand Bar
            rapids         Cranes Nest Rapids
            rapids         Cross Current Rapids
            rapids         Indian Rapids
            rapids         Ringbolt Rapids
            rapids         Roaring Rapids
            rapids         Shallow Rapids
            dock           Lake Mead Marina
            rapids         Big Sand Bar Rapids
            rapids         Horseshoe Rapids
            rapids         Boulder Rapids (historica
            dam            Mill Number 1-Pond A Dam
            dam            Mill Number 2-Pond A Dam
            dam            Mill Number 2-Pond B Dam
            dam            Mill Number 2-Pond C Dam
            dam            Mill Number 2-Pond D Dam
            dam            Mill Number 2-Pond East D
            dam            Mill Number 1-Pond B Dam
            dam            Spent Leaching Liquor Pon
            dam            Spent Leaching Liquor Pon
            dam            Miscellaneous Waste Pond
            dam            Spent Caustic Liquor Pond
            dam            Miscellaneous Waste Pond
            dam            Honeybee Dam
            dock           Temple Bar Boat Anchorage
            dock           Temple Bar Marina
            rapids         Rocky Rapids
            waterfall*/


SELECT DISTINCT natural FROM node_tags ORDER BY natural;
/* natural
-------------
bay
beach
cave_entrance
cliff
peak
spring          -- WATER
tree
volcano*/


SELECT DISTINCT natural FROM way_tags ORDER BY natural;
-- just searching for 'water' in natural wasn't enough, since there are wetlands, and a spring in node tags.
/* natural
-------------
beach
cliff
desert
heath
mud
sand
scree
scrub
water
water_park
wetland
wetlands
wood */


-- ##############################################

sqlite> SELECT natural, COUNT(*) AS count FROM node_tags WHERE natural != "" GROUP BY natural ORDER BY count DESC;
natural               count
--------------------  ------------
tree                  139
bay                   119
peak                  83
spring                63
beach                 9
cliff                 8
cave_entrance         1
volcano               1
-- "volcano"... are there volcanoes in or near LV?
.mode list
SELECT node_id, name, natural FROM node_tags WHERE natural = "volcano";
305856965|Black Cone|volcano
sqlite> select lat, lon from nodes where id = 305856965;
lat|lon
36.148767|-114.9379518
-- Yes, nearby those coords on openstreetmap.org is "Lava Butte":
sqlite> SELECT node_id, name, ele, natural FROM node_tags WHERE name LIKE "%Butte%";
/* node_id|name|ele|natural
357546463|Delmar Butte|469|peak
357547617|Lava Butte|863|peak
357550151|Twin Buttes|2193|peak
357554890|Garrett Butte|1164|peak
357561304|Mineral Buttes|1078|peak
359242740|Black Butte|738|peak */

