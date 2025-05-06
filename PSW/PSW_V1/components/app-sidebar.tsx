"use client";

import { Timer, Book, Moon, Sun, LogOut } from "lucide-react";
import { useTheme } from "@/components/theme-provider";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

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
import { Button } from "@/components/ui/button";

export function AppSidebar() {
  const { theme, toggleTheme } = useTheme();

  const items = [
    { title: "Absences / Retards", url: "/absences", icon: Timer },
    { title: "Réservations", url: "/", icon: Book },
  ];

  const handleLogout = async () => {
    try {
      const res = await fetch("/api/auth/logout", { method: "POST" });

      if (res.ok) {
        localStorage.removeItem("token");
        window.location.href = "/login";
      } else {
        console.error("Erreur lors de la déconnexion");
      }
    } catch (error) {
      console.error("Erreur réseau :", error);
    }
  };

  return (
    <Sidebar className="h-screen flex flex-col">
      <SidebarContent className="flex flex-col h-full">
        <SidebarGroup className="flex flex-col h-full justify-between">
          <SidebarGroupLabel className="flex items-center justify-center my-4">
            <Avatar>
              <AvatarImage
                alt="avatar de l'utilisateur"
                src="https://github.com/shadcn.png"
              />
              <AvatarFallback>TG</AvatarFallback>
            </Avatar>
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
          <SidebarGroupContent className="mt-auto p-4">
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild onClick={toggleTheme}>
                  <Button
                    variant="ghost"
                    aria-label="Bouton pour changer le thème de la page"
                  >
                    {theme === "dark" ? <Sun /> : <Moon />}
                    <span>
                      {theme === "dark" ? "Mode clair" : "Mode sombre"}
                    </span>
                  </Button>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarSeparator className="my-2" />
              <SidebarMenuItem>
                <SidebarMenuButton asChild onClick={handleLogout}>
                  <Button
                    variant="ghost"
                    className="text-destructive hover:text-destructive hover:bg-destructive/10"
                    aria-label="Bouton pour se déconnecter"
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
