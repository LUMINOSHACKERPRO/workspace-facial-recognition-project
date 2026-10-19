import React from 'react';
import styles from './Home.module.css';
import Webcam from "react-webcam"
import { useRef } from 'react';

export default function Home() {
  const webCamRef = useRef(null)
  
  return (
    <main className={styles.body}>
      <h1>Welcome to the Facial Recognition Project</h1>
      <p>This is the home page of the application.</p>
      <div className={styles.webCamContainer}>
        <Webcam className={styles.webCam}></Webcam>
      </div>
      <button className={styles.registerBtn}>Registrar rostro</button>
    </main>
  )
}