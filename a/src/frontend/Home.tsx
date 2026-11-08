import React, { Fragment, useCallback, useState } from "react";
import styles from "./Home.module.css";
import Webcam from "react-webcam";
import { useRef } from "react";
import api from "./api";

export default function Home() {
  const webcamRef = useRef<Webcam>(null);

  const handleRegister = () => {
    const imgURL = webcamRef.current?.getScreenshot();

    if (!imgURL) {
      console.log("Could not take screenshot from webcam...");
      return;
    }

    console.log(imgURL.slice(23));

    const nameInput = window.prompt("Enter your name");

    if (nameInput) {
      const payload = {
        name: nameInput,
        base64_face_img: imgURL.split(",")[1], // Clear "data:image/jpeg;base64," to leave only the base64 string
      };

      api
        .post("", payload)
        .then(() => {
          console.log("face img passed to the backend successfully!");
        })
        .catch((error) => {
          console.log("Error sending img to backend... ", error);
        });
    }
    console.log(nameInput);
  };

  const handleFaceId = () => {
    const imgURL = webcamRef.current?.getScreenshot();

    if (!imgURL) {
      console.log("Could not take screenshot from webcam...");
      return;
    }

    const payload = {
        base64_face_img: imgURL.split(",")[1], // Clear "data:image/jpeg;base64," to leave only the base64 string
      };
    
    // api.post("/FaceID", payload).then((response.data) => {}).catch()

  }
  return (
    <main className={styles.body}>
      <h1>Welcome to the Facial Recognition Project</h1>
      <p>Home page</p>
      <div className={styles.webCamContainer}>
        <Webcam
          className={styles.webCam}
          ref={webcamRef}
          audio={false}
          screenshotFormat={"image/jpeg"}
        ></Webcam>
      </div>
      <div className={styles.BtnContainer}>
      <button className={styles.registerBtn} onClick={handleRegister}>
        Registrar rostro
      </button>
      <button className={styles.registerBtn} onClick={handleFaceId}>
        Reconocer rostro
      </button>
      </div>
    </main>
  );
}
