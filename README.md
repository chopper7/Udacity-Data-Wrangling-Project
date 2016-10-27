## README

### Introduction
All of the code and other files in this repo were written and prepared for the **[Udacity Data Wrangling course project]**(https://www.udacity.com/course/data-wrangling-with-mongodb--ud032), _**"Wrangle OpenStreetMap Data"**_.

I took the course and prepared the project as part of [Udacity's **Data Analyst Nanodegree** program](https://www.udacity.com/course/data-analyst-nanodegree--nd002?v=a4). The course was originally designed only to be completed using MongoDB, which is a "noSQL" language. Later on, Udacity allowed students to submit SQL-based projects as well, in response to the large demand for SQL skills by employers. Though noSQL intrigues me and is on my list of _"would-be-nice-to-learn"_ subjects, I decided to complete my project using SQL instead.

### Code
Most of the Python scripts in this repo are based in one way or another on starter-code provided via quizzes in the Udacity Data Wrangling course content. Most of the code is written in **Python 2.7.11**, since at the time I took the course (May-June 2016), that is the version of Python being used in the course. As I learn more about Data Science, I would prefer to code in _Python 3.x_.

The OpenStreetMap area I chose to explore was Las Vegas, Nevada, USA. A map file of the area was available for downloading in OSM format (which is basically XML). This repo includes both that OSM file ("lasvegas.osm") and a smaller sample file that is about 1/15 the size of the original OSM file.

### Folders
- _Audit Scripts_: code used to audit the raw data from OpenStreetMap .
- _Report_: contains the markdown of the actual project report I submitted for grading (my grade was "met specifications"; Udacity basically has a pass/fail grading rubric).
- _SQL-Query-Misc_: SQLite3 code I used in exploring and extracting statistics from the database; the database itself comes from the data wrangling, cleaning and transformation of my chosen OSM map file; the XML was transformed to CSV format by Python scripts in root folder, then imported into tables in SQLite3; these queries are pretty rough, typed either from command line or within DB Browser for SQLite.
