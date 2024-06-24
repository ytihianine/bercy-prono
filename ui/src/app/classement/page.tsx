'use client'

import { Table } from "@codegouvfr/react-dsfr/Table";

export default function Classement() {
    const headers = ['Rang', 'Joueur', 'Points']
    const fake_data = [[1, 'Frosch', 100], [2, 'Toga', 20], [3, 'Acnologia', 2]]
    const last_maj = "22/06/2024 17h30"

    return (
        <>
        <Table
  caption={"Classement actuel - dernière mise à jour: " + last_maj}
  data={fake_data}
  headers={headers}
/>
        </>
    )
}
