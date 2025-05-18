using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Text;

namespace CleanUploadAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class EvaluationController : ControllerBase
    {
        [HttpPost("score")]
        public IActionResult Score([FromBody] ScoreRequest request)
        {
            var videoId = request.VideoId;
            var outputPath = Path.Combine("Summaries", $"{videoId}_summary.txt");
            var goldPath = Path.Combine("References", $"{videoId}_gold.txt");

            if (!System.IO.File.Exists(outputPath))
                return NotFound($"Sistem özeti bulunamadı: {outputPath}");

            if (!System.IO.File.Exists(goldPath))
                return NotFound($"Referans özet (gold summary) bulunamadı: {goldPath}");

            var result = RunPythonScript("evaluate_summary.py", $"{outputPath} {goldPath}");
            if (!result.Success)
                return Problem($"Skor hesaplama hatası:\n{result.Error}");

            return Ok(new
            {
                videoId,
                bert_f1 = ParseF1Score(result.Output),
                note = "BERTScore F1 - Türkçe semantik benzerlik"
            });
        }

        private float ParseF1Score(string output)
        {
            try
            {
                var line = output.Split('\n').FirstOrDefault(l => l.Contains("F1 Skoru"));
                var scoreStr = line?.Split(':')[1]?.Split('(')[0].Trim();
                return float.Parse(scoreStr.Replace(',', '.'), System.Globalization.CultureInfo.InvariantCulture);
            }
            catch
            {
                return -1f;
            }
        }

        private (bool Success, string Output, string Error) RunPythonScript(string scriptName, string arguments)
        {
            try
            {
                var startInfo = new ProcessStartInfo
                {
                    FileName = @"C:\Users\ahmet\CleanUploadAPI\.venv\Scripts\python.exe",
                    Arguments = $"python_scripts/{scriptName} {arguments}",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    WorkingDirectory = Directory.GetCurrentDirectory(),
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8
                };

                using var process = Process.Start(startInfo);
                string output = process.StandardOutput.ReadToEnd().Trim();
                string error = process.StandardError.ReadToEnd().Trim();
                process.WaitForExit();

                return (process.ExitCode == 0, output, error);
            }
            catch (Exception ex)
            {
                return (false, null, ex.Message);
            }
        }
    }

    public class ScoreRequest
    {
        public string VideoId { get; set; }
    }
}
