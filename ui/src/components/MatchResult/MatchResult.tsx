"use client";

import { useState, useEffect } from "react";
import styles from "./MatchResult.module.css";
import Button from "@codegouvfr/react-dsfr/Button";

type MatchResult = {
  equipe1: string;
  score1: string;
  score2: string;
  equipe2: string;
};

export function MatchResult({
  result,
  prono,
  dateMatch,
}: {
  result: MatchResult;
  prono: MatchResult;
  dateMatch: string;
}) {
  const [statutMatch, setStatutMatch] = useState("");

  const MINUTE_MS = 60000;

  useEffect(() => {
    const interval = setInterval(() => {
      console.log("Logs every minute");
    }, MINUTE_MS);
  });

  useEffect(() => {
    const inputDate = new Date(dateMatch);
    const currentDate = new Date();
    console.log(inputDate);
    console.log(currentDate);

    if (inputDate < currentDate) {
      setStatutMatch("A venir");
    } else if (inputDate >= currentDate) {
      setStatutMatch("En cours");
    }
  }, [dateMatch]);

  return (
    <>
      <div className={styles.match}>
        <div>
          Score: {result["equipe1"]} | {result["score1"]} - {result["score2"]} |{" "}
          {result["equipe2"]}
        </div>

        <div>
          Prono: {prono["equipe1"]} | {prono["score1"]} - {prono["score2"]} |{" "}
          {prono["equipe2"]}
        </div>
        <div>
          {dateMatch} - {statutMatch}
        </div>
        <Button
          iconId="fr-icon-checkbox-circle-line"
          onClick={function noRefCheck() {}}
        >
          Label button
        </Button>
      </div>
    </>
  );
}
