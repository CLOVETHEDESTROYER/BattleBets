import { ConnectWallet } from "@thirdweb-dev/react";
import type { NextPage } from "next";
import styles from "../styles/Home.module.css";
import { getData } from './api';
import axios from 'axios';
import React, { useEffect, useState } from "react";


  

const Home: NextPage = () => {

  const [data, setData] = useState([{}])

  useEffect(() => {
    axios.get("/winner").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data);
      }
    )
  }, [])
  

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="http://thirdweb.com/">BETfighter</a>!
        </h1>

        <p className={styles.description}>
          The worlds first computer vision betting app for AAA fighting games.
        
        </p>

        <div className={styles.connect}>
          <ConnectWallet />
        </div>

        <div className={styles.grid}>
          <a href="https://portal.thirdweb.com/" className={styles.card}>
            <h2>Place your Bet Here &rarr;</h2>
            <p>
              This is where you will place your initial Bet.
            </p>
          </a>

          <a href="https://thirdweb.com/dashboard" className={styles.card}>
            <h2>Choose Your Game &rarr;</h2>
            <p>
              We currently only support MK11.  Tekken and Street Fighter Coming S
            </p>
          </a>

          <a
            href="https://portal.thirdweb.com/templates"
            className={styles.card}
          >
            <h2>Fighter 2 &rarr;</h2>
            <p>
See if your opponent is ready for battle.            </p>
          </a>
        </div>
        <div>
        <h1>Data from Flask backend:</h1>
        <p>{JSON.stringify(data)}</p>
        
      </div>
      </main>
    </div>
  );
 
  
};


export default Home;
