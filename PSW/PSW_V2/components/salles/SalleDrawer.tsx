"use client";

import { format } from "date-fns";
import { fr } from "date-fns/locale";
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerDescription,
  DrawerFooter,
  DrawerClose,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";
import {
  Card as CarteInfo,
  CardContent as ContenuCarteInfo,
  CardHeader as EnteteCarteInfo,
  CardTitle as TitreCarteInfo,
} from "@/components/ui/card";

interface Salle {
  id: number;
  nom: string;
  capacite: number;
  occupation: number;
  estUtilisee: boolean;
}

interface SallesDetailsDrawerProps {
  salleSelectionnee: Salle;
  dateSelectionnee: Date;
  obtenirPourcentageOccupation: (salle: Salle) => number;
  obtenirCouleurOccupation: (salle: Salle) => string;
  onClose: () => void;
}

export function SallesDetailsDrawer({
  salleSelectionnee,
  dateSelectionnee,
  obtenirPourcentageOccupation,
  obtenirCouleurOccupation,
  onClose,
}: SallesDetailsDrawerProps) {
  return (
    <Drawer open={true} onOpenChange={(ouvert) => !ouvert && onClose()}>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>{salleSelectionnee.nom}</DrawerTitle>
          <DrawerDescription>
            Détails de l&apos;occupation pour le{" "}
            {format(dateSelectionnee, "dd MMMM yyyy", { locale: fr })}
          </DrawerDescription>
        </DrawerHeader>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Statut
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                <p className="text-lg font-semibold">
                  {salleSelectionnee.estUtilisee
                    ? "En utilisation"
                    : "Disponible"}
                </p>
              </ContenuCarteInfo>
            </CarteInfo>
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Capacité
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                <p className="text-lg font-semibold">
                  {salleSelectionnee.capacite} personnes
                </p>
              </ContenuCarteInfo>
            </CarteInfo>
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Occupation actuelle
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                <p className="text-lg font-semibold">
                  {salleSelectionnee.occupation} personnes
                </p>
              </ContenuCarteInfo>
            </CarteInfo>
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Taux d&apos;occupation
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                <>
                  <p className="text-lg font-semibold">
                    {Math.round(
                      obtenirPourcentageOccupation(salleSelectionnee)
                    )}
                    %
                  </p>
                  <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden mb-6">
                    <div
                      className={`h-full ${obtenirCouleurOccupation(
                        salleSelectionnee
                      )}`}
                      style={{
                        width: `${obtenirPourcentageOccupation(
                          salleSelectionnee
                        )}%`,
                      }}
                    ></div>
                  </div>
                </>
              </ContenuCarteInfo>
            </CarteInfo>
          </div>
        </div>
        <DrawerFooter>
          <DrawerClose asChild>
            <Button variant="outline">Fermer</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}
