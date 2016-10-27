-- Exploratory SQL queries: contributor(user)-related
-- A "scratch pad" of queries, most of which did not end up in final project report

/*-------------------------------*/

-- Help from ??? (didn't note the source!):
-- "the UNION ALL needs to have the same number of columns.
-- Try this:"
SELECT AccountID, Date, BarAmount, BarFlag, NULL as FooType FROM Bar 
UNION ALL
SELECT AccountID, Date, NULL, NULL, FooType FROM Foo
-- "That did it, thank you!"
-- "One thing to note for those that may reference this question in the future:"
-- "the order matters!"

/*-------------------------------*/

SELECT DISTINCT user, COUNT(*) AS count
FROM (SELECT uid, user FROM nodes
UNION ALL
SELECT uid, user FROM ways)
GROUP BY user ORDER BY count DESC LIMIT 20;
/*
alimamo|255374
woodpeck_fixbot|83303
nmixter|70222
gMitchellD|52693
robgeb|45572
MojaveNC|34761
nm7s9|17397
balrog-kun|16153
ocotillo|13256
TIGERcnl|12310
abellaofernandez|7637
Glen|7584
SimMoonXP|6831
hno2|6363
DrHog|6138
mitmas|5191
babas56|5034
ryandrake|4973
Chris Bell in California|4882
saikofish|4769
*/


/*------------------------------*/
