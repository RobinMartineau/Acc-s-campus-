"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { format } from "date-fns";
import { fr } from "date-fns/locale";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface SallesHeaderProps {
  dateSelectionnee: Date;
  onJourPrecedent: () => void;
  onJourSuivant: () => void;
  termeRecherche: string;
  setTermeRecherche: (val: string) => void;
  filtreOccupation: string;
  setFiltreOccupation: (val: string) => void;
  onResetPage: () => void;
}

export function SallesHeader({
  dateSelectionnee,
  onJourPrecedent,
  onJourSuivant,
  termeRecherche,
  setTermeRecherche,
  filtreOccupation,
  setFiltreOccupation,
  onResetPage,
}: SallesHeaderProps) {
  return (
    <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
      <div className="flex items-center gap-2">
        <Button
          aria-label="Jour précédent"
          onClick={onJourPrecedent}
          variant="outline"
          size="icon"
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <h2 className="text-xl font-bold">
          {format(dateSelectionnee, "EEEE dd MMMM yyyy", { locale: fr })}
        </h2>
        <Button
          aria-label="Jour suivant"
          onClick={onJourSuivant}
          variant="outline"
          size="icon"
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-2 w-full md:w-auto">
        <Input
          placeholder="Rechercher une salle..."
          value={termeRecherche}
          onChange={(e) => {
            setTermeRecherche(e.target.value);
            onResetPage();
          }}
          className="w-full sm:w-60"
        />
        <Select
          value={filtreOccupation}
          onValueChange={(valeur) => {
            setFiltreOccupation(valeur);
            onResetPage();
          }}
        >
          <SelectTrigger className="w-full sm:w-40">
            <SelectValue placeholder="Filtrer par statut" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="tout">Toutes les salles</SelectItem>
            <SelectItem value="utilise">En utilisation</SelectItem>
            <SelectItem value="disponible">Disponibles</SelectItem>
            <SelectItem value="complet">Complètes</SelectItem>
            <SelectItem value="quasiComplet">Presque complètes</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
