using Microsoft.AspNetCore.Mvc;

namespace CleanUploadAPI.Controllers
{
    [ApiController]
    [Route("upload-video")]
    public class VideoController : ControllerBase
    {
        [HttpPost]
        public async Task<IActionResult> UploadVideo(IFormFile file)
        {
            if (file == null || file.Length == 0)
                return BadRequest("Dosya yüklenemedi.");

            var folder = Path.Combine(Directory.GetCurrentDirectory(), "Uploads");
            if (!Directory.Exists(folder))
                Directory.CreateDirectory(folder);

            var filePath = Path.Combine(folder, file.FileName);

            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            return Ok(new { message = "Yükleme tamam", path = filePath });
        }
    }
}
