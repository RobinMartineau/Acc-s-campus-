export interface Salle {
  id: number;
  nom: string;
  numero: string;
  statut: boolean;
  capacite: number;
  occupation: number;
  estUtilisee: boolean;
}

export interface Utilisateur {
  id: number;
  nom: string;
  prenom: string;
}

export interface Reservation {
  horairedebut: string;
  horairefin: string;
  cours: string;
  utilisateur: Utilisateur;
}

export interface Activite {
  reservations: Reservation[];
  utilisateurs_derniere_heure: Utilisateur[];
  nombre_utilisateurs: number;
  detail?: string;
}

export interface Absence {
  id: number;
  cours: string;
  horaire: string;
  justifiee: boolean;
  motif: string;
}

export interface Retard {
  cours: string;
  horaire: string;
  duree: number;
  justifiee: boolean;
  motif: string;
}

export interface Etudiant {
  id: number;
  nom: string;
  prenom: string;
  classe: string;
}

export interface SallesGridProps {
  salles: Salle[];
  onSelectSalle: (salle: Salle) => void;
}

export interface SallesDetailsDrawerProps {
  salleSelectionnee: Salle;
  dateSelectionnee: Date;
  activite: Activite | null;
  onClose: () => void;
  role: string | undefined;
}

export interface SallesHeaderProps {
  dateSelectionnee: Date;
  onJourPrecedent: () => void;
  onJourSuivant: () => void;
  termeRecherche: string;
  setTermeRecherche: (val: string) => void;
  filtreOccupation: string;
  setFiltreOccupation: (val: string) => void;
  onResetPage: () => void;
}

export interface SallesPaginationProps {
  pageCourante: number;
  pagesTotales: number;
  onPageChange: (nouvellePage: number) => void;
}

export interface User {
  username: string;
  id_utilisateur?: number;
  role?: string;
}

export interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
}

export interface Eleve {
  id_utilisateur: number;
  nom: string;
  prenom: string;
  classe: string;
  role: string;
}

export interface MeResponse {
  id: number;
}
