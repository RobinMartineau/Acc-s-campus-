using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Threading.Tasks;
using GestionBadgesSalles.Models;
using GestionBadgesSalles.Services;

namespace GestionBadgesSalles
{
    public partial class FrmListeUtilisateurs : Form
    {
        public FrmListeUtilisateurs()
        {
            InitializeComponent();
        }

        private async void FrmListeUtilisateurs_Load(object sender, EventArgs e)
        {
            // Charger la liste des utilisateurs depuis l'API
            await ChargerUtilisateurs();
        }

        private async Task ChargerUtilisateurs()
        {
            try
            {
                var utilisateurs = await ApiService.GetUtilisateursAsync();
                if (utilisateurs != null && utilisateurs.Count > 0)
                {
                    // Afficher les utilisateurs dans le DataGridView
                    dataGridViewUtilisateurs.DataSource = utilisateurs;
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
    }
}
