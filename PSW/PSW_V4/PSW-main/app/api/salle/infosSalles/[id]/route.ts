import { NextResponse } from "next/server";
const API_URL = "http://127.0.0.1:8000/psw";

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const { id } = await Promise.resolve(params);
  /// Requête GET pour récupérer les informations de la salle
  const res = await fetch(`${API_URL}/salle/${id}/activite`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  const data = await res.json();
  // Si aucune activité trouvée, renvoie reponse de l'api
  if (res.status === 404) {
    return NextResponse.json(data, { status: 200 });
  }

  // Si erreur, renvoie erreur
  if (!res.ok) {
    return NextResponse.error();
  }

  // Si tout va bien, récup et renvoie données
  return NextResponse.json(data);
}
