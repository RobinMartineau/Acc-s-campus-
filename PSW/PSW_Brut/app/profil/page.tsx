import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { CalendarDays, Mail, Phone, School } from "lucide-react";

// Exemple de données (à remplacer par les vraies données)
const studentData = {
  firstName: "Thomas",
  lastName: "Gasche",
  email: "thomas.gasche@gmail.com",
  phone: "+33 6 10 49 81 73",
  studentId: "2024-4256",
  class: "BTS CIEL",
  year: "2ème année",
  promotion: "2024-2025",
  specialization: "Informatique et réseaux",
  birthDate: "14/10/2005",
  address: "Angers",
  emergencyContact: "Madame Gasche (Mère) - 06 66 66 66 66",
  currentSemester: "Semestre 4",
  overallGrade: "14.5/20",
  credits: {
    earned: 90,
    total: 120,
  },
  upcomingEvents: [
    { name: "Examen de Réseau", date: "2025-03-15" },
    { name: "Présentation Projet", date: "2025-06-02" },
  ],
};

export default function ProfilePage() {
  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold mb-6">Profil Étudiant</h1>

      <div className="grid gap-6 md:grid-cols-[300px_1fr]">
        <div className="space-y-6">
          <Card>
            <CardContent className="p-6 flex flex-col items-center space-y-4">
              <Avatar className="h-32 w-32">
                <AvatarImage
                  src="https://github.com/shadcn.png"
                  alt="Photo de profil"
                />
                <AvatarFallback>
                  {studentData.firstName[0]}
                  {studentData.lastName[0]}
                </AvatarFallback>
              </Avatar>
              <h2 className="text-xl font-semibold">
                {studentData.firstName} {studentData.lastName}
              </h2>
              <Badge variant="secondary">{studentData.specialization}</Badge>
              <Separator />
              <div className="w-full space-y-4">
                <div className="flex items-center gap-2">
                  <School className="h-4 w-4 opacity-70" />
                  <span className="text-sm">{studentData.year}</span>
                </div>
                <div className="flex items-center gap-2">
                  <CalendarDays className="h-4 w-4 opacity-70" />
                  <span className="text-sm">
                    Promotion {studentData.promotion}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 opacity-70" />
                  <span className="text-sm break-all">{studentData.email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 opacity-70" />
                  <span className="text-sm">{studentData.phone}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold">
                Informations personnelles
              </h3>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm text-muted-foreground">
                  Date de naissance
                </p>
                <p className="font-medium">{studentData.birthDate}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Adresse</p>
                <p className="font-medium">{studentData.address}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">
                  Contact d&apos;urgence
                </p>
                <p className="font-medium">{studentData.emergencyContact}</p>
              </div>
            </CardContent>
          </Card>
        </div>
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <h2 className="text-xl font-semibold">
                Informations académiques
              </h2>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              <div>
                <p className="text-sm text-muted-foreground">Numéro étudiant</p>
                <p className="font-medium">{studentData.studentId}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Classe</p>
                <p className="font-medium">{studentData.class}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">
                  Semestre en cours
                </p>
                <p className="font-medium">{studentData.currentSemester}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">
                  Moyenne générale
                </p>
                <p className="font-medium">{studentData.overallGrade}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold">Progression académique</h3>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">Crédits obtenus</span>
                  <span className="text-sm font-medium">
                    {studentData.credits.earned}/{studentData.credits.total}
                  </span>
                </div>
                <Progress
                  value={
                    (studentData.credits.earned / studentData.credits.total) *
                    100
                  }
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold">Événements à venir</h3>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {studentData.upcomingEvents.map((event, index) => (
                  <div
                    key={index}
                    className="flex justify-between items-center"
                  >
                    <span>{event.name}</span>
                    <Badge variant="outline">
                      {new Date(event.date).toLocaleDateString("fr-FR")}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
