using System;
using System.Windows.Forms;
using GestionBadgesSalles.Models;

namespace GestionBadgesSalles
{
    public partial class FormAjouterModifierSalle : Form
    {
        public Salle SalleModifiee { get; private set; }

        public FormAjouterModifierSalle()
        {
            InitializeComponent();
            SalleModifiee = new Salle();
        }

        public FormAjouterModifierSalle(Salle salle) : this()
        {
            SalleModifiee = salle;
            txtNomSalle.Text = salle.Numero; // 🔧 Remplacé 'Nom' par 'Numero'
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtNomSalle.Text))
            {
                MessageBox.Show("Le nom de la salle est obligatoire.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            SalleModifiee.Numero = txtNomSalle.Text.Trim(); // 🔧 Remplacé 'Nom' par 'Numero'
            this.DialogResult = DialogResult.OK;
            this.Close();
        }

        private void btnAnnuler_Click(object sender, EventArgs e)
        {
            this.DialogResult = DialogResult.Cancel;
            this.Close();
        }
    }
}
