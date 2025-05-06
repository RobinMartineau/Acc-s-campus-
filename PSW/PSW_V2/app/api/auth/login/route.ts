import { NextResponse } from "next/server";
import { cookies } from "next/headers";

// URL de l'API pour l'authentification
const API_URL = "http://localhost:8000/psw/login/";

export async function POST(req: Request) {
  try {
    // Récupération des données envoyées par l'utilisateur
    const { username, password } = await req.json();

    // Création du body de la requête pour l'API
    const body_req = {
      identifiant: username,
      mot_de_passe: password,
    };

    // Envoi de la requête à l'API pour vérifier les identifiants
    const Response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body_req),
    });

    // Vérification si erreur (mauvais identifiants)
    if (!Response.ok) {
      const errorBody = await Response.json();
      return NextResponse.json(
        { error: errorBody.error || "Identifiant ou mot de passe incorrect" },
        { status: 401 }
      );
    }

    // Récup données de la réponse
    const data = await Response.json();

    // Vérification si connexion bien réussi
    if (!data.success) {
      return NextResponse.json(
        { error: "Identifiant ou mot de passe incorrect" },
        { status: 401 }
      );
    }

    // Créer objet utilisateur avec ID et rôle
    const user = {
      id_utilisateur: data.id_utilisateur,
      role: data.role,
    };

    // Création cookie pour stocker informations utilisateur
    (await cookies()).set("user", JSON.stringify(user), {
      httpOnly: true, // Empêche l'accès au cookie via JS côté client
      sameSite: "strict", // Empêche l'envoi du cookie avec des requêtes tierces
      maxAge: 3600, // Durée de validité du cookie (1 heure)
    });

    // Réponse si reussite
    return NextResponse.json({ message: "Connexion réussie" });
  } catch (error) {
    // Gestion des erreurs serveur
    console.error("Erreur serveur :", error);
    return NextResponse.json({ error: "Erreur serveur" }, { status: 500 });
  }
}
