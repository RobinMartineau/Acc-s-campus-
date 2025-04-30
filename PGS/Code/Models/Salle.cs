using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GestionBadgesSalles.Models;  // Ajoute cette ligne pour accéder à la classe Salle


namespace GestionBadgesSalles.Models
{
    public class Salle
    {
        public Guid ID { get; set; }         // Identifiant unique de la salle
        public string Nom { get; set; }      // Nom de la salle
        public bool EstDisponible { get; set; } // Indique si la salle est disponible ou non

        // Constructeur par défaut
        public Salle() { }

        // Constructeur avec paramètres
        public Salle(Guid id, string nom, bool estDisponible)
        {
            ID = id;
            Nom = nom;
            EstDisponible = estDisponible;
        }

        // Méthode pour afficher les infos de la salle
        public override string ToString()
        {
            return $"{Nom} - {(EstDisponible ? "Disponible" : "Occupée")}";
        }
    }
}
