"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, Search, User } from "lucide-react";
import { eleves, absence, retard } from "@/app/api/psw/route";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

// Interfaces
interface Etudiant {
  id: number;
  nom: string;
  prenom: string;
  classe: string;
}

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

// Format de la date: "jj/mm/aaaa hh:mm"
function formatDate(date: string): string {
  const dateObj = new Date(date);
  const jour = dateObj.getDate().toString().padStart(2, "0");
  const mois = (dateObj.getMonth() + 1).toString().padStart(2, "0");
  const annee = dateObj.getFullYear();
  const heures = dateObj.getHours();
  const minutes = dateObj.getMinutes().toString().padStart(2, "0");

  return `${jour}/${mois}/${annee} ${heures}:${minutes}`;
}

// On appelle tous les APIs
async function getEtudiants(): Promise<Etudiant[]> {
  return await eleves.getEleves();
}

async function getAbsences(etudiantId: number): Promise<Absence[]> {
  return await absence.getAbsences(etudiantId);
}

async function getRetards(etudiantId: number): Promise<Retard[]> {
  return await retard.getRetards(etudiantId);
}

export default function VieScolairePage() {
  const [etudiants, setEtudiants] = useState<Etudiant[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [etudiantSelectionne, setetudiantSelectionne] =
    useState<Etudiant | null>(null);
  const [absences, setAbsences] = useState<Absence[]>([]);
  const [retards, setRetards] = useState<Retard[]>([]);
  const [loading, setLoading] = useState(false);

  // Récupération des élèves via l'API
  useEffect(() => {
    async function fetchEtudiants() {
      try {
        const data = await getEtudiants();
        setEtudiants(data);
      } catch (error) {
        console.error("Erreur lors de la récupération des élèves:", error);
      }
    }
    fetchEtudiants();
  });

  // Filtrage de recherche des étudiants
  const etudiantFiltre = etudiants.filter(
    (etudiant) =>
      etudiant.nom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      etudiant.prenom.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // On selectionne l'etudiant et lui charge ses abs/ret
  const handleSelectEtudiant = async (etudiant: Etudiant) => {
    setetudiantSelectionne(etudiant);
    setOpen(false);
    setLoading(true);

    try {
      const [absencesData, retardsData] = await Promise.all([
        getAbsences(etudiant.id),
        getRetards(etudiant.id),
      ]);
      setAbsences(absencesData);
      setRetards(retardsData);
    } catch (error) {
      console.error("Erreur lors de la récupération des données:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold mb-6">Gestion Vie Scolaire</h1>
      <Card className="mb-6">
        <CardHeader>
          <div className="flex items-center gap-2">
            <User className="h-5 w-5" />
            <h2 className="text-xl font-semibold">Rechercher un étudiant</h2>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-4">
            <Popover open={open} onOpenChange={setOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  role="combobox"
                  aria-expanded={open}
                  className="w-full justify-between"
                >
                  {etudiantSelectionne
                    ? `${etudiantSelectionne.prenom} ${etudiantSelectionne.nom} (${etudiantSelectionne.classe})`
                    : "Rechercher un étudiant..."}
                  <Search className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-full p-0" align="start">
                <Command>
                  <CommandInput
                    placeholder="Rechercher par nom ou prénom..."
                    value={searchQuery}
                    onValueChange={setSearchQuery}
                  />
                  <CommandList>
                    <CommandEmpty>Aucun étudiant trouvé</CommandEmpty>
                    <CommandGroup>
                      {etudiantFiltre.map((etudiant) => (
                        <CommandItem
                          key={etudiant.id}
                          value={`${etudiant.prenom} ${etudiant.nom}`}
                          onSelect={() => handleSelectEtudiant(etudiant)}
                        >
                          <span>
                            {etudiant.prenom} {etudiant.nom}
                          </span>
                          <span className="ml-2 text-sm text-muted-foreground">
                            {etudiant.classe}
                          </span>
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>
          </div>
        </CardContent>
      </Card>

      {etudiantSelectionne && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <h2 className="text-2xl font-semibold">
              {etudiantSelectionne.prenom} {etudiantSelectionne.nom}
            </h2>
            <Badge variant="outline">{etudiantSelectionne.classe}</Badge>
          </div>

          <Tabs defaultValue="absences" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="absences">Absences</TabsTrigger>
              <TabsTrigger value="retards">Retards</TabsTrigger>
            </TabsList>

            {/* Affichage des absences */}
            <TabsContent value="absences">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="h-5 w-5" />
                      <h2 className="text-xl font-semibold">Absences</h2>
                    </div>
                    <Badge variant="outline">Total : {absences.length}</Badge>
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
                            <p className="font-medium">{absence.cours}</p>
                            <p className="text-sm text-muted-foreground">
                              {formatDate(absence.horaire)}
                            </p>
                          </div>
                          <Badge
                            variant={
                              absence.justifiee ? "default" : "destructive"
                            }
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
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="h-5 w-5" />
                      <h2 className="text-xl font-semibold">Retards</h2>
                    </div>
                    <Badge variant="outline">Total : {absences.length}</Badge>
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
                              {formatDate(retard.horaire)} | Durée :{" "}
                              {retard.duree}
                            </p>
                          </div>
                          <Badge
                            variant={
                              retard.justifiee ? "default" : "destructive"
                            }
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
      )}
    </div>
  );
}
