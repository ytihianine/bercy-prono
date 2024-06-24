"use client";

import { Input } from "@codegouvfr/react-dsfr/Input";
import { Button } from "@codegouvfr/react-dsfr/Button";
import { useState } from "react";

export default function Connexion() {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });

  const handleInputChange = (event: any) => {
    const { name, value } = event.target;
    setCredentials({
      ...credentials,
      [name]: value,
    });
  };

  const handleLogin = async () => {
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });

    const user = await res.json();

    if (user) {
      setUser(user);
      router.push("/");
    }
  };

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
          name: "username",
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
          type: "password",
        }}
      />
      <Button
        onClick={() => {
          alert(
            `Connexion avec ${credentials.username} et ${credentials.password}`
          );
        }}
      >
        Se connecter
      </Button>
      <br></br>
      <Button
        onClick={() => {
          alert("S'enregistrer");
        }}
      >
        S'enregistrer
      </Button>
    </>
  );
}
