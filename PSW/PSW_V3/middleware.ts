import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(req: NextRequest) {
  const userCookie = req.cookies.get("user")?.value;
  const { pathname } = req.nextUrl;

  console.log("Middleware exécuté pour :", pathname);
  console.log("Cookie 'user' reçu :", userCookie);

  if (!userCookie) {
    console.log("Cookie 'user' absent, redirection vers /login");
    return NextResponse.redirect(new URL("/login", req.url));
  }

  try {
    const user = JSON.parse(userCookie);
    if (
      pathname.startsWith("/absences/vie-scolaire") &&
      user.role === "Eleve"
    ) {
      return NextResponse.redirect(new URL("/absences/eleve", req.url));
    }
    if (pathname.startsWith("/absences/eleve") && user.role !== "Eleve") {
      return NextResponse.redirect(new URL("/absences/vie-scolaire", req.url));
    }
  } catch (error) {
    console.error("Erreur lors du parsing du cookie 'user' :", error);
    return NextResponse.redirect(new URL("/login", req.url));
  }

  console.log("Cookie 'user' valide, accès autorisé :", pathname);
  return NextResponse.next();
}

export const config = {
  matcher: ["/absences/:path*", "/"],
};
