namespace GestionBadgesSalles
{
    partial class FormAssocierBadge
    {
        private System.Windows.Forms.ComboBox comboBoxBadges;
        private System.Windows.Forms.ComboBox comboBoxUtilisateurs;
        private System.Windows.Forms.Button BtnAssocier;
        private System.Windows.Forms.Button BtnDesassocier;
        private System.Windows.Forms.CheckBox checkBoxIsActive;


        // La méthode InitializeComponent qui initialise les composants
        private void InitializeComponent()
        {
            this.comboBoxBadges = new System.Windows.Forms.ComboBox();
            this.comboBoxUtilisateurs = new System.Windows.Forms.ComboBox();
            this.BtnAssocier = new System.Windows.Forms.Button();
            this.BtnDesassocier = new System.Windows.Forms.Button();
            this.checkBoxIsActive = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // 
            // comboBoxBadges
            // 
            this.comboBoxBadges.FormattingEnabled = true;
            this.comboBoxBadges.Location = new System.Drawing.Point(12, 12);
            this.comboBoxBadges.Name = "comboBoxBadges";
            this.comboBoxBadges.Size = new System.Drawing.Size(200, 21);
            this.comboBoxBadges.TabIndex = 0;
            // 
            // comboBoxUtilisateurs
            // 
            this.comboBoxUtilisateurs.FormattingEnabled = true;
            this.comboBoxUtilisateurs.Location = new System.Drawing.Point(12, 50);
            this.comboBoxUtilisateurs.Name = "comboBoxUtilisateurs";
            this.comboBoxUtilisateurs.Size = new System.Drawing.Size(200, 21);
            this.comboBoxUtilisateurs.TabIndex = 1;
            // 
            // BtnAssocier
            // 
            this.BtnAssocier.Location = new System.Drawing.Point(12, 90);
            this.BtnAssocier.Name = "BtnAssocier";
            this.BtnAssocier.Size = new System.Drawing.Size(200, 23);
            this.BtnAssocier.TabIndex = 2;
            this.BtnAssocier.Text = "Associer";
            this.BtnAssocier.UseVisualStyleBackColor = true;
            this.BtnAssocier.Click += new System.EventHandler(this.BtnAssocier_Click);
            // 
            // BtnDesassocier
            // 
            this.BtnDesassocier.Location = new System.Drawing.Point(12, 130);
            this.BtnDesassocier.Name = "BtnDesassocier";
            this.BtnDesassocier.Size = new System.Drawing.Size(200, 23);
            this.BtnDesassocier.TabIndex = 3;
            this.BtnDesassocier.Text = "Désassocier";
            this.BtnDesassocier.UseVisualStyleBackColor = true;
            this.BtnDesassocier.Click += new System.EventHandler(this.BtnDesassocier_Click);
            // 
            // checkBoxIsActive
            // 
            this.checkBoxIsActive.AutoSize = true;
            this.checkBoxIsActive.Location = new System.Drawing.Point(30, 180);
            this.checkBoxIsActive.Name = "checkBoxIsActive";
            this.checkBoxIsActive.Size = new System.Drawing.Size(81, 17);
            this.checkBoxIsActive.TabIndex = 4;
            this.checkBoxIsActive.Text = "Badge Actif";
            this.checkBoxIsActive.UseVisualStyleBackColor = true;
            // 
            // FormAssocierBadge
            // 
            this.ClientSize = new System.Drawing.Size(224, 161);
            this.Controls.Add(this.BtnDesassocier);
            this.Controls.Add(this.BtnAssocier);
            this.Controls.Add(this.comboBoxUtilisateurs);
            this.Controls.Add(this.comboBoxBadges);
            this.Controls.Add(this.checkBoxIsActive);
            this.Name = "FormAssocierBadge";
            this.Text = "Associer Badge";
            this.Load += new System.EventHandler(this.FrmAssocierBadge_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }
    }
}
