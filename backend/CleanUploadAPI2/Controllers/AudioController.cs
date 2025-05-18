using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace CleanUploadAPI.Controllers
{
    [ApiController]
    [Route("extract-audio")]
    public class AudioController : ControllerBase
    {
        [HttpPost]
        public IActionResult ExtractAudio([FromForm] string fileName)
        {
            var uploadsFolder = Path.Combine(Directory.GetCurrentDirectory(), "Uploads");
            var videoPath = Path.Combine(uploadsFolder, fileName);

            if (!System.IO.File.Exists(videoPath))
                return NotFound("Video dosyası bulunamadı.");

            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"python_scripts/extract_audio.py \"{videoPath}\"",
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            try
            {
                using var process = Process.Start(psi);
                string output = process.StandardOutput.ReadToEnd();
                process.WaitForExit();

                return Ok(new { message = "Ses çıkarma tamamlandı", output });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Hata oluştu: {ex.Message}");
            }
        }
    }
}
