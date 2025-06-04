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
import { ScrollArea } from "@/components/ui/scroll-area";
import type { SallesDetailsDrawerProps } from "@/types";
import { User, Clock } from "lucide-react";

export function SallesDetailsDrawer({
  salleSelectionnee,
  dateSelectionnee,
  activite,
  onClose,
  role,
}: SallesDetailsDrawerProps) {
  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return format(date, "HH:mm");
  };

  let statutDisplay;
  let coursDisplay = "Aucun";

  if (activite) {
    if (activite.reservations?.length) {
      const now = new Date();
      const reservationTriee = [...activite.reservations].sort(
        (a, b) =>
          new Date(a.horairedebut).getTime() -
          new Date(b.horairedebut).getTime()
      );

      let reservationActuelle = reservationTriee[0];
      for (let index = 0; index < reservationTriee.length; index++) {
        if (new Date(reservationTriee[index].horairedebut) > now) {
          reservationActuelle = reservationTriee[index];
          break;
        }
      }

      statutDisplay = `Utilisée de ${formatTime(
        reservationActuelle.horairedebut
      )} à ${formatTime(reservationActuelle.horairefin)}`;
      coursDisplay = reservationActuelle.cours;
    } else if (activite.detail) {
      statutDisplay = activite.detail;
    }
  }

  const futureReservation = (activite?.reservations ?? [])
    .filter((reservation) => new Date(reservation.horairedebut) > new Date())
    .sort(
      (a, b) =>
        new Date(a.horairedebut).getTime() - new Date(b.horairedebut).getTime()
    );

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
                <p className="text-lg font-semibold">
                  {statutDisplay || "Disponible"}
                </p>
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

            {/* Futures réservations */}
            <CarteInfo className="col-span-1 md:col-span-2">
              <EnteteCarteInfo className="pb-2">
                <TitreCarteInfo className="text-sm font-medium flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  Futures réservations
                </TitreCarteInfo>
              </EnteteCarteInfo>
              <ContenuCarteInfo>
                {futureReservation.length > 0 ? (
                  <ScrollArea className="h-[120px] w-full pr-4">
                    <div className="space-y-3">
                      {futureReservation.map((reservation, index) => (
                        <div
                          key={index}
                          className="flex justify-between border-b pb-2"
                        >
                          <div>
                            <p className="font-medium">{reservation.cours}</p>
                            <p className="text-sm text-muted-foreground">
                              {reservation.utilisateur.prenom}{" "}
                              {reservation.utilisateur.nom}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="font-medium">
                              {formatTime(reservation.horairedebut)} -{" "}
                              {formatTime(reservation.horairefin)}
                            </p>
                            <p>
                              {" "}
                              {format(
                                reservation.horairedebut,
                                "dd MMMM yyyy",
                                {
                                  locale: fr,
                                }
                              )}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                ) : (
                  <p className="text-muted-foreground">
                    Aucune réservation future
                  </p>
                )}
              </ContenuCarteInfo>
            </CarteInfo>

            {/* Liste Élèves */}
            {role !== "Eleve" ? (
              <CarteInfo className="col-span-1 md:col-span-2">
                <EnteteCarteInfo className="pb-2">
                  <TitreCarteInfo className="text-sm font-medium flex items-center gap-2">
                    <User className="h-4 w-4" />
                    Liste Élèves ({activite?.nombre_utilisateurs ?? 0})
                  </TitreCarteInfo>
                </EnteteCarteInfo>
                <ContenuCarteInfo>
                  {(activite?.utilisateurs_derniere_heure ?? []).length > 0 ? (
                    <ScrollArea className="h-[120px] w-full pr-4">
                      <div className="space-y-2">
                        {activite?.utilisateurs_derniere_heure.map((u) => (
                          <div
                            key={u.id}
                            className="flex items-center gap-2 border-b pb-2"
                          >
                            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted">
                              <User className="h-4 w-4" />
                            </div>
                            <div>
                              <p className="font-medium">
                                {u.prenom} {u.nom}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>
                  ) : (
                    <p className="text-muted-foreground">
                      Aucun élève présent actuellement
                    </p>
                  )}
                </ContenuCarteInfo>
              </CarteInfo>
            ) : (
              ""
            )}
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
