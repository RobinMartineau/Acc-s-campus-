namespace GestionBadgesSalles
{
    partial class FormAfficherSalles
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.DataGridView dataGridViewSalles;

        /// <summary>
        /// Nettoyage des ressources utilisées.
        /// </summary>
        /// <param name="disposing">true si les ressources managées doivent être supprimées ; sinon, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Code généré par le Concepteur Windows Form

        private void InitializeComponent()
        {
            this.dataGridViewSalles = new System.Windows.Forms.DataGridView();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewSalles)).BeginInit();
            this.SuspendLayout();
            // 
            // dataGridViewSalles
            // 
            this.dataGridViewSalles.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewSalles.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridViewSalles.Location = new System.Drawing.Point(0, 0);
            this.dataGridViewSalles.Name = "dataGridViewSalles";
            this.dataGridViewSalles.RowHeadersWidth = 51;
            this.dataGridViewSalles.RowTemplate.Height = 24;
            this.dataGridViewSalles.Size = new System.Drawing.Size(800, 450);
            this.dataGridViewSalles.TabIndex = 0;
            // 
            // FormAfficherSalles
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.dataGridViewSalles);
            this.Name = "FormAfficherSalles";
            this.Text = "Liste des Salles";
            this.Load += new System.EventHandler(this.FormAfficherSalles_Load);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewSalles)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion
    }
}
