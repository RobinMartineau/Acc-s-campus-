using System;
using System.Windows.Forms;

namespace GestionBadgesSalles
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new FrmGestionBadgesSalles()); // Assure-toi que c'est ce formulaire qui est lancé
        }
    }
}
