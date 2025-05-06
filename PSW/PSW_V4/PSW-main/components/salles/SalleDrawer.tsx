"use client";

import { format, differenceInMinutes } from "date-fns";
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
import { SallesDetailsDrawerProps } from "@/types";

export function SallesDetailsDrawer({
  salleSelectionnee,
  dateSelectionnee,
  activite,
  onClose,
}: SallesDetailsDrawerProps) {
  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return format(date, "HH:mm");
  };

  const calculateDuration = (debut: string, fin: string) => {
    const minutes = differenceInMinutes(new Date(fin), new Date(debut));
    return `${minutes} minutes`;
  };

  let statutDisplay;
  let coursDisplay = "Aucun";

  if (activite) {
    if (activite.reservations?.length) {
      const reservation = activite.reservations[0];
      statutDisplay = `Utilisée de ${formatTime(
        reservation.horairedebut
      )} à ${formatTime(reservation.horairefin)} (${calculateDuration(
        reservation.horairedebut,
        reservation.horairefin
      )})`;
      coursDisplay = reservation.cours;
    } else if (activite.detail) {
      statutDisplay = activite.detail;
    }
  }

  return (
    <Drawer open={true} onOpenChange={(open) => !open && onClose()}>
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
            {/* Statut */}
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Statut
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                <p className="text-lg font-semibold">{statutDisplay}</p>
              </ContenuCarteInfo>
            </CarteInfo>
            {/* Cours */}
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Cours
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                <p className="text-lg font-semibold">{coursDisplay}</p>
              </ContenuCarteInfo>
            </CarteInfo>
            {/* Occupation */}
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Occupation
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                <p className="text-lg font-semibold">
                  {(activite?.nombre_utilisateurs ?? 0) + " élève(s)"}
                </p>
              </ContenuCarteInfo>
            </CarteInfo>
            {/* Liste Élèves */}
            <CarteInfo>
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium">
                  Liste Élèves
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                {activite?.utilisateurs_derniere_heure?.length ? (
                  <details>
                    <summary className="cursor-pointer text-blue-600 underline">
                      Voir la liste
                    </summary>
                    <ul className="mt-2">
                      {activite.utilisateurs_derniere_heure.map((u) => (
                        <li key={u.id}>
                          {u.prenom} {u.nom}
                        </li>
                      ))}
                    </ul>
                  </details>
                ) : (
                  <p>Aucun élève</p>
                )}
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
