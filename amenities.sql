-- amenity: DONE
-- tourism: DONE
-- cuisine: DONE 
-- leisure: DONE
-- parking: DONE
-- shop:    DONE
-- 

-- Tourism 
SELECT tourism, COUNT(*) AS count
FROM 
(SELECT tourism FROM node_tags
UNION ALL
SELECT tourism FROM way_tags)
GROUP BY tourism
ORDER BY count DESC;
/* tourism               count
--------------------  ----------
                      754093
hotel                 80
attraction            51
picnic_site           26
museum                14
motel                 12
viewpoint             10
caravan_site          9
information           9
artwork               7
camp_site             5
Salon                 1
VINTAGE               1
guest_house           1
hostel                1
zoo                   11*/


-- ############################################

-- amenity

-- Top 20
SELECT amenity, COUNT(*) AS count 
FROM 
(SELECT amenity FROM node_tags 
WHERE amenity != '' 
UNION ALL
SELECT amenity FROM way_tags 
WHERE amenity != '') 
GROUP BY amenity 
ORDER BY count DESC
LIMIT 20;
amenity                    count
-------------------------  ----------
parking                    586
school                     526
place_of_worship           363
fountain                   265
restaurant                 126
fast_food                  88
fire_station               68
hospital                   68
fuel                       61
post_office                59
shelter                    50
toilets                    41
public_building            40
bar                        38
cafe                       35
bank                       24
casino                     24
theatre                    24
library                    22
swimming_pool              20


SELECT amenity FROM node_tags
UNION
SELECT amenity FROM way_tags
ORDER BY amenity;
/*adult day care
antiques
arts_centre
atm
bank
bar
bat
bbq
bench
bicycle_parking
bicycle_rental
bus_station
cafe
car_rental
car_wash
casino           -- Gambling
cinema
college
concierge
courthouse
dentist
doctors
drinking_water
fast_food
finish line         -- ???
fire_station
fitness_center
flower shop
food_court
fountain
fuel
furniture
grave_yard
hospital
hotel
ice_cream
kindergarten
koolsville tattoo   -- ???
library
lounge
mall
nightclub
parking            -- FURTHER INVESTIGATION FOR OVERLAPPING DATA
parking_entrance   -- FURTHER INVESTIGATION FOR OVERLAPPING DATA
pharmacy
place_of_worship
police
post_box
post_office
prison
pub
public_building
recycling
restaurant
school
shelter
smog               -- ???
social_facility
spa
swimming_pool
swingerclub
taxi
telephone
theatre
toilets
townhall
university
veterinary
waste_basket
whirlpool*/

-- ==============================

-- sqlite> .read qtemp.sql
SELECT amenity, COUNT(*) AS count
FROM (SELECT amenity FROM node_tags
WHERE amenity != ''
UNION ALL
SELECT amenity FROM way_tags
WHERE amenity != '')
GROUP BY amenity ORDER BY count DESC;
/*parking|586
school|526
place_of_worship|363
fountain|265            -- Lots of fountains.
restaurant|126
fast_food|88
fire_station|68
hospital|68
fuel|61
post_office|59
shelter|50
toilets|41
public_building|40
bar|38
cafe|35
bank|24
casino|24               -- there are more in reality
theatre|24
library|22
swimming_pool|20
police|15
bench|14
telephone|12
pharmacy|11
pub|11
atm|8
car_wash|7
bbq|6
townhall|6
university|6
bus_station|5
car_rental|5
college|5
parking_entrance|5
prison|5
recycling|5
bicycle_parking|3
drinking_water|3
hotel|3
nightclub|3
taxi|3
arts_centre|2
cinema|2
courthouse|2
dentist|2
fitness_center|2
grave_yard|2
ice_cream|2
post_box|2
veterinary|2
adult day care|1
antiques|1
bat|1
bicycle_rental|1
concierge|1
doctors|1
finish line|1
flower shop|1
food_court|1
furniture|1
kindergarten|1
koolsville tattoo|1
lounge|1
mall|1
smog|1
social_facility|1
spa|1
swingerclub|1  
waste_basket|1
whirlpool|1*/

-- smog? somebody has a sarcastic sense of humor
select node_id, amenity, name from node_tags where amenity = 'smog';
/*
node_id|amenity|name
2462473481|smog|Smog
*/
select lat, lon from nodes where id = 2462473481;
/*lat|lon
36.1295409|-115.1034374
Apparently refers a real place of business
ref: http://www.yelp.com/biz/mf-smog-las-vegas*/


-- ##############################################

-- Queries regarding: Las Vegas biggest industry
SELECT amenity, tourism, name FROM node_tags
WHERE amenity = 'casino'
UNION ALL
SELECT amenity, tourism, name FROM way_tags
WHERE amenity = 'casino'
ORDER BY name;
/*amenity     tourism     name
----------  ----------  ----------------------------------------
casino
casino      hotel       Aria Resort & Casino
casino      hotel       Bally's Hotel and Casino
casino      hotel       Bellagio Hotel and Casino
casino                  Bill's Gamblin' Hall & Saloon
casino      hotel       Caesars Hotel and Casino
casino      hotel       Circus Circus Las Vegas Hotel and Casino
casino                  Club Fortune Casino
casino      hotel       Excalibur Hotel and Casino
casino      hotel       Gold Coast Hotel & Casino
casino      hotel       Hard Rock Hotel and Casino
casino      hotel       Imperial Palace Hotel and Casino
casino      hotel       Luxor Hotel and Casino
casino      hotel       MGM Grand Hotel and Casino
casino      hotel       Mandalay Bay Hotel and Casino
casino      hotel       Mirage Hotel and Casino
casino      hotel       Monte Carlo Hotel and Casino
casino      hotel       New York New York Hotel and Casino
casino      hotel       Palms Casino Resort
casino      hotel       Planet Hollywood Hotel and Casino
casino                  Rampart Casino
casino      hotel       Stratosphere Hotel and Casino
casino      hotel       Treasure Island Hotel and Casino
casino      hotel       Venetian Hotel and Casino */

-- 3 hotels under 'amenity', but not tagged as 'casino'
SELECT * FROM 
(SELECT amenity, tourism, name FROM node_tags 
WHERE amenity = 'hotel' 
UNION ALL
SELECT amenity, tourism, name FROM way_tags 
WHERE amenity = 'hotel') 
LIMIT 20; 
/* amenity        tourism     name
------------- ----------  -----------------------
hotel
hotel                     SLSouth Las Vegas (Formerly the Sahara)
hotel                     Golden Spike */


-- ##############################################

-- Cuisine

SELECT cuisine, COUNT(*) AS count
FROM 
(SELECT cuisine FROM node_tags WHERE cuisine != ''
UNION ALL
SELECT cuisine FROM way_tags WHERE cuisine != '')
GROUP BY cuisine
ORDER BY count DESC
LIMIT 20;
cuisine                    count
-------------------------  ----------
burger                     35
mexican                    14
american                   9
coffee_shop                6
pizza                      6
chinese                    5
italian                    5
japanese                   5
chicken                    4
thai                       4
sandwich                   3
steak_house                2
American                   1
American Bistro            1
Eastern European           1
Hawaiian                   1
Marocco                    1
asian                      1
bagel_shop                 1
bavarian                   1

-- ##############################################

--shop
SELECT shop, COUNT(*) AS count
FROM
(SELECT shop FROM node_tags
UNION ALL
SELECT shop FROM way_tags)
GROUP BY shop HAVING shop != ''
ORDER BY count DESC;
shop              count
----------------  -----------
supermarket       45
clothes           36
doityourself      26
convenience       25
yes               14        -- yes (LACK SPECIFICITY)
car_repair        8
department_store  7
mall              7
shoes             6
alcohol           5
chemist           5         -- Non-local term
hairdresser       5
car               4
garden_centre     4         -- Non-local term
bakery            3
electronics       3
gift              3
jewelry           3
sports            3
bicycle           2
books             2
hifi              2
kiosk             2
optician          2
vintage           2
1Stop Auto LLc    1         -- business name
Quilt             1
Vintage           1
antique           1         -- REDUNDANT
antiques          1         -- REDUNDANT
artistantiques    1         -- REDUNDANT
beauty            1
betting           1
boutique          1
computer          1
confectionery     1
estate_agent      1
gambler           1
motorcycle        1
musical_instrume  1
outdoor           1
pawnbroker        1
pharmacy          1
stationery        1
tattoo            1
ticket            1
tyres             1         -- Non-local term
uppity furniture  1         -- business name
watch             1
wharehouse        1



-- ##############################################
-- leisure
SELECT leisure, COUNT(*) AS count
FROM (SELECT leisure FROM node_tags
UNION ALL
SELECT leisure FROM way_tags)
GROUP BY leisure HAVING leisure != ''
ORDER BY count DESC;
LIMIT 10;
