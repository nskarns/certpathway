# Cert Pathway
This is a scalable website that would allow users to find certificates that would help them progress through their journey by using only filling out an interest form and uploading their resume. This repository is copied from the originally group project repository since I'm not the owner of that repository.

## Development Process
This project had many different aspects to it, Google OAuth, the frontend of the website, finding certificates to have on our website, and the recommender system. I completed the recommender system which would allow for users to recieve nearly instant results on what certificates would work right for them. 

The recommender system used an inverted index to decide what certificates would be presented to the user. Upon submission of the interest form and the resume, the recommender system would parse out the words from both the resume and the selected responses on the interest form. This word list would be ran by the inverted index to find the certificates that had the most matching words when compared with the user word list. These ranked results would then be returned to the frontend for the user to see the results.

## Features
A user can hop onto our website, fill out the interest form and upload their resume to recieve results and links to certificates that can help them. Outside of that main objective, users could optionally make an account and view their profile page which in the future would store previous results. This would have been added if we had more development time. 

## Example of Project
Below is linked a video that my team and I submitted that shows a brief demo of a user being on the home page, filling out the interest form, uploading their resume, finding their results, and going to the certificate website.

[Video Link](https://github.com/nskarns/certpathway/blob/master/CertPathway%20Video%20Example.mp4)
