namespace GestionBadgesSalles
{
    partial class FrmGestionBadgesSalles
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Label lblUID;
        private System.Windows.Forms.TextBox txtUID;
        private System.Windows.Forms.Button BtnScanner;
        private System.Windows.Forms.Button BtnAjouter;
        private System.Windows.Forms.Button BtnVoirSalles;
        private System.Windows.Forms.ComboBox comboBoxBadges;
        private System.Windows.Forms.Label lblListeBadges;
        private System.Windows.Forms.CheckBox chkActif;
        private System.Windows.Forms.Button BtnModifierEtatBadge;
        private System.Windows.Forms.Button BtnSupprimerBadge;
        private System.Windows.Forms.Button btnRafraichir;
        private System.Windows.Forms.Button BtnAfficherUtilisateurs;
        private System.Windows.Forms.Button BtnAssocierBadge;
        private System.Windows.Forms.ComboBox comboBoxUtilisateurs; // Ajouté ComboBox pour les utilisateurs
        private System.Windows.Forms.CheckBox checkBoxIsActive;

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
            this.lblUID = new System.Windows.Forms.Label();
            this.txtUID = new System.Windows.Forms.TextBox();
            this.BtnScanner = new System.Windows.Forms.Button();
            this.BtnAjouter = new System.Windows.Forms.Button();
            this.BtnVoirSalles = new System.Windows.Forms.Button();
            this.comboBoxBadges = new System.Windows.Forms.ComboBox();
            this.lblListeBadges = new System.Windows.Forms.Label();
            this.chkActif = new System.Windows.Forms.CheckBox();
            this.BtnModifierEtatBadge = new System.Windows.Forms.Button();
            this.BtnSupprimerBadge = new System.Windows.Forms.Button();
            this.btnRafraichir = new System.Windows.Forms.Button();
            this.BtnAfficherUtilisateurs = new System.Windows.Forms.Button();
            this.BtnAssocierBadge = new System.Windows.Forms.Button();
            this.comboBoxUtilisateurs = new System.Windows.Forms.ComboBox();
            this.checkBoxIsActive = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // 
            // lblUID
            // 
            this.lblUID.AutoSize = true;
            this.lblUID.Location = new System.Drawing.Point(17, 21);
            this.lblUID.Name = "lblUID";
            this.lblUID.Size = new System.Drawing.Size(29, 13);
            this.lblUID.TabIndex = 0;
            this.lblUID.Text = "UID:";
            // 
            // txtUID
            // 
            this.txtUID.Location = new System.Drawing.Point(121, 17);
            this.txtUID.Name = "txtUID";
            this.txtUID.ReadOnly = true;
            this.txtUID.Size = new System.Drawing.Size(200, 20);
            this.txtUID.TabIndex = 1;
            // 
            // BtnScanner
            // 
            this.BtnScanner.Location = new System.Drawing.Point(337, 16);
            this.BtnScanner.Name = "BtnScanner";
            this.BtnScanner.Size = new System.Drawing.Size(75, 23);
            this.BtnScanner.TabIndex = 2;
            this.BtnScanner.Text = "Scanner";
            this.BtnScanner.UseVisualStyleBackColor = true;
            this.BtnScanner.Click += new System.EventHandler(this.BtnScanner_Click);
            // 
            // BtnAjouter
            // 
            this.BtnAjouter.Location = new System.Drawing.Point(427, 15);
            this.BtnAjouter.Name = "BtnAjouter";
            this.BtnAjouter.Size = new System.Drawing.Size(75, 23);
            this.BtnAjouter.TabIndex = 3;
            this.BtnAjouter.Text = "Ajouter";
            this.BtnAjouter.UseVisualStyleBackColor = true;
            this.BtnAjouter.Click += new System.EventHandler(this.BtnAjouter_Click);
            // 
            // BtnVoirSalles
            // 
            this.BtnVoirSalles.Location = new System.Drawing.Point(524, 238);
            this.BtnVoirSalles.Name = "BtnVoirSalles";
            this.BtnVoirSalles.Size = new System.Drawing.Size(100, 23);
            this.BtnVoirSalles.TabIndex = 4;
            this.BtnVoirSalles.Text = "Voir Salles";
            this.BtnVoirSalles.UseVisualStyleBackColor = true;
            this.BtnVoirSalles.Click += new System.EventHandler(this.BtnVoirSalles_Click);
            // 
            // comboBoxBadges
            // 
            this.comboBoxBadges.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxBadges.FormattingEnabled = true;
            this.comboBoxBadges.Location = new System.Drawing.Point(105, 115);
            this.comboBoxBadges.Name = "comboBoxBadges";
            this.comboBoxBadges.Size = new System.Drawing.Size(200, 21);
            this.comboBoxBadges.TabIndex = 6;
            // 
            // lblListeBadges
            // 
            this.lblListeBadges.AutoSize = true;
            this.lblListeBadges.Location = new System.Drawing.Point(12, 115);
            this.lblListeBadges.Name = "lblListeBadges";
            this.lblListeBadges.Size = new System.Drawing.Size(87, 13);
            this.lblListeBadges.TabIndex = 7;
            this.lblListeBadges.Text = "Liste des badges";
            // 
            // chkActif
            // 
            this.chkActif.AutoSize = true;
            this.chkActif.Location = new System.Drawing.Point(194, 244);
            this.chkActif.Name = "chkActif";
            this.chkActif.Size = new System.Drawing.Size(47, 17);
            this.chkActif.TabIndex = 8;
            this.chkActif.Text = "Actif";
            // 
            // BtnModifierEtatBadge
            // 
            this.BtnModifierEtatBadge.Location = new System.Drawing.Point(524, 267);
            this.BtnModifierEtatBadge.Name = "BtnModifierEtatBadge";
            this.BtnModifierEtatBadge.Size = new System.Drawing.Size(100, 23);
            this.BtnModifierEtatBadge.TabIndex = 9;
            this.BtnModifierEtatBadge.Text = "Modifier État";
            this.BtnModifierEtatBadge.UseVisualStyleBackColor = true;
            this.BtnModifierEtatBadge.Click += new System.EventHandler(this.BtnModifierEtatBadge_Click);
            // 
            // BtnSupprimerBadge
            // 
            this.BtnSupprimerBadge.Location = new System.Drawing.Point(524, 15);
            this.BtnSupprimerBadge.Name = "BtnSupprimerBadge";
            this.BtnSupprimerBadge.Size = new System.Drawing.Size(100, 23);
            this.BtnSupprimerBadge.TabIndex = 10;
            this.BtnSupprimerBadge.Text = "Supprimer";
            this.BtnSupprimerBadge.UseVisualStyleBackColor = true;
            this.BtnSupprimerBadge.Click += new System.EventHandler(this.BtnSupprimerBadge_Click);
            // 
            // btnRafraichir
            // 
            this.btnRafraichir.Location = new System.Drawing.Point(337, 109);
            this.btnRafraichir.Name = "btnRafraichir";
            this.btnRafraichir.Size = new System.Drawing.Size(150, 30);
            this.btnRafraichir.TabIndex = 12;
            this.btnRafraichir.Text = "Rafraîchir les badges";
            this.btnRafraichir.UseVisualStyleBackColor = true;
            this.btnRafraichir.Click += new System.EventHandler(this.btnRafraichir_Click);
            // 
            // BtnAfficherUtilisateurs
            // 
            this.BtnAfficherUtilisateurs.Location = new System.Drawing.Point(491, 307);
            this.BtnAfficherUtilisateurs.Name = "BtnAfficherUtilisateurs";
            this.BtnAfficherUtilisateurs.Size = new System.Drawing.Size(150, 23);
            this.BtnAfficherUtilisateurs.TabIndex = 13;
            this.BtnAfficherUtilisateurs.Text = "Afficher les utilisateurs";
            this.BtnAfficherUtilisateurs.UseVisualStyleBackColor = true;
            this.BtnAfficherUtilisateurs.Click += new System.EventHandler(this.BtnAfficherUtilisateurs_Click);
            // 
            // BtnAssocierBadge
            // 
            this.BtnAssocierBadge.Location = new System.Drawing.Point(505, 113);
            this.BtnAssocierBadge.Name = "BtnAssocierBadge";
            this.BtnAssocierBadge.Size = new System.Drawing.Size(150, 23);
            this.BtnAssocierBadge.TabIndex = 15;
            this.BtnAssocierBadge.Text = "Associer un badge";
            this.BtnAssocierBadge.UseVisualStyleBackColor = true;
            this.BtnAssocierBadge.Click += new System.EventHandler(this.BtnAssocierBadge_Click);
            // 
            // comboBoxUtilisateurs
            // 
            this.comboBoxUtilisateurs.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxUtilisateurs.FormattingEnabled = true;
            this.comboBoxUtilisateurs.Location = new System.Drawing.Point(3, 337);
            this.comboBoxUtilisateurs.Name = "comboBoxUtilisateurs";
            this.comboBoxUtilisateurs.Size = new System.Drawing.Size(200, 21);
            this.comboBoxUtilisateurs.TabIndex = 14;
            this.comboBoxUtilisateurs.SelectedIndexChanged += new System.EventHandler(this.comboBoxUtilisateurs_SelectedIndexChanged);
            // 
            // checkBoxIsActive
            // 
            this.checkBoxIsActive.Location = new System.Drawing.Point(262, 241);
            this.checkBoxIsActive.Name = "checkBoxIsActive";
            this.checkBoxIsActive.Size = new System.Drawing.Size(150, 20);
            this.checkBoxIsActive.TabIndex = 16;
            this.checkBoxIsActive.Text = "Badge Actif";
            // 
            // FrmGestionBadgesSalles
            // 
            this.ClientSize = new System.Drawing.Size(653, 370);
            this.Controls.Add(this.lblUID);
            this.Controls.Add(this.txtUID);
            this.Controls.Add(this.BtnScanner);
            this.Controls.Add(this.BtnAjouter);
            this.Controls.Add(this.BtnVoirSalles);
            this.Controls.Add(this.comboBoxBadges);
            this.Controls.Add(this.lblListeBadges);
            this.Controls.Add(this.chkActif);
            this.Controls.Add(this.BtnModifierEtatBadge);
            this.Controls.Add(this.BtnSupprimerBadge);
            this.Controls.Add(this.btnRafraichir);
            this.Controls.Add(this.BtnAfficherUtilisateurs);
            this.Controls.Add(this.BtnAssocierBadge);
            this.Controls.Add(this.comboBoxUtilisateurs);
            this.Controls.Add(this.checkBoxIsActive);
            this.Name = "FrmGestionBadgesSalles";
            this.Text = "Gestion des Badges et Salles";
            this.Load += new System.EventHandler(this.FrmGestionBadgesSalles_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }
    }
}
