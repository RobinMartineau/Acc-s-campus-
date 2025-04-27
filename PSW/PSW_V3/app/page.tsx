"use client";

import { useState, useEffect, useMemo, useCallback } from "react";
import { subDays, addDays } from "date-fns";
import { SallesHeader } from "@/components/salles/SalleHeader";
import { SallesGrid } from "@/components/salles/SalleGrid";
import { SallesPagination } from "@/components/salles/SallePagination";
import { SallesDetailsDrawer } from "@/components/salles/SalleDrawer";

// Structure d'une salle
interface Salle {
  id: number;
  nom: string;
  capacite: number;
  occupation: number;
  estUtilisee: boolean;
}

// Fonction pour générer des salles aléatoires
const genererSalles = (nombre: number): Salle[] => {
  return Array.from({ length: nombre }, (_, i) => {
    const capacite = Math.floor(Math.random() * 30) + 10;
    const estUtilisee = Math.random() > 0.4;
    const occupation = estUtilisee
      ? Math.floor(Math.random() * capacite) + 1
      : 0;
    return {
      id: i + 1,
      nom: `Salle ${i + 1}`,
      capacite,
      occupation,
      estUtilisee,
    };
  });
};

export default function Home() {
  // États principaux
  const [dateSelectionnee, setDateSelectionnee] = useState(new Date());
  const [salles, setSalles] = useState<Salle[]>([]);
  const [salleSelectionnee, setSalleSelectionnee] = useState<Salle | null>(
    null
  );
  const [termeRecherche, setTermeRecherche] = useState("");
  const [filtreOccupation, setFiltreOccupation] = useState<string>("tout");
  const sallesParPage = 30;
  const [pageCourante, setPageCourante] = useState(1);

  // Mise à jour des salles lors du changement de date
  useEffect(() => {
    setSalles(genererSalles(300));
  }, [dateSelectionnee]);

  const jourPrecedent = useCallback(() => {
    setDateSelectionnee((datePrecedente) => subDays(datePrecedente, 1));
  }, []);

  const jourSuivant = useCallback(() => {
    setDateSelectionnee((datePrecedente) => addDays(datePrecedente, 1));
  }, []);

  const sallesFiltrees = useMemo(() => {
    return salles.filter((salle) => {
      const correspondRecherche = salle.nom
        .toLowerCase()
        .includes(termeRecherche.toLowerCase());
      if (filtreOccupation === "tout") return correspondRecherche;
      if (filtreOccupation === "utilise")
        return correspondRecherche && salle.estUtilisee;
      if (filtreOccupation === "disponible")
        return correspondRecherche && !salle.estUtilisee;
      if (filtreOccupation === "complet")
        return (
          correspondRecherche &&
          salle.estUtilisee &&
          salle.occupation === salle.capacite
        );
      if (filtreOccupation === "quasiComplet")
        return (
          correspondRecherche &&
          salle.estUtilisee &&
          salle.occupation >= salle.capacite * 0.8 &&
          salle.occupation < salle.capacite
        );
      return correspondRecherche;
    });
  }, [salles, termeRecherche, filtreOccupation]);

  const pagesTotales = useMemo(() => {
    return Math.ceil(sallesFiltrees.length / sallesParPage);
  }, [sallesFiltrees, sallesParPage]);

  const sallesCourantes = useMemo(() => {
    const debut = (pageCourante - 1) * sallesParPage;
    const fin = debut + sallesParPage;
    return sallesFiltrees.slice(debut, fin);
  }, [sallesFiltrees, pageCourante, sallesParPage]);

  const obtenirPourcentageOccupation = (salle: Salle) => {
    return (salle.occupation / salle.capacite) * 100;
  };

  const obtenirCouleurOccupation = (salle: Salle) => {
    if (!salle.estUtilisee) return "bg-gray-200";
    const pourcentage = obtenirPourcentageOccupation(salle);
    if (pourcentage >= 90) return "bg-red-500";
    if (pourcentage >= 70) return "bg-orange-400";
    if (pourcentage >= 50) return "bg-yellow-300";
    return "bg-green-400";
  };

  const changerPage = useCallback((nouvellePage: number) => {
    setPageCourante(nouvellePage);
  }, []);

  const resetPage = useCallback(() => {
    setPageCourante(1);
  }, []);

  return (
    <div className="w-full max-w-6xl mx-auto mt-8 px-4">
      <SallesHeader
        dateSelectionnee={dateSelectionnee}
        onJourPrecedent={jourPrecedent}
        onJourSuivant={jourSuivant}
        termeRecherche={termeRecherche}
        setTermeRecherche={setTermeRecherche}
        filtreOccupation={filtreOccupation}
        setFiltreOccupation={setFiltreOccupation}
        onResetPage={resetPage}
      />

      <SallesGrid
        salles={sallesCourantes}
        obtenirPourcentageOccupation={obtenirPourcentageOccupation}
        obtenirCouleurOccupation={obtenirCouleurOccupation}
        onSelectSalle={setSalleSelectionnee}
      />

      {pagesTotales > 1 && (
        <SallesPagination
          pageCourante={pageCourante}
          pagesTotales={pagesTotales}
          onPageChange={changerPage}
        />
      )}

      {salleSelectionnee && (
        <SallesDetailsDrawer
          salleSelectionnee={salleSelectionnee}
          dateSelectionnee={dateSelectionnee}
          obtenirPourcentageOccupation={obtenirPourcentageOccupation}
          obtenirCouleurOccupation={obtenirCouleurOccupation}
          onClose={() => setSalleSelectionnee(null)}
        />
      )}
    </div>
  );
}
