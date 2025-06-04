namespace GestionBadgesSalles
{
    partial class FormAjouterModifierSalle
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Label lblNom;
        private System.Windows.Forms.TextBox txtNomSalle;
        private System.Windows.Forms.Button btnOK;
        private System.Windows.Forms.Button btnAnnuler;

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
            this.lblNom = new System.Windows.Forms.Label();
            this.txtNomSalle = new System.Windows.Forms.TextBox();
            this.btnOK = new System.Windows.Forms.Button();
            this.btnAnnuler = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // lblNom
            // 
            this.lblNom.AutoSize = true;
            this.lblNom.Location = new System.Drawing.Point(12, 15);
            this.lblNom.Name = "lblNom";
            this.lblNom.Size = new System.Drawing.Size(79, 15);
            this.lblNom.TabIndex = 0;
            this.lblNom.Text = "Nom de salle :";
            // 
            // txtNomSalle
            // 
            this.txtNomSalle.Location = new System.Drawing.Point(97, 12);
            this.txtNomSalle.Name = "txtNomSalle";
            this.txtNomSalle.Size = new System.Drawing.Size(210, 23);
            this.txtNomSalle.TabIndex = 1;
            // 
            // btnOK
            // 
            this.btnOK.Location = new System.Drawing.Point(151, 50);
            this.btnOK.Name = "btnOK";
            this.btnOK.Size = new System.Drawing.Size(75, 25);
            this.btnOK.TabIndex = 2;
            this.btnOK.Text = "OK";
            this.btnOK.UseVisualStyleBackColor = true;
            this.btnOK.Click += new System.EventHandler(this.btnOK_Click);
            // 
            // btnAnnuler
            // 
            this.btnAnnuler.Location = new System.Drawing.Point(232, 50);
            this.btnAnnuler.Name = "btnAnnuler";
            this.btnAnnuler.Size = new System.Drawing.Size(75, 25);
            this.btnAnnuler.TabIndex = 3;
            this.btnAnnuler.Text = "Annuler";
            this.btnAnnuler.UseVisualStyleBackColor = true;
            this.btnAnnuler.Click += new System.EventHandler(this.btnAnnuler_Click);
            // 
            // FormAjouterModifierSalle
            // 
            this.ClientSize = new System.Drawing.Size(319, 87);
            this.Controls.Add(this.btnAnnuler);
            this.Controls.Add(this.btnOK);
            this.Controls.Add(this.txtNomSalle);
            this.Controls.Add(this.lblNom);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Name = "FormAjouterModifierSalle";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Ajouter / Modifier Salle";
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
