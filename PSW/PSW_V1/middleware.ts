import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { jwtVerify } from "jose";

const SECRET_KEY = process.env.JWT_SECRET || "supersecret";

async function verifyToken(token: string) {
    try {
        const secret = new TextEncoder().encode(SECRET_KEY);
        const { payload } = await jwtVerify(token, secret);
        return payload;
    } catch (err) {
        return null;
    }
}

export async function middleware(req: NextRequest) {
    const token = req.cookies.get("token")?.value;
    const { pathname } = req.nextUrl;

    console.log("Middleware exécuté pour :", pathname);
    console.log("Token reçu :", token);

    if (!token) {
        console.log("Aucun token, redirection vers /login");
        return NextResponse.redirect(new URL("/login", req.url));
    }

    const decoded = await verifyToken(token);

    if (!decoded) {
        console.log("Token invalide, redirection vers /login");
        return NextResponse.redirect(new URL("/login", req.url));
    }

    console.log("Token valide, accès autorisé :", pathname);
    return NextResponse.next();
}

export const config = {
    matcher: ["/", "/absences", "/reservations"],
};
