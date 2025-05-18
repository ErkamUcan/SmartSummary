using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Text;
using CleanUploadAPI.Models;

namespace CleanUploadAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class PipelineController : ControllerBase
    {
        [HttpPost("run")]
        public IActionResult Run([FromBody] PipelineRequest request)
        {
            var videoPath = Path.Combine("Uploads", request.VideoName);
            var wavPath = videoPath.Replace(".mp4", ".wav");
            var videoId = Path.GetFileNameWithoutExtension(request.VideoName);

            // 1. extract_audio.py
            var audio = RunPythonScript("extract_audio.py", videoPath);
            if (!audio.Success)
                return Problem($"Ses çıkarma hatası:\n{audio.Error}");

            // 2. transcribe_audio.py
            var transcript = RunPythonScript("transcribe_audio.py", wavPath);
            if (!transcript.Success)
                return Problem($"Transkripsiyon hatası:\n{transcript.Error}");

            // 3. chunk_text.py
            var transcriptPath = Path.Combine("Transcripts", $"{videoId}.txt");
            var chunk = RunPythonScript("chunk_text.py", transcriptPath);
            if (!chunk.Success)
                return Problem($"Chunking hatası:\n{chunk.Error}");

            // 4. semantic_search.py
            var semantic = RunPythonScript("semantic_search.py", $"\"{request.Question}\" \"{videoId}\"");
            if (!semantic.Success)
                return Problem($"Semantic search hatası:\n{semantic.Error}");

            // 5. summarize_with_nllb_translation.py (stdin ile)
            var summary = RunPythonScriptWithInput("summarize_with_nllb_translation.py", "-", semantic.Output);
            if (!summary.Success)
                return Problem($"Özetleme hatası:\n{summary.Error}");

            return Ok(summary.Output);
        }

        private (bool Success, string Output, string Error) RunPythonScript(string scriptName, string arguments)
        {
            try
            {
                Console.WriteLine($"\n--- [Başlıyor] {scriptName} ---");
                Console.WriteLine($"Komut: python_scripts/{scriptName} {arguments}");

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

                Console.WriteLine($"--- [Bitti] {scriptName} ---");
                Console.WriteLine($"[STDOUT ÇIKTI]\n{output}");
                if (!string.IsNullOrWhiteSpace(error))
                    Console.WriteLine($"[STDERR HATA]\n{error}");

                return (process.ExitCode == 0, output, error);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[EXCEPTION - {scriptName}] {ex.Message}");
                return (false, null, ex.Message);
            }
        }

        private (bool Success, string Output, string Error) RunPythonScriptWithInput(string scriptName, string arguments, string inputText)
        {
            try
            {
                Console.WriteLine($"\n--- [Başlıyor] {scriptName} (stdin input ile) ---");

                var startInfo = new ProcessStartInfo
                {
                    FileName = @"C:\Users\ahmet\CleanUploadAPI\.venv\Scripts\python.exe",
                    Arguments = $"python_scripts/{scriptName} {arguments}",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    RedirectStandardInput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    WorkingDirectory = Directory.GetCurrentDirectory(),
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8
                };

                using var process = new Process();
                process.StartInfo = startInfo;
                process.Start();

                process.StandardInput.WriteLine(inputText);
                process.StandardInput.Close();

                string output = process.StandardOutput.ReadToEnd().Trim();
                string error = process.StandardError.ReadToEnd().Trim();
                process.WaitForExit();

                Console.WriteLine($"--- [Bitti] {scriptName} ---");
                Console.WriteLine($"[STDOUT ÇIKTI]\n{output}");
                if (!string.IsNullOrWhiteSpace(error))
                    Console.WriteLine($"[STDERR HATA]\n{error}");

                return (process.ExitCode == 0, output, error);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[EXCEPTION - {scriptName}] {ex.Message}");
                return (false, null, ex.Message);
            }
        }
    }
}
