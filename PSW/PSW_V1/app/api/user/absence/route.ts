const API_URL = "http://127.0.0.1:8000";

export async function fetchAPI(endpoint:string, options: RequestInit = {}) {
    const res = await fetch(`${API_URL}${endpoint}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),  
        }
    })

    if(!res.ok){
        throw new Error(`Erreur de l'api.. ${res.statusText}̀`);
    }

    return res.json();
};

export const absence = {

    getAbsences : () => fetchAPI("/absence/"),
    
    // addAbsence : (motif: string, justifiee: boolean, id_utilisateur: number, id_edtutilisateur: number) =>
    //     fetchAPI("/absence/", {
    //         method: "POST",
    //         body: JSON.stringify({motif, justifiee, id_utilisateur, id_edtutilisateur}),
    //     }),


};