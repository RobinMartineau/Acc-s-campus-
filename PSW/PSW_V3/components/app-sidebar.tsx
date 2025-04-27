"use client";

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

export function AppSidebar() {

  const router = useRouter();
  const { user } = useAuth();

  const absencesUrl =
    user?.role === "Eleve" ? "/absences/eleve" : "/absences/vie-scolaire";

  const items = [
    { title: "Absences / Retards", url: absencesUrl, icon: Timer },
    { title: "Réservations", url: "/", icon: Book },
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
              <AvatarFallback>TG</AvatarFallback>
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
