using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace CleanUploadAPI.Controllers
{
    [ApiController]
    [Route("chunk-text")]
    public class ChunkController : ControllerBase
    {
        [HttpPost]
        public IActionResult ChunkText([FromForm] string fileName)
        {
            // Transkript dosya yolu (örn. Transcripts/testX.txt)
            var transcriptPath = Path.Combine("Transcripts", Path.GetFileNameWithoutExtension(fileName) + ".txt");

            if (!System.IO.File.Exists(transcriptPath))
                return NotFound(new { error = "Transkript dosyası bulunamadı.", path = transcriptPath });

            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"python_scripts/chunk_text.py \"{transcriptPath}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            try
            {
                using var process = Process.Start(psi);
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (process.ExitCode != 0)
                    return StatusCode(500, new { message = "Chunking sırasında hata oluştu", error });

                return Ok(new { message = "Chunking tamamlandı", output });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { message = "İşlem çalıştırılamadı", error = ex.Message });
            }
        }
    }
}
