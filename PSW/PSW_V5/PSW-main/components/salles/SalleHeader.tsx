"use client";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { SallesHeaderProps } from "@/types";

export function SallesHeader({
  termeRecherche,
  setTermeRecherche,
  filtreOccupation,
  setFiltreOccupation,
  onResetPage,
}: SallesHeaderProps) {
  return (
    <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
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
            <SelectItem value="disponible">Disponibles</SelectItem>
            <SelectItem value="utilise">En utilisation</SelectItem>
            <SelectItem value="quasiComplet">Presque complètes</SelectItem>
            <SelectItem value="complet">Complètes</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
