using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;
using GestionBadgesSalles.Helpers;  // Pour AppSettings si tu l'utilises
using System.Text.Json;             // Pour JsonSerializer
using GestionBadgesSalles.Models;   // Pour accéder à Salle, Utilisateur, Badge
using System.Windows.Forms;         // Pour MessageBox

namespace GestionBadgesSalles.Services
{
    public class ApiService
    {
        // URL de base de l'API (à modifier si besoin en HTTPS)
        private static readonly string baseUrl = "http://api.campus.local/";

        private static readonly HttpClient client = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(10)
        };

        // 🔹 Ajouter un badge
        public static async Task<bool> AjouterBadge(string uid, int? utilisateurId = null)
        {
            string url = $"{baseUrl}badge/";

            var badgeData = new Dictionary<string, object>
            {
                { "uid", uid },
                { "dateCreation", DateTime.UtcNow }
            };

            if (utilisateurId.HasValue && utilisateurId.Value > 0)
            {
                badgeData.Add("utilisateurId", utilisateurId.Value);
            }

            try
            {
                HttpResponseMessage response = await client.PostAsJsonAsync(url, badgeData);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur ajout badge : {ex.Message}");
                return false;
            }
        }

        // 🔹 Supprimer un badge
        public static async Task<bool> DeleteBadgeAsync(string uid)
        {
            string url = $"{baseUrl}badge/{uid}";

            try
            {
                HttpResponseMessage response = await client.DeleteAsync(url);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur suppression badge : {ex.Message}");
                return false;
            }
        }

        // 🔹 Modifier état d’un badge (actif/inactif)
        public static async Task<bool> ModifierEtatBadgeAsync(string uid, bool isActive)
        {
            string url = $"{baseUrl}pgs/badge/";

            var updateData = new
            {
                uid = uid,
                actif = isActive
            };

            try
            {
                HttpResponseMessage response = await client.PutAsJsonAsync(url, updateData);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur modification état badge : {ex.Message}");
                return false;
            }
        }

        // 🔹 Récupérer la liste des utilisateurs
        public static async Task<List<Utilisateur>> GetUtilisateursAsync()
        {
            string url = $"{baseUrl}pgs/utilisateur";

            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                string json = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                    return new List<Utilisateur>();

                return JsonSerializer.Deserialize<List<Utilisateur>>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
                    ?? new List<Utilisateur>();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur récupération utilisateurs : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return new List<Utilisateur>();
            }
        }

        // 🔹 Récupérer la liste des salles
        public static async Task<List<Salle>> GetSallesAsync()
        {
            string url = $"{baseUrl}salle/";

            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                string json = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                    return new List<Salle>();

                return JsonSerializer.Deserialize<List<Salle>>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
                    ?? new List<Salle>();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur récupération salles : {ex.Message}");
                return new List<Salle>();
            }
        }

        // 🔹 Supprimer une salle
        public static async Task<bool> SupprimerSalleAsync(int id)
        {
            string url = $"{baseUrl}salle/{id}";

            try
            {
                HttpResponseMessage response = await client.DeleteAsync(url);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur suppression salle : {ex.Message}");
                return false;
            }
        }

        // 🔹 Associer un badge à un utilisateur
        public static async Task<bool> AssocierBadgeAUtilisateur(int utilisateurId, string uidBadge)
        {
            string url = $"{baseUrl}pgs/associer/utilisateur/{utilisateurId}/badge/{uidBadge}";

            var associerData = new
            {
                uid = uidBadge,
                id_utilisateur = utilisateurId
            };

            try
            {
                HttpResponseMessage response = await client.PutAsJsonAsync(url, associerData);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur association badge/utilisateur : {ex.Message}");
                return false;
            }
        }

        // 🔹 Désassocier un badge d'un utilisateur
        public static async Task<bool> DesassocierBadgeDUtilisateur(string uid, int utilisateurId)
        {
            string url = $"{baseUrl}pgs/dissocier/utilisateur/{utilisateurId}/badge/{uid}";

            var desassocierData = new
            {
                uid = uid,
                id_utilisateur = utilisateurId
            };

            try
            {
                HttpResponseMessage response = await client.PutAsJsonAsync(url, desassocierData);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur désassociation badge/utilisateur : {ex.Message}");
                return false;
            }
        }

        // 🔹 Récupérer tous les badges
        public static async Task<List<Badge>> GetBadgesFromApiAsync()
        {
            string url = $"{baseUrl}badge/";

            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                string json = await response.Content.ReadAsStringAsync();

                if (!response.IsSuccessStatusCode)
                    return new List<Badge>();

                return JsonSerializer.Deserialize<List<Badge>>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
                    ?? new List<Badge>();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur récupération badges : {ex.Message}");
                return new List<Badge>();
            }
        }
    }
}
