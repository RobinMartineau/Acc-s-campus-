import { NextResponse } from "next/server";
const API_URL = "http://127.0.0.1:8000/psw";

export async function GET() {
  //requete get pour récupérer les élèves
   const res = await fetch(`${API_URL}/eleve/`, {
    method: "GET",
    headers: { "Accept": "application/json" },
  });

  //si aucun eleve, renvoi tableau vide et pas d'erreur en console
  if (res.status === 404) {
    return NextResponse.json([], { status: 200 });
  }
  //si erreur, renvoi erreur
  if (!res.ok) {
    return NextResponse.error();
  }
  //si tout va bien, renvoi les données
  const data = await res.json();
  return NextResponse.json(data);
}