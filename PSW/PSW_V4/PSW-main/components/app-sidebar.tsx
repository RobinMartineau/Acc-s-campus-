"use client";

import { useState, useEffect } from "react";
import { Timer, Book, LogOut } from "lucide-react";
import { ThemeSwitcher } from "@/components/ThemeSwitcher";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarSeparator,
} from "@/components/ui/sidebar";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";
import { Eleve, MeResponse } from "@/types";

export function AppSidebar() {
  const router = useRouter();
  const { user } = useAuth();
  const [eleveData, setEleveData] = useState<Eleve>();

  useEffect(() => {
    async function fetchUserAndEleve() {
      try {
        const meRes = await fetch("/api/infoEleve/me");
        const meData = await meRes.json();
        console.log("Utilisateur connecté:", meData);
        const eleveRes = await fetch("/api/infoEleve/eleve");
        const eleves = await eleveRes.json();
        console.log("Liste des élèves:", eleves);
        const found = eleves.find(
          (item: MeResponse) => item.id === meData.id_utilisateur
        );
        console.log("Élève trouvé:", found);
        setEleveData(found || null);
      } catch (error) {
        console.error(
          "Erreur lors de la récupération des données utilisateur:",
          error
        );
      }
    }
    fetchUserAndEleve();
  }, []);

  // Calcul initiales (si admin ou vie-scolaire, j'affiche rien)
  const initials = eleveData
    ? `${eleveData.prenom[0]}${eleveData.nom[0]}`.toUpperCase()
    : "";

  const absencesUrl =
    user?.role === "Eleve" ? "/absences/eleve" : "/absences/vie-scolaire";

  // Liens de navigation
  const items = [
    { title: "Absences / Retards", url: absencesUrl, icon: Timer },
    { title: "Salles de cours", url: "/", icon: Book },
  ];

  const handleLogout = async () => {
    try {
      const res = await fetch("/api/auth/logout", { method: "POST" });
      if (res.ok) {
        router.push("/login");
      } else {
        console.error("Erreur lors de la déconnexion");
      }
    } catch (error) {
      console.error("Erreur réseau lors de la déconnexion :", error);
    }
  };

  return (
    <Sidebar className="h-screen flex flex-col">
      <SidebarContent className="flex flex-col h-full">
        <div className="sr-only">
          <h2>Menu de navigation</h2>
          <p>Accédez aux différentes sections du site</p>
        </div>
        <SidebarGroup className="flex flex-col h-full justify-between">
          <SidebarGroupLabel className="flex items-center justify-center my-4">
            <Avatar>
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <Link href={item.url} prefetch={true}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
          <SidebarGroupContent className="mt-auto p-4">
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <ThemeSwitcher />
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarSeparator className="my-2" />
              <SidebarMenuItem>
                <SidebarMenuButton asChild onClick={handleLogout}>
                  <Button
                    variant="ghost"
                    className="text-destructive hover:text-destructive hover:bg-destructive/10"
                    aria-label="Se déconnecter"
                  >
                    <LogOut />
                    <span>Se déconnecter</span>
                  </Button>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
