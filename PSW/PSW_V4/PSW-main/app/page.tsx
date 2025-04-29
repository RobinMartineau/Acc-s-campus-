"use client";

import { useState, useEffect, useMemo, useCallback } from "react";
import { subDays, addDays } from "date-fns";
import { SallesHeader } from "@/components/salles/SalleHeader";
import { SallesGrid } from "@/components/salles/SalleGrid";
import { SallesPagination } from "@/components/salles/SallePagination";
import { SallesDetailsDrawer } from "@/components/salles/SalleDrawer";
import { Salle, Activite } from "@/types";

export default function Home() {
  // États principaux
  const [dateSelectionnee, setDateSelectionnee] = useState(new Date());
  const [salles, setSalles] = useState<Salle[]>([]);
  const [salleSelectionnee, setSalleSelectionnee] = useState<Salle | null>(
    null
  );
  const [activite, setActivite] = useState<Activite | null>(null);
  const [termeRecherche, setTermeRecherche] = useState("");
  const [filtreOccupation, setFiltreOccupation] = useState<string>("tout");
  const sallesParPage = 30;
  const [pageCourante, setPageCourante] = useState(1);

  // Appel API pour récup toutes les salles
  useEffect(() => {
    async function fetchSalles() {
      try {
        const response = await fetch("/api/salle/listeSalles");
        const data = await response.json();
        const sallesFromApi: Salle[] = data.map((item: Salle) => ({
          id: item.id,
          nom: item.numero,
          estUtilisee: item.statut,
          numero: item.numero,
        }));
        setSalles(sallesFromApi);
      } catch (error) {
        console.error("Erreur lors de la récupération des salles:", error);
      }
    }
    fetchSalles();
  }, [dateSelectionnee]);

  // Navigat° entre jours
  const jourPrecedent = useCallback(() => {
    setDateSelectionnee((datePrecedente) => subDays(datePrecedente, 1));
  }, []);

  const jourSuivant = useCallback(() => {
    setDateSelectionnee((datePrecedente) => addDays(datePrecedente, 1));
  }, []);

  // Filtrage des salles par recherche et occupat°
  const sallesFiltrees = useMemo(() => {
    return salles.filter((salle) => {
      const correspondRecherche = salle.nom
        .toLowerCase()
        .includes(termeRecherche.toLowerCase());
      switch (filtreOccupation) {
        case "utilise":
          return correspondRecherche && salle.estUtilisee;
        case "disponible":
          return correspondRecherche && !salle.estUtilisee;
        case "complet":
          return (
            correspondRecherche &&
            salle.estUtilisee &&
            salle.occupation === salle.capacite
          );
        case "quasiComplet":
          return (
            correspondRecherche &&
            salle.estUtilisee &&
            salle.occupation >= salle.capacite * 0.8 &&
            salle.occupation < salle.capacite
          );
        default:
          return correspondRecherche;
      }
    });
  }, [salles, termeRecherche, filtreOccupation]);

  const pagesTotales = useMemo(() => {
    return Math.ceil(sallesFiltrees.length / sallesParPage);
  }, [sallesFiltrees, sallesParPage]);

  const sallesCourantes = useMemo(() => {
    const debut = (pageCourante - 1) * sallesParPage;
    return sallesFiltrees.slice(debut, debut + sallesParPage);
  }, [sallesFiltrees, pageCourante, sallesParPage]);

  // Fonct° pour récup l'activité d'une salle
  const fetchSalleActivite = async (salleId: number) => {
    try {
      const response = await fetch(`/api/salle/infosSalles/${salleId}`);
      const data: Activite = await response.json();
      setActivite(data);
    } catch (error) {
      console.error("Erreur lors de la récupération de l'activité:", error);
      setActivite(null);
    }
  };

  // Lors de la sélect° d'une salle, on récup l'activité
  const handleSelectSalle = (salle: Salle) => {
    setSalleSelectionnee(salle);
    fetchSalleActivite(salle.id);
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
        // Ici, on passe handleSelectSalle pour sélectionner et charger l'activité de la salle
        onSelectSalle={handleSelectSalle}
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
          // / On passe l'activité récupérée au drawer
          activite={activite}
          onClose={() => {
            setSalleSelectionnee(null);
            setActivite(null);
          }}
        />
      )}
    </div>
  );
}
