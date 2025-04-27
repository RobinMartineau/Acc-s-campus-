"use client";

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, Clock } from "lucide-react";
import { absence } from "@/app/api/user/absence/route";
import { retard } from "@/app/api/user/retard/route";
import { useEffect, useState } from "react";

interface Absence {
  id: number;
  motif: string;
  justifiee: boolean;
  id_utilisateur: number;
  id_edtutilisateur: number;
}

interface Retard {
  id: number;
  duree: number;
  motif: string;
  justifiee: boolean;
  id_utilisateur: number;
  id_edtutilisateur: number;
}

export default function AbsencesRetardsPage() {
  const [absences, setAbsences] = useState<Absence[]>([]);
  const [retards, setRetards] = useState<Retard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [absData, retData] = await Promise.all([
          absence.getAbsences(),
          retard.getRetards(),
        ]);
        setAbsences(absData);
        setRetards(retData);
      } catch (error) {
        console.error("Erreur au chargement des absences, raison : ", error);
      } finally {
        setLoading(false);
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
                      key={absence.id}
                      className="flex items-center justify-between p-3"
                    >
                      <div className="space-y-1">
                        <p className="font-medium">{absence.motif}</p>
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
              ) : absences.length === 0 ? (
                <p>Aucun retard.</p>
              ) : (
                <div className="space-y-4">
                  {retards.map((retard) => (
                    <div
                      key={retard.id}
                      className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                    >
                      <div className="space-y-1">
                        <p className="font-medium">{retard.motif}</p>
                      </div>
                      <Badge
                        variant={retard.justifiee ? "default" : "destructive"}
                      >
                        {retard.justifiee ? "Justifié" : "Non-justifié"}
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
