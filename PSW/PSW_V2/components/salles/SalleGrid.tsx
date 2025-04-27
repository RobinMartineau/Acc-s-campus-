"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Lock, Unlock, Users } from "lucide-react";

interface Salle {
  id: number;
  nom: string;
  capacite: number;
  occupation: number;
  estUtilisee: boolean;
}

interface SallesGridProps {
  salles: Salle[];
  obtenirPourcentageOccupation: (salle: Salle) => number;
  obtenirCouleurOccupation: (salle: Salle) => string;
  onSelectSalle: (salle: Salle) => void;
}

export function SallesGrid({
  salles,
  obtenirPourcentageOccupation,
  obtenirCouleurOccupation,
  onSelectSalle,
}: SallesGridProps) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
      {salles.map((salle) => (
        <Card
          key={salle.id}
          className={`cursor-pointer hover:shadow-md transition-shadow ${
            !salle.estUtilisee ? "opacity-70" : ""
          }`}
          onClick={() => onSelectSalle(salle)}
        >
          <CardContent className="p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-medium">{salle.nom}</h3>
              {salle.estUtilisee ? (
                <Lock className="h-4 w-4 text-red-500" />
              ) : (
                <Unlock className="h-4 w-4 text-green-500" />
              )}
            </div>
            <div className="flex items-center gap-1 text-sm text-gray-600 mb-2">
              <Users className="h-3 w-3" />
              <span>
                {salle.occupation}/{salle.capacite}
              </span>
            </div>
            <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className={`h-full ${obtenirCouleurOccupation(salle)}`}
                style={{ width: `${obtenirPourcentageOccupation(salle)}%` }}
              />
            </div>
            <div className="mt-2 flex justify-between items-center">
              <Badge variant={salle.estUtilisee ? "destructive" : "outline"}>
                {salle.estUtilisee ? "Occupée" : "Libre"}
              </Badge>
              <span className="text-xs">
                {salle.estUtilisee
                  ? `${Math.round(obtenirPourcentageOccupation(salle))}%`
                  : "0%"}
              </span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
