import React, { useEffect, useState } from 'react';
import styles from '/styles/styles.module.css';

const topSongsData: Record<string, string[]> = {
    "2019": [
      "JUMP (feat. YoungBoy Never Broke Again) by DaBaby",
      "Every Single Time by Jonas Brothers",
      "Honky Tonk Highway by Luke Combs",
      "Why DON'T You LOVE me? by Tory Lanez",
      "I THINK by Tyler, The Creator"
    ],
    "2021": [
      "the 1 by Taylor Swift",
      "Oxytocin by Billie Eilish",
      "Baby Pluto by Lil Uzi Vert",
      "Conversation Pt. 1 by Mac Miller",
      "Bought A Bad Bitch by Future"
    ],
    "2017": [
      "Even My Dad Does Sometimes by Ed Sheeran",
      "Don't Say by The Chainsmokers",
      "Can't Have Everything by Drake",
      "8TEEN by Khalid",
      "Gettin' In The Way by Keith Urban"
    ],
    "2015": [
      "Love Me Harder by Ariana Grande",
      "Fireball (feat. John Ryan) by Pitbull",
      "Dollar Signs (feat. Tinashe) by Calvin Harris",
      "Out Of The Woods by Taylor Swift",
      "In The Night by The Weeknd"
    ],
    "2022": [
      "I THINK by Tyler, The Creator",
      "I'm Sorry by Lil Uzi Vert",
      "Bad Blood by Taylor Swift",
      "Less Than Zero by The Weeknd",
      "Gasoline by The Weeknd"
    ],
    "2018": [
      "Privacy by Chris Brown",
      "River (feat. Ed Sheeran) by Eminem",
      "Supermarket Flowers by Ed Sheeran",
      "Psycho (feat. Ty Dolla $ign) by Post Malone",
      "Congratulations by Post Malone"
    ],
    "2016": [
      "Don't Hurt Yourself (feat. Jack White) by Beyonce",
      "Body Electric by Lana Del Rey",
      "Love Yourself by Justin Bieber",
      "Brenda's Got A Baby by 2Pac",
      "M'$ (feat. Lil Wayne) by A$AP Rocky"
    ],
    "2020": [
      "Rich & Sad by Post Malone",
      "HYFR (Hell Ya Fucking Right) by Drake",
      "This Ain't That by Trippie Redd",
      "Ball For Me (feat. Nicki Minaj) by Post Malone",
      "Just How It Is by Young Thug"
    ]
  }
  

  const Top200: React.FC = () => {
    const sortedYears = Object.keys(topSongsData).sort((a, b) => Number(b) - Number(a));
  
    return (
      <div>
        <h3>Top 200 Songs</h3>
        <div className={styles.columnContainer}>
          {sortedYears.map((year, index) => (
            <div className={styles.column} key={year}>
              <h4>{year}</h4>
              <ul>
                {topSongsData[year].map((song, songIndex) => (
                  <li key={songIndex}>{song}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  export default Top200;