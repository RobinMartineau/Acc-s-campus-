using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Threading.Tasks;
using GestionBadgesSalles.Services;
using GestionBadgesSalles.Models;
using GestionBadgesSalles.Helpers;
using System.Net.Http;

namespace GestionBadgesSalles
{
    public partial class FrmGestionBadgesSalles : Form
    {
        private string dernierUIDScanne = string.Empty;
        private static readonly HttpClient client = new HttpClient();

        public FrmGestionBadgesSalles()
        {
            InitializeComponent();
        }

        private async void FrmGestionBadgesSalles_Load(object sender, EventArgs e)
        {
            await ChargerUtilisateurs();
            await LoadBadges();
        }

        private async Task ChargerUtilisateurs()
        {
            try
            {
                var utilisateurs = await ApiService.GetUtilisateursAsync();
                if (utilisateurs != null && utilisateurs.Count > 0)
                {
                    foreach (var utilisateur in utilisateurs)
                    {
                        if (utilisateur != null)
                        {
                            Console.WriteLine($"Utilisateur : ID = {utilisateur.Id}, Nom = {utilisateur.Nom}, Prénom = {utilisateur.Prenom}, Rôle = {utilisateur.Role}");
                        }
                    }
                }
                else
                {
                    MessageBox.Show("Aucun utilisateur trouvé.", "Avertissement", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors du chargement des utilisateurs : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private async Task LoadBadges()
        {
            try
            {
                var badges = await ApiService.GetBadgesFromApiAsync();
                comboBoxBadges.Items.Clear();

                if (badges == null || badges.Count == 0)
                {
                    MessageBox.Show("Aucun badge trouvé.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    return;
                }

                foreach (var badge in badges)
                {
                    if (badge != null && !string.IsNullOrEmpty(badge.UID))
                    {
                        comboBoxBadges.Items.Add(badge.UID);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors du chargement des badges : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private async void BtnScanner_Click(object sender, EventArgs e)
        {
            try
            {
                string uid = await NFCReader.LireUIDNFCAsync();
                if (!string.IsNullOrEmpty(uid))
                {
                    dernierUIDScanne = uid;
                    txtUID.Text = uid;
                    MessageBox.Show($"Badge détecté : {uid}", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("Aucun badge détecté !", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors du scan du badge : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private async void BtnAjouter_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(dernierUIDScanne))
            {
                MessageBox.Show("Veuillez scanner un badge avant d'ajouter.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                // Associer un utilisateur (ici on passe l'ID utilisateur comme int)
                var utilisateurId = 1; // À remplacer par l'ID réel de l'utilisateur

                bool success = await ApiService.AjouterBadge(dernierUIDScanne, utilisateurId); // Ici on passe un int au lieu d'un Guid
                MessageBox.Show(success ? "Badge ajouté avec succès !" : "Erreur lors de l'ajout du badge.", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information);

                if (success)
                {
                    await LoadBadges();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de l'ajout du badge : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private async void BtnSupprimerBadge_Click(object sender, EventArgs e)
        {
            var badgeUid = comboBoxBadges.SelectedItem?.ToString();
            if (string.IsNullOrEmpty(badgeUid))
            {
                MessageBox.Show("Veuillez sélectionner un badge à supprimer.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                bool success = await ApiService.DeleteBadgeAsync(badgeUid);
                if (success)
                {
                    MessageBox.Show("Badge supprimé avec succès.", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    await LoadBadges();
                }
                else
                {
                    MessageBox.Show("Erreur lors de la suppression du badge.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de la suppression du badge : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private async void BtnModifierEtatBadge_Click(object sender, EventArgs e)
        {
            var badgeUid = comboBoxBadges.SelectedItem?.ToString();
            if (string.IsNullOrEmpty(badgeUid))
            {
                MessageBox.Show("Veuillez sélectionner un badge à modifier.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                bool isActive = checkBoxIsActive.Checked;

                bool success = await ApiService.ModifierEtatBadgeAsync(badgeUid, isActive);
                if (success)
                {
                    MessageBox.Show("État du badge modifié avec succès.", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("Erreur lors de la modification de l'état du badge.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de la modification de l'état du badge : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void dataGridViewSalles_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            // À implémenter si nécessaire
        }

        private void BtnVoirSalles_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Afficher les salles ici.", "Info", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private async void btnRafraichir_Click(object sender, EventArgs e)
        {
            await LoadBadges();
        }

        private void BtnAssocierBadge_Click(object sender, EventArgs e)
        {
            FormAssocierBadge associerForm = new FormAssocierBadge();
            associerForm.ShowDialog();
        }

        private void BtnAfficherUtilisateurs_Click(object sender, EventArgs e)
        {
            FormAfficherUtilisateurs form = new FormAfficherUtilisateurs();
            form.ShowDialog();
        }

        private void comboBoxUtilisateurs_SelectedIndexChanged(object sender, EventArgs e)
        {
            // À implémenter si nécessaire
        }
    }
}
