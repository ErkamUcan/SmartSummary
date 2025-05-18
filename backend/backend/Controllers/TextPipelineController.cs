using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;

namespace SmartSummaryAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TextPipelineController : ControllerBase
    {
        [HttpPost("run")]
        public async Task<IActionResult> RunPipeline([FromForm] string fileName, [FromForm] string question)
        {
            if (string.IsNullOrEmpty(fileName) || string.IsNullOrEmpty(question))
                return BadRequest("fileName ve question alanları zorunludur.");

            var scriptPath = "run_pipeline.py";
            var processStartInfo = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"{scriptPath} {fileName} \"{question}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            string output, error;
            using (var process = new Process())
            {
                process.StartInfo = processStartInfo;
                process.Start();

                output = await process.StandardOutput.ReadToEndAsync();
                error = await process.StandardError.ReadToEndAsync();

                process.WaitForExit();
            }

            if (!string.IsNullOrEmpty(error))
                return BadRequest(new { message = "Pipeline çalıştırılırken hata oluştu.", error });

            return Ok(new { message = "Pipeline başarıyla çalıştı.", output });
        }
    }
}
