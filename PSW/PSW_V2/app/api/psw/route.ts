const API_URL = "http://127.0.0.1:8000"; // URL de base de l'API

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  // Effectue une requête à l'API avec l'URL complète
  const res = await fetch(`${API_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  // Vérifie si la requête est un succès
  if (!res.ok) {
    throw new Error(`Erreur de l'API : ${res.statusText}`);
  }

  return res.json(); // Renvoie la réponse en JSON
}

// On récupère ici les absences, retards et la liste des élèves
export const absence = {
  getAbsences: (id: number) => fetchAPI(`/psw/absence/${id}`),
};

export const retard = {
  getRetards: (id: number) => fetchAPI(`/psw/absence/${id}`),
};

export const eleves = {
  getEleves: () => fetchAPI("/psw/eleve"),
};
