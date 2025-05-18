using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace CleanUploadAPI.Controllers
{
    [ApiController]
    [Route("transcribe-audio")]
    public class TranscribeController : ControllerBase
    {
        [HttpPost]
        public IActionResult Transcribe([FromForm] string fileName)
        {
            var uploadsFolder = Path.Combine(Directory.GetCurrentDirectory(), "Uploads");
            var audioPath = Path.Combine(uploadsFolder, Path.ChangeExtension(fileName, ".wav"));

            if (!System.IO.File.Exists(audioPath))
                return NotFound("Ses dosyası bulunamadı.");

            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"python_scripts/transcribe_audio.py \"{audioPath}\"",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            try
            {
                using var process = Process.Start(psi);
                string output = process.StandardOutput.ReadToEnd();
                process.WaitForExit();

                return Ok(new { message = "Transkripsiyon tamamlandı", output });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Hata oluştu: {ex.Message}");
            }
        }
    }
}
