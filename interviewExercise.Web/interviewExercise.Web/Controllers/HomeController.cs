using interviewExercise.Web.Models;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Net;
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
                    quote.ImageLink = GetImageUrlAsync(isGrayscale);
                }

                return Json(quote);
            }
            catch (Exception)
            {
                return Json(new ForismaticQuote { Error = true });
            }
        }

        private string GetImageUrlAsync(bool isGrayscale)
        {
            var imageUrlBuilder = new StringBuilder();
            int width = 536;
            int height = 354;
            string baseUrl = "https://picsum.photos";
            imageUrlBuilder.Append($"{baseUrl}/{width}/{height}");
            int randomNumber = new Random().Next(0, 100);

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
                return null;
            }
        }

        private async Task<HttpResponseMessage> GetApiResponseAsync(string format = "json")
        {
            using var client = new HttpClient();
            var url = $"https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format={format}";
            var response = await client.GetAsync(url);

            if (response.IsSuccessStatusCode)
            {
                return response;
            }

            return null;
        }




    }
}