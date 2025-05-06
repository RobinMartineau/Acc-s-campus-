"use client";

import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { usePathname } from "next/navigation";

export default function LayoutClient({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isLoginPage = pathname === "/login";

  return (
    <div className="flex">
      <SidebarProvider>
        {!isLoginPage && <AppSidebar />}
        <main className="flex-1">
          {!isLoginPage && <SidebarTrigger />}
          {children}
        </main>
      </SidebarProvider>
    </div>
  );
}
