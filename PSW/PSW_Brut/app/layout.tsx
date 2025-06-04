import { Inter } from "next/font/google";
import "./globals.css";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { ThemeProvider } from "@/components/theme-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "ENT",
  description: "Ent test de badges",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <ThemeProvider>
        <body className={inter.className}>
          <div className="flex">
            <SidebarProvider>
              <AppSidebar />
              <main className="flex-1">
                <SidebarTrigger />
                {children}
              </main>
            </SidebarProvider>
          </div>
        </body>
      </ThemeProvider>
    </html>
  );
}
