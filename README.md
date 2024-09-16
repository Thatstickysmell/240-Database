# 240-Database
Zach Kessler

Databases and SQL

Project Proposal

9/15/24

My original idea is pictured below and we determined that it didn’t offer the level of complexity that we were looking for. 
![image](https://github.com/user-attachments/assets/334b7a40-d3e5-4673-a484-eeaf3cbdea8d)
 

What we landed on was doing a database that involves bands, the songs they performed, where/how they were performed, and what key they were in. Here is what that might look like:
We would have an entity type for Band. The band would have a name and band members. We decided that the band members would qualify as a plural attribute for the Band entity. 

Our next entity would be performance. The performance would hold the date and length of the performance. Additionally, this entity would have 2 subtypes: Live and Recorded. 
Next, we would have a Song entity. This would hold the name of the song, the composer/writer, and the album it was on (if applicable, maybe it was a song that was only ever played live. \mm/ )

We would finish off with a Key entity. This would probably store the name of the key the song was written in, as well as if this key contains sharps, flats, or is natural. We could perhaps even find its circle of fifths position. Example: C major, position 0. G major, position 1. We could even define their emotional quality. 

Let’s lay it out. 

    Entity Type: Band. Sample Bands: Bands (The Dillards, Bob Dylan, Grateful Dead, Billy Strings, Peter Paul and Mary.) Members (Peter Yarrow) YearFormed (1961)

    Entity Type: Performance. Sample Performance: Date (1964-7-26) Length (5.00)

          Subtypes
          Subtype: Live. Sample Live: Venue (Newport Folk Festival) ApproxCrowdSize (70000) Indoor or Outdoor (Indoor)
          Subtype: Record. Sample Record: Medium (vinyl, MP3)

    Entity Type: Song. Song Example: Name (Mr. Tambourine Man) Artist (Bob Dylan) Album (Bringing It All Back Home)

    Entity Type: Key. Sample Key: Key (C major) Shaprs/Flats/Natural (Natural) CircleOfFifthsPosition (0)

QUESTIONS
While this would be a rather small database, we should at least be able to answer a few questions by querying it:

“What bands have covered (insert favorite song here)”

“Does this band mostly tour or are they a studio artist?”

“Who were the members of The Grateful Dead when Tennessee Jed was written?”

“Does Billy Strings play ‘There is a Time’ in the same key as The Dillards?”


These were the notes we took during our meeting to come up with this structure. 
![image](https://github.com/user-attachments/assets/99a969cc-fac6-4305-96a6-2125199e8572)

