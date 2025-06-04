namespace GestionBadgesSalles
{
    partial class FormAfficherUtilisateurs
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
            this.dataGridViewUtilisateurs.AllowUserToAddRows = false;
            this.dataGridViewUtilisateurs.AllowUserToDeleteRows = false;
            this.dataGridViewUtilisateurs.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewUtilisateurs.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridViewUtilisateurs.Location = new System.Drawing.Point(0, 0);
            this.dataGridViewUtilisateurs.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.dataGridViewUtilisateurs.Name = "dataGridViewUtilisateurs";
            this.dataGridViewUtilisateurs.ReadOnly = true;
            this.dataGridViewUtilisateurs.Size = new System.Drawing.Size(600, 366);
            this.dataGridViewUtilisateurs.TabIndex = 0;
            this.dataGridViewUtilisateurs.CellContentClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridViewUtilisateurs_CellContentClick);
            // 
            // FormAfficherUtilisateurs
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(600, 366);
            this.Controls.Add(this.dataGridViewUtilisateurs);
            this.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.Name = "FormAfficherUtilisateurs";
            this.Text = "Liste des Utilisateurs";
            this.Load += new System.EventHandler(this.FormAfficherUtilisateurs_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewUtilisateurs)).EndInit();
            this.ResumeLayout(false);

        }
    }
}
