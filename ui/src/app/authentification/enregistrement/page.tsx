'use client'

import { Input } from "@codegouvfr/react-dsfr/Input";
import { Button } from "@codegouvfr/react-dsfr/Button";
import { useState } from "react";

export default function Enregistrement() {
    const [credentials, setCredentials] = useState({ username: "", password: "", email: "" });

    const handleInputChange = (event: any) => {
        const { name, value } = event.target;
        setCredentials({
            ...credentials,
            [name]: value,
        });
    };

    return (
        <>
            <h1>S'enregistrer</h1>
            <Input
                label="Email"
                state="default"
                stateRelatedMessage="Text de validation / d'explication de l'erreur"
                value={credentials.email}
                onChange={handleInputChange}
                nativeInputProps={{
                    type:"email",
                    pattern:".+@finances\.gouv\.fr",
                    name:"email"
                }}
            />
            <Input
                label="Identifiant"
                state="default"
                stateRelatedMessage="Text de validation / d'explication de l'erreur"
                value={credentials.username}
                onChange={handleInputChange}
                nativeInputProps={{
                    name:"username"
                }}
            />
            <Input
                label="Mot de passe"
                state="default"
                stateRelatedMessage="Text de validation / d'explication de l'erreur"
                value={credentials.password}
                onChange={handleInputChange}
                nativeInputProps={{
                    name:"password",
                    type: "password"
                }}
            />
            <Button onClick={() => {alert(`Enregistrement avec ${credentials.email} -- ${credentials.username} -- ${credentials.password}`)}}>S'enregistrer</Button>
        </>
    );
}
