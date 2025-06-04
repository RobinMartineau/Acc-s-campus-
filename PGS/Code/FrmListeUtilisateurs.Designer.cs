namespace GestionBadgesSalles
{
    partial class FrmListeUtilisateurs
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.DataGridView dataGridViewUtilisateurs;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.dataGridViewUtilisateurs = new System.Windows.Forms.DataGridView();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewUtilisateurs)).BeginInit();
            this.SuspendLayout();
            // 
            // dataGridViewUtilisateurs
            // 
            this.dataGridViewUtilisateurs.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewUtilisateurs.Location = new System.Drawing.Point(12, 12);
            this.dataGridViewUtilisateurs.Name = "dataGridViewUtilisateurs";
            this.dataGridViewUtilisateurs.Size = new System.Drawing.Size(500, 200);
            this.dataGridViewUtilisateurs.TabIndex = 0;
            // 
            // FrmListeUtilisateurs
            // 
            this.ClientSize = new System.Drawing.Size(524, 261);
            this.Controls.Add(this.dataGridViewUtilisateurs);
            this.Name = "FrmListeUtilisateurs";
            this.Text = "Liste des Utilisateurs";
            this.Load += new System.EventHandler(this.FrmListeUtilisateurs_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewUtilisateurs)).EndInit();
            this.ResumeLayout(false);
        }
    }
}
