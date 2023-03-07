using interviewExercise.Web.Models;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Net;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

namespace interviewExercise.Web.Controllers
{
    public class HomeController : Controller
    {

        public IActionResult Index()
        {
            
            return View();
        }

        [HttpGet]
        public async Task<JsonResult> GetQuoteAsync(bool isGrayscale)
        {
            try
            {
                var quote = await GetQuoteAsync();

                if (quote != null)
                {
                    quote.ImageBase64String = await GetImageAsync(isGrayscale);
                }

                return Json(quote);
            }
            catch (Exception)
            {
                return Json(new ForismaticQuote { Error = true });
            }
        }
        private async Task<ForismaticQuote> GetQuoteAsync()
        {
            try
            {
                var response = await GetApiResponseAsync();
                var quote = await response.Content.ReadFromJsonAsync<ForismaticQuote>();
                return quote;
            }
            catch (Exception)
            {
                return await Task.FromResult<ForismaticQuote>(null);
            }
        }
        private async Task<HttpResponseMessage> GetApiResponseAsync(string format = "json")
        {
            using var client = new HttpClient();
            var url = $"https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format={format}";
            return await client.GetAsync(url);
        }
        private async Task<string> GetImageAsync(bool isGrayscale)
        {
            try
            {
                using var client = new HttpClient();
                client.DefaultRequestHeaders.Add("User-Agent", "C# App");

                int randomNumber = new Random().Next(0, 100);

                string imageUrl = GetImageUrl(isGrayscale, randomNumber);
                HttpResponseMessage response = await client.GetAsync(imageUrl);
                response.EnsureSuccessStatusCode();
                byte[] imageBytes = await response.Content.ReadAsByteArrayAsync();
                return ConvertJpegByteArrayToBase64(imageBytes);
            }   
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            return string.Empty;
        }
        private string ConvertJpegByteArrayToBase64(byte[] jpegByteArray)
        {
            return Convert.ToBase64String(jpegByteArray);
        }
        private string GetImageUrl(bool isGrayscale, int randomNumber)
        {
            var imageUrlBuilder = new StringBuilder();
            int width = 536;
            int height = 354;
            string baseUrl = "https://picsum.photos";
            imageUrlBuilder.Append($"{baseUrl}/{width}/{height}");

            if (isGrayscale)
            {
                imageUrlBuilder.Append($"?grayscale&random={randomNumber}");
            }
            else
            {
                imageUrlBuilder.Append($"?random={randomNumber}");
            }

            return imageUrlBuilder.ToString();
        }

    }
}