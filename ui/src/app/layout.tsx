"use client"

import { useState } from 'react';
import { DsfrHead } from "@codegouvfr/react-dsfr/next-appdir/DsfrHead";
import { DsfrProvider } from "@codegouvfr/react-dsfr/next-appdir/DsfrProvider";
import { getHtmlAttributes } from "@codegouvfr/react-dsfr/next-appdir/getHtmlAttributes";
import { StartDsfr } from "./StartDsfr";
import { defaultColorScheme } from "./defaultColorScheme";
import { Header } from "@codegouvfr/react-dsfr/Header";
import { Footer } from "@codegouvfr/react-dsfr/Footer";
import { Badge } from "@codegouvfr/react-dsfr/Badge";
import Link from "next/link";
import './globals.css';  // Assurez-vous que ce fichier CSS est importé

export default function RootLayout({ children }: { children: JSX.Element }) {
  const [activeTab, setActiveTab] = useState(0);

  const handleActiveTab = (index: number) => {
    setActiveTab(index);
  };

  const lang = "fr";
  return (
    <html {...getHtmlAttributes({ defaultColorScheme, lang })}>
      <head>
        <StartDsfr />
        <DsfrHead Link={Link} />
      </head>
      <body>
        <DsfrProvider lang={lang}>
          <div className="main">
            <Header
              brandTop={
                <>
                  INTITULE
                  <br />
                  OFFICIEL
                </>
              }
              homeLinkProps={{
                href: "/",
                title: "Accueil - Bercy Prono",
              }}
              id="fr-header-simple-header-with-service-title-and-tagline"
              // onClick={() => alert("test")}
              navigation={[
                {
                  linkProps: {
                    href: '/pronostiques',
                    target: '_self',
                    onClick: () => handleActiveTab(0)
                  },
                  text: 'Mes pronostics',
                  isActive: activeTab === 0,
                },
                {
                  linkProps: {
                    href: '/classement',
                    target: '_self',
                    onClick: () => handleActiveTab(1)
                  },
                  text: 'Classement général',
                  isActive: activeTab === 1,
                },
                {
                  linkProps: {
                    href: '/regles',
                    target: '_self',
                    onClick: () => handleActiveTab(2)
                  },
                  text: 'Règles de calcul',
                  isActive: activeTab === 2,
                }
              ]}
              serviceTitle={
                <>
                  Bercy Pronostic{" "}
                  <Badge as="span" noIcon severity="success">
                    Beta
                  </Badge>
                </>
              }
            />
            <div class="fr-container">
              {children}
            </div>
            <Footer
              className="CustomFooter"
              accessibility="fully compliant"
              contentDescription="
                Ce message est à remplacer par les informations de votre site.
                Comme exemple de contenu, vous pouvez indiquer les informations
                suivantes : Le site officiel d’information administrative pour les entreprises.
                Retrouvez toutes les informations et démarches administratives nécessaires à la création,
                à la gestion et au développement de votre entreprise.
              "
              termsLinkProps={{
                href: "#",
              }}
              websiteMapLinkProps={{
                href: "#",
              }}
            />
          </div>
        </DsfrProvider>
      </body>
    </html>
  );
}
