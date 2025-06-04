using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Forms;
using GestionBadgesSalles.Models;
using GestionBadgesSalles.Services;

namespace GestionBadgesSalles
{
    public partial class FormAssocierBadge : Form
    {
        private List<Badge> badges; // Liste des badges
        private List<Utilisateur> utilisateurs; // Liste des utilisateurs

        public FormAssocierBadge()
        {
            InitializeComponent();
            this.Load += FrmAssocierBadge_Load;
        }

        // Lors du chargement du formulaire, récupérer les badges et utilisateurs
        private async void FrmAssocierBadge_Load(object sender, EventArgs e)
        {
            await ChargerBadges();
            await ChargerUtilisateurs();
        }

        // Charger les badges depuis l'API
        private async Task ChargerBadges()
        {
            try
            {
                badges = await ApiService.GetBadgesFromApiAsync();
                comboBoxBadges.Items.Clear();

                foreach (var badge in badges)
                {
                    comboBoxBadges.Items.Add(badge.UID.ToString());
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors du chargement des badges : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Charger les utilisateurs depuis l'API
        private async Task ChargerUtilisateurs()
        {
            try
            {
                utilisateurs = await ApiService.GetUtilisateursAsync();
                comboBoxUtilisateurs.Items.Clear();

                foreach (var utilisateur in utilisateurs)
                {
                    comboBoxUtilisateurs.Items.Add($"{utilisateur.Nom} {utilisateur.Prenom}");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors du chargement des utilisateurs : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // ✅ Associer un badge à un utilisateur
        private async void BtnAssocier_Click(object sender, EventArgs e)
        {
            if (comboBoxBadges.SelectedItem == null || comboBoxUtilisateurs.SelectedItem == null)
            {
                MessageBox.Show("Veuillez sélectionner un badge et un utilisateur.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            string selectedBadgeUID = comboBoxBadges.SelectedItem.ToString();
            string selectedUtilisateurNomComplet = comboBoxUtilisateurs.SelectedItem.ToString();

            // Trouver les objets correspondants
            var badge = badges.Find(b => b.UID.ToString() == selectedBadgeUID);
            var utilisateur = utilisateurs.Find(u => $"{u.Nom} {u.Prenom}" == selectedUtilisateurNomComplet);

            if (badge == null || utilisateur == null)
            {
                MessageBox.Show("Badge ou utilisateur introuvable.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                // Appel correct de la méthode AssocierBadgeAUtilisateur avec les bons types
                bool success = await ApiService.AssocierBadgeAUtilisateur(utilisateur.Id, badge.UID);

                MessageBox.Show(
                    success ? "✅ Badge associé à l'utilisateur avec succès !" : "❌ Échec de l'association du badge.",
                    success ? "Succès" : "Erreur",
                    MessageBoxButtons.OK,
                    success ? MessageBoxIcon.Information : MessageBoxIcon.Error
                );
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de l'association : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Désassocier un badge d'un utilisateur
        private async void BtnDesassocier_Click(object sender, EventArgs e)
        {
            string selectedBadge = comboBoxBadges.SelectedItem?.ToString();
            string selectedUtilisateur = comboBoxUtilisateurs.SelectedItem?.ToString();

            if (string.IsNullOrEmpty(selectedBadge) || string.IsNullOrEmpty(selectedUtilisateur))
            {
                MessageBox.Show("Veuillez sélectionner un badge et un utilisateur.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                var badge = badges.Find(b => b.UID.ToString() == selectedBadge);
                var utilisateur = utilisateurs.Find(u => $"{u.Nom} {u.Prenom}" == selectedUtilisateur);

                if (badge != null && utilisateur != null)
                {
                    // Désassociation du badge
                    bool success = await ApiService.DesassocierBadgeDUtilisateur(badge.UID.ToString(), utilisateur.Id);
                    MessageBox.Show(success ? "Badge désassocié avec succès!" : "Erreur lors de la désassociation du badge.",
                                    success ? "Succès" : "Erreur",
                                    MessageBoxButtons.OK,
                                    success ? MessageBoxIcon.Information : MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors de la désassociation du badge : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // Modifier l'état actif d'un badge
        private async void BtnModifierEtatBadge_Click(object sender, EventArgs e)
        {
            string selectedBadge = comboBoxBadges.SelectedItem?.ToString();
            bool isActive = checkBoxIsActive.Checked;

            if (string.IsNullOrEmpty(selectedBadge))
            {
                MessageBox.Show("Veuillez sélectionner un badge.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                bool success = await ApiService.ModifierEtatBadgeAsync(selectedBadge, isActive);
                MessageBox.Show(success ? "L'état du badge a été modifié avec succès!" : "Erreur lors de la modification de l'état du badge.",
                                success ? "Succès" : "Erreur",
                                MessageBoxButtons.OK,
                                success ? MessageBoxIcon.Information : MessageBoxIcon.Error);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
