"use client";

import { User, Timer, Book, Moon, Sun } from "lucide-react";
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
} from "@/components/ui/sidebar";
import { Button } from "./ui/button";

export function AppSidebar() {
  const { theme, toggleTheme } = useTheme();

  const items = [
    { title: "Profil", url: "/profil", icon: User },
    { title: "Absences / Retards", url: "/abscences", icon: Timer },
    { title: "Réservations", url: "/", icon: Book },
  ];

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
                  <Button aria-label="Bouton pour changer le thème de la page">
                    {theme === "dark" ? <Sun /> : <Moon />}
                    <span>
                      {theme === "dark" ? "Mode clair" : "Mode sombre"}
                    </span>
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
