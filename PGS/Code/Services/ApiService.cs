using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;
using GestionBadgesSalles.Helpers;  // Pour AppSettings
using System.Text.Json;             // Pour JsonSerializer
using GestionBadgesSalles.Models;   // Pour accéder à Salle, Utilisateur, Badge
using System.Windows.Forms;         // Pour MessageBox

namespace GestionBadgesSalles.Services
{
    public class ApiService
    {
        private static readonly HttpClient client = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(10)
        };

        // 🔹 Ajouter un badge
        public static async Task<bool> AjouterBadge(string uid, int utilisateurId)
        {
            string url = "http://192.168.30.3:8000/badge/";

            var badgeData = new
            {
                UID = uid,
                UtilisateurID = utilisateurId,
                DateCreation = DateTime.UtcNow
            };

            try
            {
                Console.WriteLine($"📤 Envoi de la requête à : {url}");
                Console.WriteLine($"📨 Données envoyées : {JsonSerializer.Serialize(badgeData)}");

                HttpResponseMessage response = await client.PostAsJsonAsync(url, badgeData);
                string responseContent = await response.Content.ReadAsStringAsync();

                Console.WriteLine($"📥 Réponse HTTP {(int)response.StatusCode} : {responseContent}");

                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"🚨 Exception lors de l'ajout du badge : {ex.Message}");
                return false;
            }
        }

        // 🔹 Supprimer un badge
        public static async Task<bool> DeleteBadgeAsync(string uid)
        {
            string url = $"http://192.168.30.3:8000/badge/{uid}";

            try
            {
                HttpResponseMessage response = await client.DeleteAsync(url);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"🚨 Erreur lors de la suppression du badge : {ex.Message}");
                return false;
            }
        }

        // 🔹 Modifier l'état actif/inactif d'un badge
        public static async Task<bool> ModifierEtatBadgeAsync(string uid, bool isActive)
        {
            string url = $"http://192.168.30.3:8000/badge/{uid}";

            var updateData = new
            {
                Etat = isActive ? "actif" : "inactif"
            };

            try
            {
                HttpResponseMessage response = await client.PutAsJsonAsync(url, updateData);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"🚨 Erreur lors de la mise à jour du badge : {ex.Message}");
                return false;
            }
        }

        // 🔹 Récupérer la liste des utilisateurs
        public static async Task<List<Utilisateur>> GetUtilisateursAsync()
        {
            string url = "http://192.168.30.3:8000/pgs/utilisateur";

            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                string responseContent = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    return JsonSerializer.Deserialize<List<Utilisateur>>(responseContent,
                        new JsonSerializerOptions { PropertyNameCaseInsensitive = true }) ?? new List<Utilisateur>();
                }
                else
                {
                    return new List<Utilisateur>();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de la récupération des utilisateurs : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return new List<Utilisateur>();
            }
        }

        // 🔹 Récupérer la liste des salles
        public static async Task<List<Salle>> RecupererSallesAsync()
        {
            string url = "http://192.168.30.3:8000/salles";

            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                string responseContent = await response.Content.ReadAsStringAsync();

                return response.IsSuccessStatusCode
                    ? JsonSerializer.Deserialize<List<Salle>>(responseContent) ?? new List<Salle>()
                    : new List<Salle>();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de la récupération des salles : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return new List<Salle>();
            }
        }

        // 🔹 Associer un badge à un utilisateur (PUT avec JSON)
        public static async Task<bool> AssocierBadgeAUtilisateur(int utilisateurId, string uidBadge)
        {
            string url = $"http://192.168.30.3:8000/pgs/associer/utilisateur/{utilisateurId}/badge/{uidBadge}";

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
                Console.WriteLine($"🚨 Erreur lors de l'association du badge : {ex.Message}");
                return false;
            }
        }

        // 🔹 Désassocier un badge d'un utilisateur (PUT avec JSON)
        public static async Task<bool> DesassocierBadgeDUtilisateur(string uid, int utilisateurId)
        {
            string url = $"http://192.168.30.3:8000/pgs/dissocier/utilisateur/{utilisateurId}/badge/{uid}";

            var desassocierData = new
            {
                uid = uid,
                id_utilisateur = utilisateurId
            };

            try
            {
                HttpResponseMessage response = await client.PutAsJsonAsync(url, desassocierData);

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine($"✅ Badge {uid} désassocié de l'utilisateur {utilisateurId} avec succès !");
                    return true;
                }
                else
                {
                    string responseContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine($"❌ Erreur lors de la désassociation : {response.StatusCode} - {responseContent}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"🚨 Exception : {ex.Message}");
                return false;
            }
        }

        // 🔹 Récupérer tous les badges
        public static async Task<List<Badge>> GetBadgesFromApiAsync()
        {
            string url = "http://192.168.30.3:8000/badge/";

            try
            {
                HttpResponseMessage response = await client.GetAsync(url);
                string responseContent = await response.Content.ReadAsStringAsync();

                return response.IsSuccessStatusCode
                    ? JsonSerializer.Deserialize<List<Badge>>(responseContent) ?? new List<Badge>()
                    : new List<Badge>();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Erreur lors de la récupération des badges : {ex.Message}");
                return new List<Badge>();
            }
        }
    }
}
