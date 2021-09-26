
# Voting App

Codeinit() Hackathon topic - SAC Elections

Team Bully Maguire

Team Members - Ayush Peter Junior,Kartik Shukla 


## Tech Stack

**Front End** : Bootstrap, React

**Backend** : Flask

**Database** : PostgreSQL
  
**Token Encryption/Decyption Module** : itsdangerous
## Introduction

Our project is a basic voting web app built using flask which makes use of email 
verification using token encryption/decryption.

  
## Aims

Verify the identity of the voter.

Prevent double Voting.

To get the votes for all the posts from each candidate.

To decide winner for each post on the basis of vote count.




  
## Features

- Voter only needs to enter his/her nitc mail id to register following which he/she will be sent a verfication mail.
- The verification mail will have the voting page link which will be generated through a unique token number.
- After this the voter's response will be added to the database and his/her voting status will be set as true.
- If the voter tries to double vote he/she will be prompted out to an error page.

  
