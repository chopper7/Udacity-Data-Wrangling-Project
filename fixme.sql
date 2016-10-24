-- "FIXME"

-- k="fixme" is used for human-entered, not automated; "to express that the mapper thinks there is an error" (http://wiki.openstreetmap.org/wiki/Key:fixme)

SELECT FIXME, type, COUNT(*) AS count
FROM
(SELECT FIXME, type FROM node_tags
UNION ALL
SELECT FIXME, type FROM way_tags)
GROUP BY FIXME HAVING FIXME != ''
ORDER BY count DESC;
-- Mostly involving ways, especially bicycle questions
FIXME                                                         type    count
------------------------------------------------------------  ------  ------
are bikes allowed?                                            way     148
verfiy bicycle=yes                                            way     103
check lanes                                                   way     50
Divided highway                                               way     45
verify bicycle=yes                                            way     25
dual carriageway                                              way     14
check lanes; are bikes allowed?                               way     11
Divided highway.                                              way     8
Does the old_ref apply to the entire length?                  way     7
reconfigured?                                                 way     6
Temporary construction road.                                  way     4
verify entrance type                                          node    4
Old alignment being replaced                                  way     3
Continue                                                      node    2
This way will go oneway when other side is completed.         way     2
yes                                                           way     2
Area Needs Checking                                           way     1
Is this really a park & sports center?                        way     1
Landuse shouldnt be attached to centerlines but follow actu   way     1
Remove this road when adjacent ramp is completed.             way     1
access=private?                                               way     1
check name                                                    way     1
inaccurate                                                    way     1
name needs checking                                           way     1
need subdivision                                              way     1
not sure which shop type                                      way     1
old_ref?                                                      node    1
ref?                                                          node    1
-- Questions about bicycle usage predominate
-- 4 of the top 7
-- and 287 out of 446 (64%):
SELECT SUM(FIXME LIKE '%bi%') FROM
(SELECT FIXME FROM node_tags
UNION ALL
SELECT FIXME FROM way_tags);
287

SELECT SUM(FIXME != '') FROM
(SELECT FIXME FROM node_tags
UNION ALL
SELECT FIXME FROM way_tags);
446
