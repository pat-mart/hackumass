# Mood Mood Light

Submission for HackUMass 12.0.

## About

Mood Mood Light is a Python app that changes the color of strip lights as your mood (emotion) changes. We use AWS Rekognition to get facial emotions and let users customize what color corresponds to what emotion. The strip lights slowly change color over time as your emotion changes. Additionally, we have modes where we play spotify music based on emotion and where the light propogation is controlled by sound.

## How to Run
Run client/src/main.py. You will need to deploy AWS beforehand (We have a Terraform script that configures everything for you!) and will need to create Spotify API credentials.


