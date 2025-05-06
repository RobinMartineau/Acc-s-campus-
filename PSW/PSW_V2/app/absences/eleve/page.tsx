"use client"; // Indique que c'est une utilisat° coté navigateur

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, Clock } from "lucide-react";
import { absence, retard } from "@/app/api/psw/route";

import { useEffect, useState } from "react";

// Interfaces absences et retards
interface Absence {
  id: number;
  cours: string;
  horaire: string;
  justifiee: boolean;
  motif: string;
}

interface Retard {
  cours: string;
  horaire: string;
  duree: number;
  justifiee: boolean;
  motif: string;
}

// Formate la date de la sorte: "jj/mm/aaaa hh:mm"
function formatDate(date: string): string {
  const dateObj = new Date(date); // Crée un objet Date

  // Récupère différentes parties de la date avec gestion format (ajout de 0 si besoin)
  const minutes = dateObj.getMinutes().toString().padStart(2, "0");
  const heures = dateObj.getHours();
  const jour = dateObj.getDate().toString().padStart(2, "0");
  const mois = (dateObj.getMonth() + 1).toString().padStart(2, "0"); // Les mois commencent à 0
  const annee = dateObj.getFullYear();

  return `${jour}/${mois}/${annee} ${heures}:${minutes}`;
}

export default function AbsencesRetardsPage() {
  // Etats (set + setter) pour stocker les absences et les retards
  const [absences, setAbsences] = useState<Absence[]>([]);
  const [retards, setRetards] = useState<Retard[]>([]);
  const [loading, setLoading] = useState(true); // Indicateur de chargement

  // Récupération des données au montage du composant
  useEffect(() => {
    async function fetchData() {
      try {
        // On récupère d'abord l'id utilisateur via notre API dédiée
        const user = await fetch("/api/auth/me");
        const { id_utilisateur } = await user.json();

        // On appelle l'API des absences avec le bon id
        const [absData, retData] = await Promise.all([
          absence.getAbsences(id_utilisateur),
          retard.getRetards(id_utilisateur),
        ]);
        setAbsences(absData);
        setRetards(retData);
      } catch (error) {
        console.error("Erreur au chargement des données :", error);
      } finally {
        setLoading(false); // Désactive le chargement dès que données récup
      }
    }

    fetchData();
  }, []);

  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold mb-6">Absences et Retards</h1>

      <Tabs defaultValue="absences" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="absences">Absences</TabsTrigger>
          <TabsTrigger value="retards">Retards</TabsTrigger>
        </TabsList>

        {/* Affichage des absences */}
        <TabsContent value="absences">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5" />
                <h2 className="text-xl font-semibold">Absences</h2>
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <p>Chargement des données...</p>
              ) : absences.length === 0 ? (
                <p>Aucune absence.</p>
              ) : (
                <div className="space-y-4 divide-y divide-border">
                  {absences.map((absence) => (
                    <div
                      key={absence.horaire}
                      className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                    >
                      <div className="space-y-1">
                        <div>
                          <p className="font-medium">{absence.cours}</p>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {formatDate(absence.horaire)}
                        </p>
                      </div>
                      <Badge
                        variant={absence.justifiee ? "default" : "destructive"}
                      >
                        {absence.justifiee ? "Justifiée" : "Non-justifiée"}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Affichage des retards */}
        <TabsContent value="retards">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                <h2 className="text-xl font-semibold">Retards</h2>
              </div>
            </CardHeader>
            <CardContent>
              {loading ? (
                <p>Chargement des données...</p>
              ) : retards.length === 0 ? (
                <p>Aucun retard.</p>
              ) : (
                <div className="space-y-4 divide-y divide-border">
                  {retards.map((retard) => (
                    <div
                      key={retard.horaire}
                      className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                    >
                      <div className="space-y-1">
                        <div>
                          <p className="font-medium">{retard.cours}</p>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {formatDate(retard.horaire)} | Durée : {retard.duree}
                        </p>
                      </div>
                      <Badge
                        variant={retard.justifiee ? "default" : "destructive"}
                      >
                        {retard.justifiee ? "Justifiée" : "Non-justifiée"}
                      </Badge>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
