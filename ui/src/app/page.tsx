"use client";

import Alert from "@codegouvfr/react-dsfr/Alert";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.push("/authentification/connexion");
  }, []);
  return (
    <>
      <Alert
        description="Redirection en cours"
        onClose={function noRefCheck() {}}
        severity="info"
      />
    </>
  );
}
