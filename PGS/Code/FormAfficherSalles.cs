using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Forms;
using GestionBadgesSalles.Models;
using GestionBadgesSalles.Services;

namespace GestionBadgesSalles
{
    public partial class FormAfficherSalles : Form
    {
        private List<Salle> listeSalles = new List<Salle>();

        public FormAfficherSalles()
        {
            InitializeComponent();
            this.Load += FormAfficherSalles_Load; // Assure que l'événement est bien attaché
        }

        private async void FormAfficherSalles_Load(object sender, EventArgs e)
        {
            await ChargerSallesAsync();
        }

        private async Task ChargerSallesAsync()
        {
            try
            {
                listeSalles = await ApiService.GetSallesAsync();

                // Vérifie que le DataGridView existe bien dans le Designer
                if (dataGridViewSalles != null)
                {
                    dataGridViewSalles.DataSource = null;
                    dataGridViewSalles.DataSource = listeSalles;

                    // Vérifie que les colonnes existent bien
                    if (dataGridViewSalles.Columns.Contains("Id"))
                        dataGridViewSalles.Columns["Id"].HeaderText = "ID";

                    if (dataGridViewSalles.Columns.Contains("Nom"))
                        dataGridViewSalles.Columns["Nom"].HeaderText = "Nom de la Salle";
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors du chargement des salles : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
