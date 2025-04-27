import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

const SECRET_KEY = process.env.JWT_SECRET || "supersecret";

const hashedPassword = bcrypt.hashSync("demo", 10);

const fakeUsers: Record<string, { username: string; password: string }> = {
  demo: {
    username: "Thomas",
    password: hashedPassword, 
  },
};

const generateToken = (username: string) => {
  return jwt.sign({ username }, SECRET_KEY, { expiresIn: "1h" });
};

export async function POST(req: Request) {
  try {
    const { username, password } = await req.json();
    const user = fakeUsers[username];

    if (!user || !bcrypt.compareSync(password, user.password)) {
      return NextResponse.json({ error: "Identifiant ou mot de passe incorrect" }, { status: 401 });
    }

    const token = generateToken(username);

    (await cookies()).set("token", token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 3600,
    });

    return NextResponse.json({ message: "Connexion réussie" });
  } catch (error) {
    console.error("Erreur serveur :", error);
    return NextResponse.json({ error: "Erreur serveur" }, { status: 500 });
  }
}
