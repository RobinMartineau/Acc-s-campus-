namespace GestionBadgesSalles
{
    partial class FormGestionSalles
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.DataGridView dataGridViewSalles;
        private System.Windows.Forms.Button BtnAjouterSalle;
        private System.Windows.Forms.Button BtnModifierSalle;
        private System.Windows.Forms.Button BtnSupprimerSalle;

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
            this.dataGridViewSalles = new System.Windows.Forms.DataGridView();
            this.BtnAjouterSalle = new System.Windows.Forms.Button();
            this.BtnModifierSalle = new System.Windows.Forms.Button();
            this.BtnSupprimerSalle = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewSalles)).BeginInit();
            this.SuspendLayout();
            // 
            // dataGridViewSalles
            // 
            this.dataGridViewSalles.AllowUserToAddRows = false;
            this.dataGridViewSalles.AllowUserToDeleteRows = false;
            this.dataGridViewSalles.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dataGridViewSalles.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewSalles.Location = new System.Drawing.Point(12, 12);
            this.dataGridViewSalles.MultiSelect = false;
            this.dataGridViewSalles.Name = "dataGridViewSalles";
            this.dataGridViewSalles.ReadOnly = true;
            this.dataGridViewSalles.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.dataGridViewSalles.Size = new System.Drawing.Size(560, 300);
            this.dataGridViewSalles.TabIndex = 0;
            // 
            // BtnAjouterSalle
            // 
            this.BtnAjouterSalle.Location = new System.Drawing.Point(12, 330);
            this.BtnAjouterSalle.Name = "BtnAjouterSalle";
            this.BtnAjouterSalle.Size = new System.Drawing.Size(120, 40);
            this.BtnAjouterSalle.TabIndex = 1;
            this.BtnAjouterSalle.Text = "Ajouter";
            this.BtnAjouterSalle.UseVisualStyleBackColor = true;
            this.BtnAjouterSalle.Click += new System.EventHandler(this.BtnAjouterSalle_Click);
            // 
            // BtnModifierSalle
            // 
            this.BtnModifierSalle.Location = new System.Drawing.Point(150, 330);
            this.BtnModifierSalle.Name = "BtnModifierSalle";
            this.BtnModifierSalle.Size = new System.Drawing.Size(120, 40);
            this.BtnModifierSalle.TabIndex = 2;
            this.BtnModifierSalle.Text = "Modifier";
            this.BtnModifierSalle.UseVisualStyleBackColor = true;
            this.BtnModifierSalle.Click += new System.EventHandler(this.BtnModifierSalle_Click);
            // 
            // BtnSupprimerSalle
            // 
            this.BtnSupprimerSalle.Location = new System.Drawing.Point(300, 330);
            this.BtnSupprimerSalle.Name = "BtnSupprimerSalle";
            this.BtnSupprimerSalle.Size = new System.Drawing.Size(120, 40);
            this.BtnSupprimerSalle.TabIndex = 3;
            this.BtnSupprimerSalle.Text = "Supprimer";
            this.BtnSupprimerSalle.UseVisualStyleBackColor = true;
            this.BtnSupprimerSalle.Click += new System.EventHandler(this.BtnSupprimerSalle_Click);
            // 
            // FormGestionSalles
            // 
            this.ClientSize = new System.Drawing.Size(584, 391);
            this.Controls.Add(this.BtnSupprimerSalle);
            this.Controls.Add(this.BtnModifierSalle);
            this.Controls.Add(this.BtnAjouterSalle);
            this.Controls.Add(this.dataGridViewSalles);
            this.Name = "FormGestionSalles";
            this.Text = "Gestion des Salles";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewSalles)).EndInit();
            this.ResumeLayout(false);

        }
    }
}
