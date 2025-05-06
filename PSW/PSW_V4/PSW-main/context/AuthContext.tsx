"use client";
import { createContext, useContext, useState } from "react";
import { AuthContextType, User } from "@/types";
// Définition des interfaces User et AuthContextType

// Création du contexte d'authentification
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Composant AuthProvider pour gérer l'état de l'utilisateur
export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  // Fonction "login" pour se connecter avec comme paramètre le nom de l'util et son mot de passe
  const login = async (
    username: string,
    password: string
  ): Promise<boolean> => {
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });

      // Si requete reussie on recuperer l'ID et le role de l'utilisateur sinon false
      if (res.ok) {
        const data = await res.json();
        setUser({
          username,
          id_utilisateur: data.id_utilisateur,
          role: data.role,
        });
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error("Erreur lors de la connexion :", error);
      return false;
    }
  };

  // Fournit le contexte d'auth avec l'utilisateur et la fonction de connexion à tous les composants enfants
  return (
    <AuthContext.Provider value={{ user, login }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook personnalisé pour utiliser le contexte d'auth
export const useAuth = () => {
  const context = useContext(AuthContext);

  // Si le contexte n'est pas disponible (par exemple si useAuth est utilisé en dehors du AuthProvider), alors on pose une erreur
  if (!context) {
    throw new Error("useAuth n'est pas dans un AuthProvider");
  }
  return context;
};
