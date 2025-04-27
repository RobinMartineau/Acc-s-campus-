import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import jwt from "jsonwebtoken";

export const dynamic = "force-dynamic";


const SECRET_KEY = process.env.JWT_SECRET || "supersecret";

export async function GET() {
  try {
    const token = (await cookies()).get("token")?.value;
    if (!token) {
      return NextResponse.json({ error: "Non autorisé" }, { status: 401 });
    }

    const decoded = jwt.verify(token, SECRET_KEY) as { username: string };
    
    return NextResponse.json({ username: decoded.username });
  } catch (error) {
    console.error("Erreur de vérification du token:", error);
    
    return NextResponse.json({ error: "Session invalide ou expirée" }, { status: 403 });
  }
}
