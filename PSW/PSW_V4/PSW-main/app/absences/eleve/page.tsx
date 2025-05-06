"use client"; // Indique que c'est une utilisat° coté navigateur

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, Clock } from "lucide-react";
import { useEffect, useState } from "react";
import { Absence, Retard } from "@/types";
import { format } from "date-fns";

function formatDate(date: string): string {
  return format(new Date(date), "dd/MM/yyyy HH:mm");
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
        const user = await fetch("/api/infoEleve/me");
        const { id_utilisateur } = await user.json();

        // On appelle l'API des absences avec le bon id
        const [absRes, retRes] = await Promise.all([
          fetch(`/api/infoEleve/absence/${id_utilisateur}`),
          fetch(`/api/infoEleve/retard/${id_utilisateur}`),
        ]);
        const absData = await absRes.json();
        const retData = await retRes.json();

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
                  {absences.map((absence, index) => (
                    <div
                      key={`${absence.horaire}-${index}`}
                      className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                    >
                      <div className="space-y-1">
                        <div>
                          {absence.motif == null ? (
                            <p>{absence.cours} | Motif : Aucun motif</p>
                          ) : (
                            <p>
                              {absence.cours} | Motif : {absence.motif}
                            </p>
                          )}
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
                  {retards.map((retard, index) => (
                    <div
                      key={`${retard.horaire}-${index}`}
                      className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                    >
                      <div className="space-y-1">
                        <div>
                          {retard.motif == null ? (
                            <p>{retard.cours} | Motif : Aucun motif</p>
                          ) : (
                            <p>
                              {retard.cours} | Motif : {retard.motif}
                            </p>
                          )}
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
