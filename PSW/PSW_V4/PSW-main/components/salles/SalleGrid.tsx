"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Lock, Unlock, Users } from "lucide-react";
import { SallesGridProps } from "@/types";

export function SallesGrid({ salles, onSelectSalle }: SallesGridProps) {
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
            <div className="mt-2 flex justify-between items-center">
              <Badge variant={salle.estUtilisee ? "destructive" : "outline"}>
                {salle.estUtilisee ? "Occupée" : "Libre"}
              </Badge>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
