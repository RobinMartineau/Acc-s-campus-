using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows.Forms;
using GestionBadgesSalles.Models;
using GestionBadgesSalles.Services;

namespace GestionBadgesSalles
{
    public partial class FormGestionSalles : Form
    {
        private List<Salle> listeSalles = new List<Salle>();

        public FormGestionSalles()
        {
            InitializeComponent();
            // Assure-toi que l'événement Load est bien lié
            this.Load += FormGestionSalles_Load;
        }

        private async void FormGestionSalles_Load(object sender, EventArgs e)
        {
            await ChargerSalles();
        }

        private async Task ChargerSalles()
        {
            try
            {
                listeSalles = await ApiService.GetSallesAsync();
                dataGridViewSalles.DataSource = null;
                dataGridViewSalles.DataSource = listeSalles;

                // Masquer colonne Id
                if (dataGridViewSalles.Columns["Id"] != null)
                    dataGridViewSalles.Columns["Id"].Visible = false;

                // Modifier les en-têtes
                if (dataGridViewSalles.Columns["Numero"] != null)
                    dataGridViewSalles.Columns["Numero"].HeaderText = "Numéro";

                if (dataGridViewSalles.Columns["Statut"] != null)
                    dataGridViewSalles.Columns["Statut"].HeaderText = "Disponible";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Erreur lors du chargement des salles : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private async void BtnAjouterSalle_Click(object sender, EventArgs e)
        {
            var formAjout = new FormAjouterModifierSalle();
            if (formAjout.ShowDialog() == DialogResult.OK)
            {
                await ChargerSalles();
            }
        }

        private async void BtnModifierSalle_Click(object sender, EventArgs e)
        {
            if (dataGridViewSalles.CurrentRow == null)
            {
                MessageBox.Show("Veuillez sélectionner une salle à modifier.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            var salleSelectionnee = dataGridViewSalles.CurrentRow.DataBoundItem as Salle;
            var formModif = new FormAjouterModifierSalle(salleSelectionnee);
            if (formModif.ShowDialog() == DialogResult.OK)
            {
                await ChargerSalles();
            }
        }

        private async void BtnSupprimerSalle_Click(object sender, EventArgs e)
        {
            if (dataGridViewSalles.CurrentRow == null)
            {
                MessageBox.Show("Veuillez sélectionner une salle à supprimer.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            var salleSelectionnee = dataGridViewSalles.CurrentRow.DataBoundItem as Salle;
            var confirm = MessageBox.Show($"Voulez-vous vraiment supprimer la salle {salleSelectionnee.Numero} ?", "Confirmation", MessageBoxButtons.YesNo, MessageBoxIcon.Question);

            if (confirm == DialogResult.Yes)
            {
                try
                {
                    bool success = await ApiService.SupprimerSalleAsync(salleSelectionnee.Id);
                    if (success)
                    {
                        MessageBox.Show("Salle supprimée avec succès.", "Succès", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        await ChargerSalles();
                    }
                    else
                    {
                        MessageBox.Show("Erreur lors de la suppression de la salle.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Erreur lors de la suppression de la salle : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }
    }
}
