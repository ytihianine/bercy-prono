"use client";

import { useState, useEffect } from "react";
import styles from "./MatchResult.module.css";
import Button from "@codegouvfr/react-dsfr/Button";
import Badge from "@codegouvfr/react-dsfr/Badge";
import "@codegouvfr/react-dsfr/dsfr/utility/icons/icons-design/icons-design.css";
import Input from "@codegouvfr/react-dsfr/Input";

type DataMatch = {
  date_match: string;
  date_validation_pronostique: string;
  equipe_a: string;
  equipe_b: string;
  id_joueur: string;
  id_match: string;
  id_pronostique: string;
  index: string;
  resultat: string;
  score_a: string;
  score_b: string;
  score_prono_a: string;
  score_prono_b: string;
  statut_match: string;
  type_match: string;
};

export function MatchResult({ data_match }: { data_match: DataMatch }) {
  const pays = {
    'Pays-Bas': 'nl.svg',
    'Slovénie': 'si.svg',
    'Belgique': 'be.svg',
    'Géorgie': 'ge.svg',
    'Espagne': 'es.svg',
    'Danemark': 'dk.svg',
    'Allemagne': 'de.svg',
    'France': 'fr.svg',
    'Suisse': 'ch.svg',
    'Angleterre': 'gb.svg',
    'Portugal': 'pt.svg',
    'Autriche': 'at.svg',
    'Turquie': 'tr.svg',
    'Roumanie': 'ro.svg',
    'Italie': 'it.svg',
    'Slovaquie': 'sk.svg',
  }

  const [statutMatch, setStatutMatch] = useState("");
  const [statutModification, setStatutModification] = useState(false);
  const [pronostique, setPronostique] = useState({
    score_prono_a: data_match['score_prono_a'],
    score_prono_b: data_match['score_prono_b']
  });

  const handleInputChange = (event: any) => {
    const { name, value } = event.target;
    setPronostique({
      ...pronostique,
      [name]: value
    });
  };

  const postPronostic = async () => {
    try {
      const response = await fetch(
        process.env.NEXT_PUBLIC_API_URL + "/match/prono",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            id_match: data_match["id_match"],
            username: localStorage.getItem('usernameBercyProno'),
            score_prono_a: pronostique["score_prono_a"],
            score_prono_b: pronostique["score_prono_b"]
          })
        }
      );
      if (!response.ok) {
        throw new Error("Failed to to post prono");
      }
      console.log("prono fait");
    } catch (error) {
      console.error("Error fetching information matchs:", error);
    }
  };

  const MINUTE_MS = 60000;

  function changeModification() {
    console.log(pronostique)
    if (statutModification) {
      console.log(pronostique);
      postPronostic();
      setStatutModification(false);
    } else {
      setStatutModification(true);
    }
  }

  function statut_badge(statut) {
    if (statut == "a venir") {
      return (
        <>
          <Badge severity="new">A venir</Badge>
        </>
      );
    }
    if (statut == "en cours") {
      return (
        <>
          <Badge severity="new">En cours</Badge>
        </>
      );
    }
    if (statut == "terminé") {
      return (
        <>
          <Badge severity="success">Terminé</Badge>
        </>
      );
    }
    return (
      <>
        <Badge severity="error">Erreur</Badge>
      </>
    );
  }

  useEffect(() => {
    const inputDate = new Date(data_match["date_match"]);
    const currentDate = new Date();
    console.log(inputDate);
    console.log(currentDate);

    if (inputDate < currentDate) {
      setStatutMatch("A venir");
    } else if (inputDate >= currentDate) {
      setStatutMatch("En cours");
    }
  }, [data_match["date_match"]]);

  return (
    <>
      <div className={styles.match}>
        <div className={styles["bandeau-sup"]}>
          <div>{data_match["date_match"]}</div>
          <div>{statut_badge(data_match["statut_match"])}</div>
        </div>

        <div className={styles["equipes"]}>
          <div>
            {data_match["equipe_a"]}{" "}
            <img
              className={styles["img-drapeau"]}
              src={"/drapeaux/" + pays[data_match['equipe_a']]}
              alt={"Drapeau: " + pays[data_match['equipe_a']]}
            />
          </div>
          <div>
            <img
              className={styles["img-drapeau"]}
              src={"/drapeaux/" + pays[data_match['equipe_b']]}
              alt={"Drapeau: " + pays[data_match['equipe_b']]}
            /> {" "}
            {data_match["equipe_b"]}
          </div>
        </div>

        {statutModification ? (
          <>
            <div className={styles["resultat"]}>
              <div className={styles["input-prono"]}>
                <div className={styles["champ-prono"]}>
                  <Input
                    label={null}
                    value={pronostique.score_prono_a}
                    onChange={handleInputChange}
                    nativeInputProps={{
                      name: "score_prono_a",
                      placeholder: pronostique.score_prono_a
                    }}
                  />
                </div>
                <div className={styles["champ-prono"]}>
                  <Input
                    label={null}
                    value={pronostique.score_prono_b}
                    onChange={handleInputChange}
                    nativeInputProps={{
                      name: "score_prono_b",
                      placeholder: pronostique.score_prono_b
                    }}
                  />
                </div>
              </div>

              <div className={styles["center-button"]}>
                <Button
                  className={styles["button-border"]}
                  iconId="fr-icon-checkbox-circle-line"
                  onClick={changeModification}
                >
                  Valider mon pronostique
                </Button>
              </div>
            </div>
          </>
        ) : (
          <>
            <div className={styles["resultat"]}>
              <div className={styles["score"]}>prono</div>
              <div>
                {data_match["score_prono_a"]} - {data_match["score_prono_b"]}
              </div>
            </div>
            <div className={styles["resultat"]}>
              <div className={styles["score"]}>score</div>
              <div>
                {data_match["statut_match"] == "à venir" ? (
                  data_match["statut_match"]
                ) : (
                  <>
                    {data_match["score_a"]} - {data_match["score_b"]}
                  </>
                )}
              </div>
            </div>

            <div className={styles["center-button"]}>
              {data_match["statut_match"] === "a venir" ? (
                <Button
                  className={styles["button-border"]}
                  iconId="fr-icon-ball-pen-fill"
                  onClick={changeModification}
                >
                  Modifier mon pronostique
                </Button>
              ) : (
                <Button
                  className={styles["button-border"]}
                  disabled
                  iconId="fr-icon-ball-pen-fill"
                  onClick={changeModification}
                >
                  Modifier mon pronostique
                </Button>
              )}
            </div>
          </>
        )}
      </div>
    </>
  );
}
