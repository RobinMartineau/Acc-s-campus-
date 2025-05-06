import { NextResponse } from "next/server";

const API_URL = "http://127.0.0.1:8000/psw";

export async function GET(request: Request, context: { params: { id: string } }) {
  const { id } = await Promise.resolve(context.params);
  //requete get pour récupérer les retards avec en param l'id' de l'eleve  
  const res = await fetch(`${API_URL}/retard/${id}`, {
    method: "GET",
    headers: { "Accept": "application/json" },
  });
  
  //si aucun retard, renvoi tableau vide et pas d'erreur en console
  if (res.status === 404) return NextResponse.json([], { status: 200 });

  //si erreur, renvoie erreur
  if (!res.ok) return NextResponse.error();
  
  //sinon renvoi reponse
  const data = await res.json();
  return NextResponse.json(data);
}