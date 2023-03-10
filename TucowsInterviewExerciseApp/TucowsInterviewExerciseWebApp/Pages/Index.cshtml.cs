using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text.Json;
using System.Threading.Tasks;
using TucowsInterviewExerciseWebApp.Models;

namespace TucowsInterviewExerciseWebApp.Pages
{
    public class IndexModel : PageModel
    {
        // Apis base urls
        private const string QUOTES_API_URL = "http://api.forismatic.com/api/1.0/";
        private const string IMAGES_API_BASIC_URL = "https://picsum.photos";

        [BindProperty]
        public string key { get; set; }

        [BindProperty]
        public bool grayscaleImage { get; set; }

        public Quote responseObj = new Quote();
        public byte[] image = null;
        public string errorMsg = "";

        private readonly ILogger<IndexModel> _logger;

        public IndexModel(ILogger<IndexModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {
            if (image == null)
            {
                GetImage();
            }
            if (responseObj == null || responseObj.quoteText == null || responseObj.quoteText.Equals(""))
            {
                OnPost();
            }
        }

        public IActionResult OnPost()
        {
            //preparing quote api parameters
            var quoteKey = key;
            string requestParams = $"?method=getQuote&format=json&key={quoteKey}&lang=en";

            HttpClient client = new HttpClient();
            client.BaseAddress = new Uri(QUOTES_API_URL);

            client.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));

            //get the response
            HttpResponseMessage response = client.PostAsync(QUOTES_API_URL + requestParams, null).Result;

            if (response.IsSuccessStatusCode)
            {
                var responseContent = response.Content.ReadAsStringAsync().Result;
                Console.WriteLine(responseContent);

                try
                {
                    responseObj = JsonSerializer.Deserialize<Quote>(responseContent);
                    errorMsg = "";
                }
                catch (Exception e)
                {
                    errorMsg = e.ToString();
                }

            }
            else
            {
                Console.WriteLine("Error: " + response.StatusCode);
                errorMsg = "Error: " + response.StatusCode;
            }
            OnGet();
            return Page();


        }

        public void GetImage()
        {
            HttpClient client = new HttpClient();

            string imageApiURL = IMAGES_API_BASIC_URL + "/200/150";


            client.BaseAddress = new Uri(imageApiURL);
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept", "text/html,application/xhtml+xml,application/xml");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept-Encoding", "gzip, deflate");
            client.DefaultRequestHeaders.TryAddWithoutValidation("User-Agent", "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept-Charset", "ISO-8859-1");
            Console.WriteLine(imageApiURL);
            
            string requestParams = grayscaleImage ? "?grayscale" : "";

            HttpResponseMessage response = client.GetAsync(requestParams).Result;

            if (response.IsSuccessStatusCode)
            {
                var responseContent = response.Content.ReadAsStringAsync().Result;
                image = response.Content.ReadAsByteArrayAsync().Result; ;
                Console.WriteLine(responseContent);
            }
            else
            {
                Console.WriteLine("Error: " + response.StatusCode);
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }
        }
    }

}
