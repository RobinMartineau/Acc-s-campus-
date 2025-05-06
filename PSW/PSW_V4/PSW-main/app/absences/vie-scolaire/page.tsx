"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, Search, User, MoveLeft } from "lucide-react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Absence, Retard, Etudiant } from "@/types";
import { format } from "date-fns";

function formatDate(date: string): string {
  return format(new Date(date), "dd/MM/yyyy HH:mm");
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

  // Récupération des élèves via API
  useEffect(() => {
    async function fetchEtudiants() {
      try {
        const response = await fetch("/api/infoEleve/eleve");
        const data = await response.json();
        setEtudiants(data);
      } catch (error) {
        console.error("Erreur lors de la récupération des élèves:", error);
      }
    }
    fetchEtudiants();
  }, []);

  // Filtrage de recherche
  const etudiantFiltre = etudiants.filter(
    (etudiant) =>
      etudiant.nom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      etudiant.prenom.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Fonct° pour recup absences/retards
  const fetchAbsencesRetards = async (id?: number) => {
    setLoading(true);
    try {
      const [absRes, retRes] = await Promise.all([
        fetch(`/api/infoEleve/absence/${id}`),
        fetch(`/api/infoEleve/retard/${id}`),
      ]);
      const absData = await absRes.json();
      const retData = await retRes.json();

      setAbsences(absData);
      setRetards(retData);
    } catch (error) {
      console.error("Erreur lors de la récupération des données:", error);
    } finally {
      setLoading(false);
    }
  };

  // quand eleve selectionne
  const handleSelectEtudiant = async (etudiant: Etudiant) => {
    setetudiantSelectionne(etudiant);
    setOpen(false);
    await fetchAbsencesRetards(etudiant.id);
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

            {!etudiantSelectionne && (
              <div className="mt-4">
                <h3 className="text-sm font-medium mb-2">Liste des élèves</h3>
                <div className="border rounded-md max-h-60 overflow-y-auto">
                  {etudiants.length === 0 ? (
                    <div className="p-4 text-center text-muted-foreground">
                      Chargement des élèves...
                    </div>
                  ) : (
                    <div className="divide-y">
                      {etudiants.map((etudiant) => (
                        <div
                          key={etudiant.id}
                          className="p-3 hover:bg-muted/50 cursor-pointer"
                          onClick={() => handleSelectEtudiant(etudiant)}
                        >
                          <div className="flex justify-between items-center">
                            <span>
                              {etudiant.prenom} {etudiant.nom}
                            </span>
                            <span className="text-sm text-muted-foreground">
                              {etudiant.classe}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {etudiantSelectionne && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setetudiantSelectionne(null)}
              className="mr-2"
            >
              <MoveLeft className="mr-1 h-4 w-4" />
              Retour
            </Button>
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
                      {absences.map((absence, index) => (
                        <div
                          key={`${absence.horaire}-${index}`}
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
                    <Badge variant="outline">Total : {retards.length}</Badge>
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
