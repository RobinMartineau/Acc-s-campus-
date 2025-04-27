"use client";

import { useTheme } from "next-themes";
import { useState, useEffect } from "react";
import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  const buttonClasses = "flex items-center justify-center w-full px-4 py-2";

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    // Retourne bouton vide de même taille en attendant le montage
    return (
      <Button variant="ghost" aria-label="Changer le thème" className={buttonClasses}>
        <div style={{ width: 24, height: 24 }} />
      </Button>
    );
  }

  return (
    <Button
      variant="ghost"
      aria-label="Changer le thème"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className={buttonClasses}
    >
      {theme === "dark" ? <Sun className="h-6 w-6" /> : <Moon className="h-6 w-6" />}
      <span>{theme === "dark" ? "Mode clair" : "Mode sombre"}</span>
    </Button>
  );
}