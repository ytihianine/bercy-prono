"use client";

import styles from "./pronostiques.module.css";
import { MatchResult } from "@/components/MatchResult/MatchResult";
import { useState, useEffect } from "react";
import Alert from "@codegouvfr/react-dsfr/Alert";
import { useRouter } from "next/navigation";

export default function Pronostiques() {
  const router = useRouter()
  const [matchs, setMatchs] = useState(null);

  // Check if user is logged
  useEffect(() => {
    if (localStorage.getItem("bearToken") === null) {
      router.push("/authentification/connexion")
    }
  }, [])

  useEffect(() => {
    const fetchMatchs = async () => {
      try {
        const response = await fetch(
          process.env.NEXT_PUBLIC_API_URL + "/match/information", {
          method: "POST",
          headers: {
            "Content-Type": "Application/json",
            "Authorization" : "Bearer " + localStorage.getItem('bearToken')
          },
          body: JSON.stringify({'username': localStorage.getItem('usernameBercyProno')})
        });

        if (!response.ok) {
          throw new Error("Failed to fetch fiche data");
        }
        const data_matchs = await response.json();
        setMatchs(data_matchs);
        console.log("ici");
        console.log(data_matchs);
      } catch (error) {
        console.error("Error fetching information matchs:", error);
      }
    };
    fetchMatchs();
  }, []);

  if (!matchs) {
    return (
      <>
        <Alert
          description="Chargement des données des matchs"
          onClose={function noRefCheck() {}}
          severity="info"
        />
      </>
    );
  }

  return (
    <>
      <h3>Huitièmes de finale</h3>
      <div className={styles.listeMatch}>
        {matchs["results"].map((match, index) => {
          if (match["type_match"] === "Huitièmes de finale") {
            return <MatchResult key={index} data_match={match} />;
          } else {
            return null;
          }
        })}
      </div>

      <h3>Quarts de finale</h3>
      <h3>Demi-finale</h3>
      <h3>Finale</h3>
    </>
  );
}
