using System.Text.Json.Serialization;

namespace GestionBadgesSalles.Models
{
    public class Salle
    {
        [JsonPropertyName("id")]
        public int Id { get; set; }   // Identifiant unique de la salle

        [JsonPropertyName("numero")]
        public string Numero { get; set; }  // Numéro ou nom de la salle

        [JsonPropertyName("statut")]
        public bool Statut { get; set; }   // Statut de la salle (true = disponible, false = occupée)

        public override string ToString()
        {
            return $"{Numero} - {(Statut ? "Disponible" : "Occupée")}";
        }
    }
}
