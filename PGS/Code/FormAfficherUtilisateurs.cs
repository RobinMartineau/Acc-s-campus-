using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Forms;
using GestionBadgesSalles.Models;
using GestionBadgesSalles.Services;

namespace GestionBadgesSalles
{
    public partial class FormAfficherUtilisateurs : Form
    {
        public FormAfficherUtilisateurs()
        {
            InitializeComponent();
        }

        private async void FormAfficherUtilisateurs_Load(object sender, EventArgs e)
        {
            await ChargerUtilisateurs();
        }

        private async Task ChargerUtilisateurs()
        {
            try
            {
                // On récupère la liste des utilisateurs via le service API
                List<Utilisateur> utilisateurs = await ApiService.GetUtilisateursAsync();
                // On lie les données à la grille
                dataGridViewUtilisateurs.DataSource = utilisateurs;
            }
            catch (Exception ex)
            {
                // Gestion des erreurs
                MessageBox.Show($"Erreur lors du chargement des utilisateurs : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void dataGridViewUtilisateurs_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }
    }
}
