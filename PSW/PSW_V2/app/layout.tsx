import "./globals.css";
import { ThemeProvider } from "next-themes";
import { AuthProvider } from "@/context/AuthContext";
import LayoutClient from "@/components/layout-client";

// Définition des métadonnées du site (titre et description)
export const metadata = {
  title: "PSW",
  description: "PSW BTS Ciel",
};

// Fonction principale qui gère la structure de la page (le layout)
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <AuthProvider>
        <body className="font-sans">
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <LayoutClient>{children}</LayoutClient>
          </ThemeProvider>
        </body>
      </AuthProvider>
    </html>
  );
}
