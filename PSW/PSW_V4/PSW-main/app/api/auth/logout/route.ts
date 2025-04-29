import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function POST() {
  // Supprime le cookie "user" pour déconnecter l'utilisateur
  (await cookies()).delete("user");
  
  // Renvoie une réponse indiquant que la déconnexion est un succès
  return NextResponse.json({ message: "Déconnexion réussie" }, { status: 200 });
}
