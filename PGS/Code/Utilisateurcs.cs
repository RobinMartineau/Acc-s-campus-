using System;
using System.Text.Json.Serialization;


public class Utilisateur
{
    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("nom")]
    public string Nom { get; set; }

    [JsonPropertyName("prenom")]
    public string Prenom { get; set; }

    [JsonPropertyName("identifiant")]
    public string Identifiant { get; set; }

    [JsonPropertyName("role")]
    public string Role { get; set; }

    [JsonPropertyName("mot_de_passe")]
    public string MotDePasse { get; set; }

    [JsonPropertyName("date_de_naissance")]
    public DateTime? DateDeNaissance { get; set; }

    [JsonPropertyName("id_classe")]
    public int? IdClasse { get; set; }
}
