"use client";

import { Input } from "@codegouvfr/react-dsfr/Input";
import { Button } from "@codegouvfr/react-dsfr/Button";
import { useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./enregistrement.module.css"
import Alert from "@codegouvfr/react-dsfr/Alert";

export default function Enregistrement() {
  const router = useRouter();
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
    mail: ""
  });

  const handleLogin = async () => {
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + "/user/enregistrement", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(credentials)
    });

    if (res.status === 201) {
      router.push("/authentification/connexion");
    }
  };

  const handleInputChange = (event: any) => {
    const { name, value } = event.target;
    setCredentials({
      ...credentials,
      [name]: value
    });
  };

  return (
    <>
    <Alert
        className={styles['bandeau-sup']}
          description="Un mail de confirmation vous sera envoyé. Pensez à vérifier vos spams."
          onClose={function noRefCheck() {}}
          severity="info"
        />
      <h1>S'enregistrer</h1>
      <Input
        label="Email"
        state="default"
        stateRelatedMessage="Text de validation / d'explication de l'erreur"
        value={credentials.mail}
        onChange={handleInputChange}
        nativeInputProps={{
          type: "mail",
          pattern: ".+@finances.gouv.fr",
          name: "mail"
        }}
      />
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
        S'enregistrer
      </Button>
    </>
  );
}
