using System;
using System.Text.Json.Serialization;

namespace GestionBadgesSalles.Models
{
    public class Badge
    {
        [JsonPropertyName("uid")]
        public string UID { get; set; }

        [JsonPropertyName("utilisateur_id")]
        public Guid UtilisateurID { get; set; }

        [JsonPropertyName("date_creation")]
        public DateTime DateCreation { get; set; }

        // ✅ AJOUT DE LA PROPRIÉTÉ ACTIF
        [JsonPropertyName("actif")]
        public bool Actif { get; set; }

        // ✅ ToString pour affichage dans ComboBox
        public override string ToString()
        {
            return $"{UID} - {(Actif ? "Actif" : "Inactif")}";
        }
    }
}
