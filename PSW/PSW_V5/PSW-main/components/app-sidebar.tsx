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
import { Eleve, MeResponse } from "@/types";

export function AppSidebar() {
  const router = useRouter();
  const [eleveData, setEleveData] = useState<Eleve>();
  const [userData, setUserData] = useState<{
    id_utilisateur: number;
    role: string;
  } | null>(null);

  useEffect(() => {
    async function fetchUserAndEleve() {
      try {
        const meRes = await fetch("/api/infoEleve/me");
        const meData = await meRes.json();
        setUserData({
          id_utilisateur: meData.id_utilisateur,
          role: meData.role,
        });

        const eleveRes = await fetch("/api/infoEleve/eleve");
        const eleves = await eleveRes.json();
        const found = eleves.find(
          (item: MeResponse) => item.id === meData.id_utilisateur
        );
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

  // Calcul initiales (si admin ou vie-scolaire, j'affiche Admin ou PS)
  const initials = eleveData
    ? `${eleveData.prenom[0]}${eleveData.nom[0]}`.toUpperCase()
    : userData?.role;

  // Liens de navigation
  const items = [
    { title: "Absences / Retards", url: "/absences/eleve", icon: Timer },
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
            <Avatar className="w-16 h-16 mt-6">
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
          </SidebarGroupLabel>
          <SidebarGroupContent className="mt-6">
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
