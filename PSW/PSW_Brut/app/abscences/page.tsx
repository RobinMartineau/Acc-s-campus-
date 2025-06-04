import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, Clock } from "lucide-react";

// Exemple de données (à remplacer par les vraies données)
const attendanceData = {
  absences: [
    { date: "2024-02-01", duration: "4h", reason: "Maladie", justified: true },
    {
      date: "2024-01-15",
      duration: "2h",
      reason: "Non justifiée",
      justified: false,
    },
    {
      date: "2023-12-05",
      duration: "8h",
      reason: "Rendez-vous médical",
      justified: true,
    },
  ],
  delays: [
    { date: "2024-02-10", duration: "15min", reason: "Retard transport" },
    { date: "2024-01-20", duration: "10min", reason: "Non justifié" },
    { date: "2023-12-12", duration: "5min", reason: "Problème de réveil" },
  ],
};

export default function AbsencesRetardsPage() {
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
              <div className="space-y-4">
                {attendanceData.absences.map((absence, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                  >
                    <div className="space-y-1">
                      <p className="font-medium">
                        {new Date(absence.date).toLocaleDateString("fr-FR")}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {absence.reason}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={absence.justified ? "default" : "destructive"}
                      >
                        {absence.justified ? "Justifiée" : "Non justifiée"}
                      </Badge>
                      <span className="text-sm font-medium">
                        {absence.duration}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
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
              <div className="space-y-4">
                {attendanceData.delays.map((delay, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                  >
                    <div className="space-y-1">
                      <p className="font-medium">
                        {new Date(delay.date).toLocaleDateString("fr-FR")}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {delay.reason}
                      </p>
                    </div>
                    <span className="text-sm font-medium">
                      {delay.duration}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
