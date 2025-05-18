var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
var app = builder.Build();
app.UseCors("AllowReactApp");

app.UseStaticFiles();
app.MapControllers();
app.Run();


builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp", policy =>
    {
        policy.WithOrigins("http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

