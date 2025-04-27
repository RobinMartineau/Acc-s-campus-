import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function GET() {
  const userCookie = (await cookies()).get("user");
  if (!userCookie) {
    return NextResponse.json({ error: "Non authentifié" }, { status: 401 });
  }
  try {
    // Si cookie encodé en URI, on le décode
    const decoded = decodeURIComponent(userCookie.value);
    const user = JSON.parse(decoded);
    return NextResponse.json({
      id_utilisateur: user.id_utilisateur,
      role: user.role,
    });
  } catch (error) {
    return NextResponse.json(
      { error: `Erreur lors du parsing : ${error}` },
      { status: 500 }
    );
  }
}
