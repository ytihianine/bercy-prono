"use client";

import { Input } from "@codegouvfr/react-dsfr/Input";
import { Button } from "@codegouvfr/react-dsfr/Button";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Alert from "@codegouvfr/react-dsfr/Alert";
import styles from "./connexion.module.css"

export default function Connexion() {
  const router = useRouter();
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
    provider: "db",
    refresh: "true"
  });

  const handleInputChange = (event: any) => {
    const { name, value } = event.target;
    setCredentials({
      ...credentials,
      [name]: value
    });
  };

  const handleLogin = async () => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + "/security/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(credentials)
    });

    const loginResult = await res.json();
    const access_token = loginResult['access_token']

    if (access_token) {
      localStorage.setItem('bearToken', access_token)
      localStorage.setItem('usernameBercyProno', credentials['username'])
      router.push("/pronostiques");
    }
  };

  // Check if user is logged
  useEffect(() => {
    if (localStorage.getItem("bearToken") !!= null) {
      router.push("/pronostiques")
    }
  }, [])

  return (
    <>
      <h1>Se connecter</h1>
      <Input
        label="Identifiant"
        state="default"
        stateRelatedMessage="Text de validation / d'explication de l'erreur"
        value={credentials.username}
        onChange={handleInputChange}
        nativeInputProps={{
          name: "username"
        }}
      />
      <Input
        label="Mot de passe"
        state="default"
        stateRelatedMessage="Text de validation / d'explication de l'erreur"
        value={credentials.password}
        onChange={handleInputChange}
        nativeInputProps={{
          name: "password",
          type: "password"
        }}
      />

      <Button
        className={styles['button-custom']}
        onClick={handleLogin}
      >
        Se connecter
      </Button>

      <Button
        className={styles['button-custom']}
        onClick={() => {
          router.push("/authentification/enregistrement");
        }}
      >
        S'enregistrer
      </Button>
    </>
  );
}
