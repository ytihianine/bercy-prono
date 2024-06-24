"use client";

import { MatchProno } from "@/components/MatchPronostique/Matchprono";
import styles from "./pronostiques.module.css";
import { MatchResult } from "@/components/MatchResult/MatchResult";

export default function Pronostiques() {
  const fake_data = [
    { equipe1: "FRA", score1: "1", equipe2: "AUT", score2: "0" },
    { equipe1: "FRA", score1: "1", equipe2: "AUT", score2: "0" },
    { equipe1: "FRA", score1: "1", equipe2: "AUT", score2: "0" },
  ];

  return (
    <>
      <h3>Huitièmes de finale</h3>
      <div className={styles.listeMatch}>
        {fake_data.map((match, index) => (
          <>
            <MatchResult key={index} result={match} prono={match} dateMatch={"2024/06/22 16:30"}></MatchResult>
          </>
        ))}
      </div>

      <h3>Quarts de finale</h3>
      <h3>Demi-finales</h3>
      <h3>Finale</h3>
    </>
  );
}
