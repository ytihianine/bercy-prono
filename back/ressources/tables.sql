CREATE TABLE IF NOT EXISTS public.equipes {
    id_equipe SERIAL PRIMARY KEY,
    nom_equipe TEXT,
    nom_court TEXT
};

CREATE TABLE IF NOT EXISTS public.pays {
    id_pays SERIAL PRIMARY KEY;
    nom_pays TEXT;
    svg_filename TEXT;
}

DROP TABLE public.matchs IF EXISTS;
CREATE TABLE IF NOT EXISTS public.matchs {
    id_match SERIAL PRIMARY KEY,
    date_match DATE,
    heure_match TIME,
    statut_match TEXT,
    equipe_a TEXT,
    equipe_b TEXT,
    score_a TEXT,
    score_b TEXT,
    type_match TEXT
};

CREATE TABLE IF NOT EXISTS public.pronostiques (
    id_pronostique SERIAL PRIMARY KEY,
    id_match INT,
    id_joueur INT,
    score_prono_a INT,
    score_prono_b INT,
    resultat TEXT,
    date_validation_pronostique DATE
);

CREATE TABLE IF NOT EXISTS public.classement (
    id_classement SERIAL PRIMARY KEY,
    rang_joueur INT,
    id_joueur INT,
    points INT
);
