using System;
using System.Linq;
using System.Threading.Tasks;
using PCSC;
using PCSC.Iso7816;

namespace GestionBadgesSalles.Helpers
{
    public class NFCReader
    {
        // Méthode asynchrone pour lire l'UID d'un badge NFC
        public static async Task<string> LireUIDNFCAsync()
        {
            return await Task.Run(() =>
            {
                try
                {
                    using (var context = ContextFactory.Instance.Establish(SCardScope.System))
                    {
                        string lecteur = context.GetReaders().FirstOrDefault();
                        if (string.IsNullOrEmpty(lecteur))
                            throw new Exception("Aucun lecteur NFC trouvé.");

                        using (var isoReader = new IsoReader(context, lecteur, SCardShareMode.Shared, SCardProtocol.T1))
                        {
                            var apdu = new CommandApdu(IsoCase.Case2Short, isoReader.ActiveProtocol)
                            {
                                CLA = 0xFF,
                                INS = 0xCA,
                                P1 = 0x00,
                                P2 = 0x00,
                                Le = 0
                            };

                            var response = isoReader.Transmit(apdu);
                            return BitConverter.ToString(response.GetData()).Replace("-", "");
                        }
                    }
                }
                catch (Exception ex)
                {
                    // Si une erreur se produit lors de la lecture du badge
                    Console.WriteLine($"Erreur lors de la lecture du badge NFC : {ex.Message}");
                    return string.Empty; // Retourne une chaîne vide ou un message d'erreur
                }
            });
        }
    }
}
